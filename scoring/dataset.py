"""
Test dataset classes for MPD-Enhanced scoring phase.

Loads pre-transcribed JSON files and produces piano-roll images
for segment-based chroma comparison.
"""

import torch
import jsonpickle
import unicodedata
from torch.utils.data import Dataset
from scoring.compare_utils import quantize_image, infos_to_pianorolls, get_duration_in_interval


class TestDataset(Dataset):
    """Dataset for the input (test) song."""

    def __init__(self, info_path, use_all=False, use_new_bpm=False,
                 inst=['vocal', 'melody'], condition=4):
        if use_new_bpm:
            self.library_files = [info_path.replace(".json", "newbpm.json")]
        else:
            self.library_files = [info_path]
        self.info_path = info_path
        self.use_all = use_all
        self.inst = inst
        self.condition = condition

    def __len__(self):
        return 1

    def get_chords(self, chord_info, time1, time2):
        if chord_info is None:
            return ['Unknown', 'Unknown', 'Unknown', 'Unknown']
        intervals = [(time1 + i * (time2 - time1) / 4,
                      time1 + (i + 1) * (time2 - time1) / 4) for i in range(4)]
        selected_chords = []
        for start_interval, end_interval in intervals:
            best_chord = None
            best_duration = 0
            for chord in chord_info:
                if chord['start'] <= end_interval and chord['end'] >= start_interval:
                    duration = get_duration_in_interval(chord, start_interval, end_interval)
                    if duration > best_duration:
                        best_duration = duration
                        best_chord = chord['chord']
            if best_chord:
                selected_chords.append(best_chord)
            else:
                selected_chords.append('Unknown')
        return selected_chords

    def get_structure(self, segment_label, time1, time2):
        max_overlap = 0
        target_label = None
        for segment in segment_label:
            overlap = min(segment['end'], time2) - max(segment['start'], time1)
            if overlap > 0:
                if overlap > max_overlap:
                    max_overlap = overlap
                    target_label = segment['label']
        return target_label

    def __getitem__(self, idx):
        images = []
        labels = []
        points = []
        info_links = self.library_files
        for info_link in info_links:
            with open(info_link, 'rb') as f:
                infos = jsonpickle.decode(f.read())
                test_piano, test_timing, test_point = infos_to_pianorolls(infos, self.use_all)
                one_bar_beat = (infos['beat_times'][1] - infos['beat_times'][0]) * infos['rhythm']
                for key in test_piano.keys():
                    if key in self.inst:
                        for time, image in test_piano[key].items():
                            second_values = [item[1] for item in test_point[key][time]]
                            unique_values = set(second_values)
                            if len(test_point[key][time]) > 4 and len(unique_values) >= 1:
                                image = torch.tensor(image).transpose(0, 1).unsqueeze(dim=0).float()
                                time1 = infos['downbeat_start'] + one_bar_beat * int(test_timing[time])
                                time2 = time1 + 4 * one_bar_beat
                                chord = self.get_chords(infos['chord_info'], time1, time2)
                                title = unicodedata.normalize('NFC', infos['title'])
                                label = {
                                    "title": title,
                                    "bpm": infos['bpm'],
                                    "newbpm": infos['new_bpm'],
                                    "inst": key,
                                    "time": time1,
                                    "time2": time2,
                                    "link": infos['link'],
                                    "shift": 0,
                                    "platform": infos['platform'],
                                    "song_start": infos['downbeat_start'] + one_bar_beat * int(test_timing[0]),
                                    "song_end": infos['beat_times'][-1],
                                    "chord": chord,
                                    "used_time": None,
                                    "info_link": info_link,
                                    "vocal_embedding": infos.get('vocal_embedding', None),
                                    "lyrics": infos.get('lyrics', None),
                                }
                                images.append(quantize_image(image))
                                labels.append(label)
                                points.append(test_point[key][time])
        return images, labels, points


class TestDataset2(Dataset):
    """Dataset for the covers80 library songs."""

    def __init__(self, library_files, inst=['vocal', 'melody'], condition=4):
        self.library_files = library_files
        self.use_all = True
        self.inst = inst
        self.condition = condition

    def __len__(self):
        return len(self.library_files)

    def get_chords(self, chord_info, time1, time2):
        if chord_info is None:
            return ['Unknown', 'Unknown', 'Unknown', 'Unknown']
        intervals = [(time1 + i * (time2 - time1) / 4,
                      time1 + (i + 1) * (time2 - time1) / 4) for i in range(4)]
        selected_chords = []
        for start_interval, end_interval in intervals:
            best_chord = None
            best_duration = 0
            for chord in chord_info:
                if chord['start'] <= end_interval and chord['end'] >= start_interval:
                    duration = get_duration_in_interval(chord, start_interval, end_interval)
                    if duration > best_duration:
                        best_duration = duration
                        best_chord = chord['chord']
            if best_chord:
                selected_chords.append(best_chord)
            else:
                selected_chords.append('Unknown')
        return selected_chords

    def get_structure(self, segment_label, time1, time2):
        max_overlap = 0
        target_label = None
        for segment in segment_label:
            overlap = min(segment['end'], time2) - max(segment['start'], time1)
            if overlap > 0:
                if overlap > max_overlap:
                    max_overlap = overlap
                    target_label = segment['label']
        return target_label

    def __getitem__(self, idx):
        images = []
        labels = []
        points = []
        info_link = self.library_files[idx]
        with open(info_link, 'rb') as f:
            infos = jsonpickle.decode(f.read())
            test_piano, test_timing, test_point = infos_to_pianorolls(infos, True)
            one_bar_beat = (infos['beat_times'][1] - infos['beat_times'][0]) * infos['rhythm']
            for key in test_piano.keys():
                if key in self.inst:
                    for time, image in test_piano[key].items():
                        second_values = [item[1] for item in test_point[key][time]]
                        unique_values = set(second_values)
                        if len(test_point[key][time]) > 4 and len(unique_values) >= 1:
                            image = torch.tensor(image).transpose(0, 1).unsqueeze(dim=0).float()
                            time1 = infos['downbeat_start'] + one_bar_beat * int(test_timing[time])
                            time2 = time1 + 4 * one_bar_beat
                            chord = self.get_chords(infos['chord_info'], time1, time2)
                            title = unicodedata.normalize('NFC', infos['title'])
                            label = {
                                "title": title,
                                "bpm": infos['bpm'],
                                "newbpm": infos['new_bpm'],
                                "inst": key,
                                "time": time1,
                                "time2": time2,
                                "shift": 0,
                                "platform": 'youtube',
                                "song_start": infos['downbeat_start'] + one_bar_beat * int(test_timing[0]),
                                "song_end": infos['beat_times'][-1],
                                "chord": chord,
                                "used_time": None,
                                "info_link": info_link,
                                "vocal_embedding": infos.get('vocal_embedding', None),
                                "lyrics": infos.get('lyrics', None),
                            }
                            images.append(quantize_image(image))
                            labels.append(label)
                            points.append(test_point[key][time])
        return images, labels, points


def compare_titles(title1, title2):
    """Case-insensitive alphanumeric-only title comparison."""
    def strip_to_basics(title):
        return ''.join(c.lower() for c in title if c.isalnum())
    return strip_to_basics(title1) == strip_to_basics(title2)
