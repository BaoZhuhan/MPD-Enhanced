"""
Shared data structures for MPD-Enhanced pipeline.

Phase 1 (transcription) produces SongFeatures.
Phase 2 (scoring) produces MatchResult objects.
Phase 3 (judging) consumes both to produce PlagiarismReport.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class SongFeatures:
    """Features extracted from a song during Phase 1 transcription."""
    title: str
    bpm: int
    rhythm: int
    downbeat_start: float
    beat_times: list
    vocal_info: list               # quantized MIDI notes
    vocal_embedding: Optional[list] = None  # 192-dim timbre vector
    lyrics: Optional[dict] = None          # {"full_text", "segments", "language"}


@dataclass
class BoostDetail:
    """Per-dimension boost information for frontend display."""
    available: bool = False
    value: float = 1.0
    cos_sim: Optional[float] = None       # timbre only
    lyrics_sim: Optional[float] = None    # lyrics only


@dataclass
class MatchResult:
    """A single match between input song and a library reference."""
    rank: int
    score: float
    song_title: str
    test_time: float
    test_time2: float
    library_time: float
    library_time2: float
    confidence: str                  # e.g. "47.5%"
    time_match: str                  # e.g. "Input: 60.1s ↔ Library: 133.3s"
    # 分维度得分，前端可展示"旋律 xx% + 音色 +x% + 歌词 -x%"
    chroma_score: Optional[float] = None
    timbre_boost: Optional[float] = None
    lyrics_boost: Optional[float] = None

    @classmethod
    def from_compare_data(cls, rank: int, score: float, test_label: dict,
                          library_label: dict, chroma_raw: float = None,
                          boost_details: dict = None) -> "MatchResult":
        """Construct from raw compare.py label dicts."""
        timbre_boost = None
        lyrics_boost = None
        if boost_details:
            timbre_boost = boost_details.get("timbre", {}).get("value")
            lyrics_boost = boost_details.get("lyrics", {}).get("value")

        return cls(
            rank=rank,
            score=score,
            song_title=library_label.get("title", "Unknown"),
            test_time=test_label.get("time", 0) if test_label else 0,
            test_time2=test_label.get("time2", 0) if test_label else 0,
            library_time=library_label.get("time", 0),
            library_time2=library_label.get("time2", 0),
            confidence=f"{score * 100:.1f}%",
            time_match=(
                f"Input: {test_label.get('time', 0):.1f}s ↔ "
                f"Library: {library_label.get('time', 0):.1f}s"
            ),
            chroma_score=round(chroma_raw, 4) if chroma_raw is not None else None,
            timbre_boost=round(timbre_boost, 4) if timbre_boost is not None else None,
            lyrics_boost=round(lyrics_boost, 4) if lyrics_boost is not None else None,
        )

    def to_dict(self) -> dict:
        """Convert to JSON-serializable dict for frontend."""
        return asdict(self)


@dataclass
class PlagiarismReport:
    """Final output: matches + optional LLM judgment."""
    matches: list[MatchResult] = field(default_factory=list)
    llm_judgment: Optional[dict] = None   # Phase 3 fills this
    llm_analysis: Optional[str] = None    # Phase 3 fills this
    message: str = "success"

    def to_dict(self) -> dict:
        """Convert to JSON-serializable dict for frontend."""
        return {
            "matches": [m.to_dict() for m in self.matches],
            "llm_judgment": self.llm_judgment,
            "llm_analysis": self.llm_analysis,
            "message": self.message,
        }
