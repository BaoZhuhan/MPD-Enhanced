"""
Phase 3: LLM-based plagiarism judgment.

Placeholder - will be implemented with an LLM that evaluates
the similarity scores, song features, and known plagiarism cases
to produce a final judgment with detailed analysis.

Expected interface:
    llm_judge(matches, features) → PlagiarismReport

For now, it passes through matches without additional judgment.
"""


def llm_judge(matches, features=None):
    """
    Judge whether the matched songs constitute plagiarism.

    Args:
        matches: list of MatchResult from Phase 2 scoring
        features: SongFeatures from Phase 1 (optional, for context)

    Returns:
        dict with keys: matches, judgment, analysis, message
    """
    return {
        "matches": matches,
        "judgment": None,       # TODO: LLM判断结果
        "analysis": None,       # TODO: LLM分析文本
        "message": "success" if matches else "No matches found"
    }
