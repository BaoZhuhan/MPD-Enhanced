"""
Phase 3: LLM-based plagiarism judgment using DeepSeek API.

Evaluates algorithmic similarity scores against music plagiarism
legal standards, famous case precedents, and musicological criteria
to produce a reasoned judgment with confidence and analysis.

Architecture:
  - knowledge_base.py: RAG context (legal standards, cases, criteria)
  - Prompt engineering: structured prompt with few-shot examples
  - DeepSeek API: OpenAI-compatible chat completion
  - Output: structured judgment with confidence + reasoning

Usage:
    from judging.llm_judge import llm_judge
    report = llm_judge(matches, features, api_key="sk-...")
"""

import os
import json
from schemas import MatchResult, SongFeatures
from judging.knowledge_base import KNOWLEDGE_BASE, JUDGMENT_GUIDELINES

# DeepSeek API configuration
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
DEEPSEEK_MODEL = "deepseek-chat"


def _build_prompt(matches, features):
    """Build the LLM prompt with case context, scores, and judgment request."""

    # Format match data for the prompt
    match_lines = []
    for i, m in enumerate(matches, 1):
        match_lines.append(
            f"Match #{i}: \"{m.song_title}\"\n"
            f"  Overall score: {m.confidence} ({m.score:.4f})\n"
            f"  Chroma (melody) raw: {m.chroma_score or 'N/A'}\n"
            f"  Timbre boost: {m.timbre_boost or 'N/A'} "
            f"{'(similar voice!)' if m.timbre_boost and m.timbre_boost > 1.03 else ''}\n"
            f"  Lyrics boost: {m.lyrics_boost or 'N/A'} "
            f"{'(similar lyrics!)' if m.lyrics_boost and m.lyrics_boost > 1.03 else ''}\n"
            f"  Time alignment: {m.time_match}"
        )

    match_text = "\n".join(match_lines)

    # Feature context
    feature_text = ""
    if features:
        feature_text = (
            f"Song BPM: {features.get('bpm', 'N/A')}, "
            f"Rhythm: {features.get('rhythm', 'N/A')}/4"
        )

    system_prompt = f"""You are an expert music plagiarism analyst. You combine
algorithmic similarity scores with legal standards and musicological analysis
to judge whether songs constitute plagiarism.

{KNOWLEDGE_BASE}

{JUDGMENT_GUIDELINES}

## OUTPUT FORMAT (JSON only, no markdown)
Return a JSON object with this exact structure:
{{
  "judgments": [
    {{
      "rank": 1,
      "matched_song": "song name",
      "verdict": "Likely Plagiarism" | "Possible Plagiarism" | "Probably Coincidental" | "Insufficient Evidence",
      "confidence": 85,
      "reasoning": "2-3 sentence analysis citing specific dimensions...",
      "key_evidence_for": ["melody similarity in chorus", "identical lyrics phrase"],
      "key_evidence_against": ["common chord progression", "different vocal timbre"],
      "relevant_case": "Name of similar legal precedent or N/A",
      "recommendation": "Next step recommendation"
    }}
  ],
  "overall_assessment": "1-2 paragraph summary",
  "risk_level": "High" | "Medium" | "Low"
}}
"""

    user_prompt = f"""Analyze the following music plagiarism detection results:

## Algorithmic Results
{match_text}

## Song Context
{feature_text if feature_text else 'No additional context available.'}

Please provide your plagiarism judgment for each match, applying the legal
standards and criteria from your knowledge base. Consider:
1. Whether the similarity scores cross the substantial similarity threshold
2. Whether the similar elements are protected expression or common vocabulary
3. How the timbre and lyrics boosts affect the assessment
4. Which famous cases are most analogous

Return ONLY valid JSON (no markdown, no commentary outside the JSON)."""

    return system_prompt, user_prompt


def _call_deepseek(system_prompt, user_prompt, api_key):
    """Call DeepSeek API with the constructed prompt."""
    from openai import OpenAI

    client = OpenAI(
        api_key=api_key,
        base_url=DEEPSEEK_BASE_URL,
    )

    response = client.chat.completions.create(
        model=DEEPSEEK_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,  # Low temp for consistent legal analysis
        max_tokens=2048,
        response_format={"type": "json_object"},
    )

    return response.choices[0].message.content


def _parse_response(text):
    """Parse LLM response into structured dict, with fallback."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Fallback: try to extract JSON from markdown code block
        import re
        match = re.search(r'```(?:json)?\s*([\s\S]*?)```', text)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
        return {
            "judgments": [],
            "overall_assessment": f"Failed to parse LLM response: {text[:200]}...",
            "risk_level": "Unknown",
            "raw_response": text,
        }


def llm_judge(matches, features=None, api_key=None):
    """
    Judge whether matched songs constitute plagiarism using LLM analysis.

    Args:
        matches: list of MatchResult from Phase 2 scoring
        features: SongFeatures from Phase 1 (optional)
        api_key: DeepSeek API key (or set DEEPSEEK_API_KEY env var)

    Returns:
        dict with matches, judgment, analysis, message
    """
    api_key = api_key or os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        return {
            "matches": matches,
            "judgment": None,
            "analysis": "LLM judgment skipped: no API key provided",
            "message": "success" if matches else "No matches found",
        }

    if not matches:
        return {
            "matches": [],
            "judgment": None,
            "analysis": "No matches to judge",
            "message": "No plagiarism matches found",
        }

    try:
        system_prompt, user_prompt = _build_prompt(matches, features)
        raw_response = _call_deepseek(system_prompt, user_prompt, api_key)
        judgment = _parse_response(raw_response)

        return {
            "matches": matches,
            "judgment": judgment.get("judgments", []),
            "analysis": judgment.get("overall_assessment", ""),
            "risk_level": judgment.get("risk_level", "Unknown"),
            "raw_llm_response": raw_response,
            "message": "success",
        }

    except Exception as e:
        return {
            "matches": matches,
            "judgment": None,
            "analysis": f"LLM judgment failed: {e}",
            "message": "success" if matches else "No matches found",
        }
