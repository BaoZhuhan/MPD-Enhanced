"""
MPD-Enhanced: Music Plagiarism Detection with Timbre + Lyrics Embedding.

Pipeline (3 phases):
  Phase 1 (transcription): Demucs → Beat → AST → ECAPA → Whisper → JSON
  Phase 2 (scoring):         Chroma matching + timbre boost + lyrics boost
  Phase 3 (judging):         LLM-based plagiarism judgment (placeholder)

Usage:
  python inference.py /path/to/song.wav
"""

import os
import sys

from transcription.pipeline import segment_transcription
from scoring.matcher import get_one_result
from judging.llm_judge import llm_judge
from schemas import MatchResult


def inference(audio_path):
    """Run the full 3-phase plagiarism detection pipeline."""

    # ── Phase 1: Feature extraction ──
    json_path = segment_transcription(audio_path)

    # ── Phase 2: Algorithmic matching ──
    raw_results = get_one_result(json_path)
    matches = result_formatting(raw_results)

    # ── Phase 3: LLM judgment (future) ──
    report = llm_judge(matches, features=None)

    return report


def result_formatting(result):
    """
    Convert raw CompareHelper results to structured MatchResult list.

    Args:
        result: sorted list of CompareHelper objects from get_one_result

    Returns:
        list of MatchResult
    """
    if not result or len(result) == 0:
        return []

    if isinstance(result, list) and len(result) > 0 and isinstance(result[0], str):
        return []  # "there is no note for this song"

    top_3 = []
    for i, compare_helper in enumerate(result[:3]):
        score = compare_helper.data[0]
        test_label = compare_helper.data[1]
        library_label = compare_helper.data[2]

        match = MatchResult.from_compare_data(
            rank=i + 1,
            score=float(score),
            test_label=test_label,
            library_label=library_label,
        )
        top_3.append(match)

    return top_3


if __name__ == "__main__":
    audio_path = sys.argv[1]
    result = inference(audio_path)
    print(result)
