"""
Vocal timbre embedding extraction using SpeechBrain ECAPA-TDNN.

Extracts a 192-dimensional speaker/timbre embedding from a vocal audio track.
This can be used to compare vocal similarity between songs for plagiarism detection.

Usage:
    from vocal_embedding import extract_vocal_embedding
    emb = extract_vocal_embedding("vocals.wav", device="cuda")
    # returns list of 192 floats, or None on failure
"""

import os
import torch
import torchaudio
import numpy as np

# Cache directory for model weights (group storage, not HOME)
CACHE_DIR = "/hpc/group/honglab/zb78/cache/speechbrain"

def extract_vocal_embedding(vocal_path, device="cuda"):
    """
    Extract 192-dim ECAPA-TDNN speaker embedding from vocal audio.

    Args:
        vocal_path: Path to vocal WAV file (from Demucs separation)
        device: "cuda" or "cpu"

    Returns:
        list of 192 floats (embedding), or None if extraction fails
    """
    try:
        from speechbrain.inference.speaker import EncoderClassifier
    except ImportError:
        print("[Timbre] speechbrain not installed. Install with: pip install speechbrain")
        return None

    if not os.path.exists(vocal_path):
        print(f"[Timbre] Vocal file not found: {vocal_path}")
        return None

    try:
        # Load model (auto-downloads to cache on first use)
        classifier = EncoderClassifier.from_hparams(
            source="speechbrain/spkrec-ecapa-voxceleb",
            run_opts={"device": device},
            savedir=CACHE_DIR,
        )

        # Load audio
        signal, sr = torchaudio.load(vocal_path)

        # Resample to 16kHz (ECAPA expects 16kHz)
        if sr != 16000:
            signal = torchaudio.functional.resample(signal, sr, 16000)

        # Convert to mono
        if signal.shape[0] > 1:
            signal = signal.mean(dim=0, keepdim=True)

        # Normalize
        signal = signal / signal.abs().max()

        # Move to device
        signal = signal.to(device)

        with torch.no_grad():
            embedding = classifier.encode_batch(signal)

        # Squeeze to 1D list
        emb = embedding.squeeze().cpu().numpy().tolist()
        print(f"[Timbre] Extracted {len(emb)}-dim embedding from {os.path.basename(vocal_path)}")
        return emb

    except Exception as e:
        print(f"[Timbre] Extraction failed: {e}")
        return None
