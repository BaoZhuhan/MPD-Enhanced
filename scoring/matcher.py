"""
Phase 2: Chroma-based plagiarism matching engine.

Matches the input song against the covers80 library using:
- 4-bar sliding window chroma comparison
- Time shift (-5 to +5) and pitch invariance
- BPM ratio compensation
- Multi-dimensional boost fusion (timbre, lyrics)
"""

import torch
import heapq
import os
import glob
from tqdm import tqdm
from torch.utils.data import DataLoader
from scoring.dataset import TestDataset, TestDataset2
from scoring.boosts import compute_all_boosts
from scoring.compare_utils import remove_1, algorithmic_collate3, CompareHelper, \
    shift_image_optimized, piano_roll_to_chroma, calculate_correlation

covers80_path = "covers80"
youtubecover_jsons = glob.glob(os.path.join(covers80_path, "*.json"))


def get_one_result(info_json):
    """
    Compare input song JSON against all covers80 library songs.

    Returns sorted list of CompareHelper objects (best matches first).
    """
    device = torch.device('cpu')
    use_new_bpm = False
    inst = 'vocal'

    # Load test song
    test_dataset = TestDataset(info_json, use_new_bpm=use_new_bpm, inst=[inst])
    imgs, labels, points = test_dataset[0]
    test_images = [img for img in imgs]
    test_labels = [label for label in labels]
    test_points = [remove_1(point) for point in points]

    # Retry with relaxed conditions if needed
    try:
        test_images = torch.cat(test_images).to(device)
    except Exception:
        test_dataset = TestDataset(info_json, use_new_bpm=use_new_bpm, inst=['vocal'], condition=0)
        imgs, labels, points = test_dataset[0]
        test_images = [img for img in imgs]
        test_labels = [label for label in labels]
        test_points = [remove_1(point) for point in points]
        try:
            test_images = torch.cat(test_images).to(device)
        except Exception as e:
            test_dataset = TestDataset(info_json, use_new_bpm=use_new_bpm, inst=['vocal'], condition=0)
            imgs, labels, points = test_dataset[0]
            test_images = [img for img in imgs]
            test_labels = [label for label in labels]
            test_points = [remove_1(point) for point in points]
            try:
                test_images = torch.cat(test_images).to(device)
            except Exception:
                print(e)
                return ["there is no note for this song"], []

    test_bpms = torch.tensor([label['bpm'] for label in labels])
    test_bpms_expanded = test_bpms[:, None]
    test_images_expanded = test_images[:, None, :, :].to(device)

    # Load covers80 library
    additional_test_dataset = TestDataset2(youtubecover_jsons, inst=[inst], condition=0)
    additional_test_loader = DataLoader(additional_test_dataset, batch_size=40,
                                        collate_fn=algorithmic_collate3)

    compare_result = []
    max_heap_size = 1000

    for idx, (lib_images, lib_labels, lib_points) in tqdm(
            enumerate(additional_test_loader)):
        lib_images = torch.cat(lib_images).to(device).squeeze(1)
        lib_images_expanded = lib_images[None, :, :, :].to(device)
        lib_bpms = torch.tensor([lbl['bpm'] for lbl in lib_labels]).to(device)
        lib_bpms_expanded = lib_bpms[None, :]

        metrics = calculate_metric_optimized(
            test_images_expanded, lib_images_expanded,
            test_points, lib_points,
            test_bpms_expanded, lib_bpms_expanded,
            device
        )

        for i, test_label in enumerate(test_labels):
            for j, lib_label in enumerate(lib_labels):
                metric = metrics[i, j].item()
                final_metric = min(metric, 1.0)

                # Apply all dimension boosts (timbre + lyrics + future)
                total_boost, _ = compute_all_boosts(test_label, lib_label)
                final_metric *= total_boost

                result_entry = CompareHelper([
                    final_metric, test_label, lib_label,
                    test_points[i], lib_points[j]
                ])

                # Top-K heap
                if len(compare_result) < max_heap_size:
                    heapq.heappush(compare_result, result_entry)
                elif result_entry.data[0] > compare_result[0].data[0]:
                    heapq.heappop(compare_result)
                    heapq.heappush(compare_result, result_entry)

    sorted_results = sorted(compare_result, key=lambda x: x.data[0], reverse=True)
    return sorted_results


def calculate_metric_optimized(images1, images2, points1, points2, bpms1, bpms2, device):
    """
    Compute chroma similarity matrix with time-shift and pitch invariance.

    Returns max metric over all shift combinations.
    """
    images1 = piano_roll_to_chroma(images1)
    images2 = piano_roll_to_chroma(images2)
    min_length1 = min(images1.shape[0], len(points1))
    min_length2 = min(images2.shape[1], len(points2))
    images1 = images1[:min_length1]
    images2 = images2[:min_length2]
    points1 = points1[:min_length1]
    points2 = points2[:min_length2]
    bpms1 = bpms1[:, :min_length1]
    bpms2 = bpms2[:, :min_length2]

    # Build rhythm matrices
    rhythm_images2 = torch.zeros((images2.shape[1], 64)).to(device)
    if rhythm_images2.shape[0] < len(points2):
        rhythm_images2 = torch.zeros((len(points2), 64)).to(device)
    for j, pts in enumerate(points2):
        if j < len(rhythm_images2):
            pts_tensor = torch.tensor(pts).to(device)
            indices = torch.round(pts_tensor[:, 0] / 3.0).long()
            indices = torch.clamp(indices, max=63)
            rhythm_images2[j, indices] = 1

    # Time-shifted variants
    shifted_images1_list = []
    shifted_bpms1_list = []
    shift_count = 0
    for pitch_shifts in [0]:
        for time_shifts in [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]:
            shifted_images1_list.append(shift_image_optimized(images1, time_shifts, pitch_shifts))
            shifted_bpms1_list.append(bpms1)
            shift_count += 1
    shifted_images1_batch = torch.cat(shifted_images1_list, dim=0).to(device)
    shifted_bpms1_batch = torch.cat(shifted_bpms1_list, dim=0).to(device)

    rhythm_images1_batch = torch.zeros((shifted_images1_batch.shape[0], 64)).to(device)
    dtw_images1_batch = torch.zeros_like(rhythm_images1_batch)

    for i, pts in enumerate(points1):
        pts_tensor = torch.tensor(pts).to(device)
        start_times = torch.round(pts_tensor[:, 0] / 3.0).long()
        pitches = pts_tensor[:, 1].long()
        start_times = torch.clamp(start_times, max=63)
        pitches = torch.clamp(pitches, max=127)
        end_times = torch.cat([start_times[1:], torch.tensor([64]).to(device)])
        for k in range(len(shifted_images1_list)):
            rhythm_images1_batch[i + k * len(points1), start_times] = 1
            batch_index = i + k * len(points1)
            for jt in range(len(start_times)):
                dtw_images1_batch[batch_index, start_times[jt]:end_times[jt]] = pitches[jt].float()

    dtw_images2_batch = torch.zeros_like(rhythm_images2).to(device)
    for j, pts in enumerate(points2):
        if j < len(dtw_images2_batch):
            pts_tensor = torch.tensor(pts).to(device)
            start_times = torch.round(pts_tensor[:, 0] / 3.0).long()
            pitches = pts_tensor[:, 1].long()
            start_times = torch.clamp(start_times, max=63)
            pitches = torch.clamp(pitches, max=127)
            end_times = torch.cat([start_times[1:], torch.tensor([64]).to(device)])
            batch_mask = torch.zeros(dtw_images2_batch.size(1)).to(device)
            for jt in range(len(start_times)):
                batch_mask[start_times[jt]:end_times[jt]] = pitches[jt].float()
            dtw_images2_batch[j] = batch_mask

    # BPM ratio compensation
    min_bpm_optimized = torch.min(shifted_bpms1_batch, bpms2)
    max_bpm_optimized = torch.max(shifted_bpms1_batch, bpms2)
    bpm_ratio_optimized = (min_bpm_optimized / max_bpm_optimized) ** 0.65

    # Rhythm correlation
    max_shift = 8
    correlation = calculate_correlation(rhythm_images1_batch, rhythm_images2, max_shift, device)

    # Pitch similarity
    unique_pitches_intersection = ((shifted_images1_batch * images2).sum(dim=3) > 0).float().sum(dim=2)
    unique_pitches_image2 = (images2.sum(dim=3) > 0).float().sum(dim=2)
    unique_pitches_image1 = (shifted_images1_batch.sum(dim=3) > 0).float().sum(dim=2)
    difficulty = 1 / (1 + torch.exp(((unique_pitches_image2 + unique_pitches_image1) - 9) * -0.5))
    pitch_score = 2 * unique_pitches_intersection / (unique_pitches_image2 + unique_pitches_image1)
    final_pitch_score = pitch_score * difficulty

    # Final metric
    total = (shifted_images1_batch + images2).clamp_(0, 1).sum(dim=(2, 3))
    intersection = (shifted_images1_batch * images2).sum(dim=(2, 3))
    ratio = intersection / total
    metrics = (0.5 + final_pitch_score) * (ratio * 1.05 + 0.15 * torch.maximum(correlation, ratio)) * bpm_ratio_optimized
    metrics = metrics.clamp_(0, 1)
    metrics_reshaped = metrics.view(shift_count, -1, *metrics.shape[1:])
    max_metric, _ = torch.max(metrics_reshaped, dim=0)

    return max_metric
