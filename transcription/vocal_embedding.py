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
import numpy as np
import soundfile as sf

# 配置 hf-mirror（解决国内访问 HuggingFace 的问题）
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")

# 本地缓存目录（相对于项目根目录）
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "model_cache", "hub")


def _load_audio(path, target_sr=16000):
    """使用 soundfile 加载音频（避免 torchcodec 依赖问题）"""
    audio, sr = sf.read(path, dtype="float32")

    # 转 mono
    if audio.ndim > 1:
        audio = audio.mean(axis=1)

    # 转 tensor
    signal = torch.from_numpy(audio).unsqueeze(0)  # (1, samples)

    # 重采样到 16kHz
    if sr != target_sr:
        import torchaudio.functional as F
        signal = F.resample(signal, sr, target_sr)

    # 归一化
    signal = signal / signal.abs().max()

    return signal


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
        # 修复 device 格式：SpeechBrain 需要 "cuda:0" 而非 "cuda"
        if device == "cuda":
            device = "cuda:0"

        # 从本地缓存加载模型（已通过 hf-mirror 预下载）
        classifier = EncoderClassifier.from_hparams(
            source="speechbrain/spkrec-ecapa-voxceleb",
            run_opts={"device": device},
            savedir=CACHE_DIR,
        )

        # 使用 soundfile 加载音频（避免 torchcodec CUDA 依赖问题）
        signal = _load_audio(vocal_path)

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
