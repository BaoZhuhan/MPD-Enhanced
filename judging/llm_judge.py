"""
Phase 3: LLM-based plagiarism judgment.

Placeholder - will be implemented with an LLM that evaluates
the similarity scores, song features, and known plagiarism cases
to produce a final judgment with detailed analysis.

Interface for future LLM integration:
    llm_judge(matches, features) → dict with matches, judgment, analysis
"""

from schemas import PlagiarismReport


def llm_judge(matches, features=None):
    """
    Judge whether the matched songs constitute plagiarism.

    Args:
        matches: list of MatchResult from Phase 2 scoring
        features: SongFeatures from Phase 1 (optional)

    Returns:
        dict with keys: matches, judgment, analysis, message
    """
    report = PlagiarismReport(
        matches=matches if matches else [],
        llm_judgment=None,      # TODO: LLM判断结果
        llm_analysis=None,      # TODO: LLM分析文本
        message="success" if matches else "No plagiarism matches found",
    )
    return {
        "matches": report.matches,
        "judgment": report.llm_judgment,
        "analysis": report.llm_analysis,
        "message": report.message,
    }
