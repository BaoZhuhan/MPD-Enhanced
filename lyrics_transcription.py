"""
Lyrics transcription using faster-whisper.

Transcribes vocal audio to text lyrics with timestamps.
Uses hf-mirror for model access.

Usage:
    from lyrics_transcription import transcribe_lyrics
    lyrics = transcribe_lyrics("vocals.wav", device="cuda")
    # returns list of {"start": float, "end": float, "text": str}
"""

import os

# 配置 hf-mirror
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")


def transcribe_lyrics(vocal_path, model_size="base", device="cuda"):
    """
    Transcribe lyrics from vocal audio using faster-whisper.

    Args:
        vocal_path: Path to vocal WAV file
        model_size: Whisper model size (tiny/base/small/medium/large-v3)
        device: "cuda" or "cpu"

    Returns:
        dict with:
            - "full_text": complete transcription text
            - "segments": list of {"start": float, "end": float, "text": str}
            - "language": detected language code
        or None on failure
    """
    if not os.path.exists(vocal_path):
        print(f"[Lyrics] Vocal file not found: {vocal_path}")
        return None

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("[Lyrics] faster-whisper not installed. Run: pip install faster-whisper")
        return None

    try:
        # faster-whisper 使用 "cuda"/"cpu" 格式（非 "cuda:0"）
        compute_type = "float16" if device in ("cuda", "cuda:0") else "int8"
        whisper_device = "cuda" if device in ("cuda", "cuda:0") else device

        print(f"[Lyrics] Loading Whisper {model_size} on {whisper_device}...")
        model = WhisperModel(model_size, device=whisper_device, compute_type=compute_type)

        print(f"[Lyrics] Transcribing {os.path.basename(vocal_path)}...")
        segments, info = model.transcribe(
            vocal_path,
            beam_size=5,
            vad_filter=True,
            vad_parameters=dict(
                min_silence_duration_ms=500,
            ),
        )

        full_text = []
        seg_list = []
        for seg in segments:
            text = seg.text.strip()
            if text:
                full_text.append(text)
                seg_list.append({
                    "start": round(seg.start, 2),
                    "end": round(seg.end, 2),
                    "text": text,
                })

        result = {
            "full_text": " ".join(full_text),
            "segments": seg_list,
            "language": info.language,
        }

        print(f"[Lyrics] Transcribed {len(seg_list)} segments "
              f"({len(result['full_text'].split())} words, lang={info.language})")
        return result

    except Exception as e:
        print(f"[Lyrics] Transcription failed: {e}")
        return None
