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
import json
import traceback

from transcription.pipeline import segment_transcription
from scoring.matcher import get_one_result
from judging.llm_judge import llm_judge
from schemas import MatchResult, PlagiarismReport


def inference(audio_path, library_path=None, output_dir=None):
    """
    Run the full 3-phase plagiarism detection pipeline.

    Args:
        audio_path: path to input audio file
        library_path: path to covers80 library dir (default: auto-detect)
        output_dir: directory for output JSON (default: same as input)

    Returns:
        dict with keys:
          - success: bool
          - data: PlagiarismReport serialized (on success)
          - error: str (on failure)
    """
    try:
        # ── Phase 1: Feature extraction ──
        json_path = segment_transcription(audio_path, output_dir=output_dir)

        # ── Phase 2: Algorithmic matching ──
        raw_results = get_one_result(json_path, library_path=library_path)
        matches = result_formatting(raw_results)

        # ── Phase 3: LLM judgment (future) ──
        report = llm_judge(matches)

        return {
            "success": True,
            "data": _serialize(report),
        }

    except FileNotFoundError as e:
        return {
            "success": False,
            "error": f"File not found: {e}",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
        }


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

    top_matches = []
    for i, compare_helper in enumerate(result[:3]):
        score = compare_helper.data[0]
        test_label = compare_helper.data[1]
        library_label = compare_helper.data[2]

        # 提取分维度信息 (data[5]=chroma_raw, data[6]=boost_details)
        chroma_raw = None
        boost_details = None
        if len(compare_helper.data) >= 7:
            chroma_raw = compare_helper.data[5]
            boost_details = compare_helper.data[6]

        match = MatchResult.from_compare_data(
            rank=i + 1,
            score=float(score),
            test_label=test_label,
            library_label=library_label,
            chroma_raw=chroma_raw,
            boost_details=boost_details,
        )
        top_matches.append(match)

    return top_matches


def _serialize(report):
    """Convert PlagiarismReport to JSON-safe dict."""
    if isinstance(report, dict) and "matches" in report:
        return {
            "matches": [
                m.to_dict() if hasattr(m, "to_dict") else m
                for m in report["matches"]
            ],
            "judgment": report.get("judgment"),
            "analysis": report.get("analysis"),
            "message": report.get("message", "success"),
        }
    return report


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": "Usage: python inference.py <audio_path>"}))
        sys.exit(1)

    audio_path = sys.argv[1]
    library_path = sys.argv[2] if len(sys.argv) > 2 else None
    output_dir = sys.argv[3] if len(sys.argv) > 3 else None

    result = inference(audio_path, library_path=library_path, output_dir=output_dir)
    print(json.dumps(result, indent=2, ensure_ascii=False))
