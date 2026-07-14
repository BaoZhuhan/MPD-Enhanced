"""
Lyrics similarity computation for plagiarism detection.

Computes text similarity between two lyrics transcriptions using:
1. Character n-gram Jaccard similarity (robust to ASR errors)
2. TF-IDF cosine similarity (word-level, good for longer texts)
3. Normalized Levenshtein ratio (catches near-identical text)

Blended with n-gram having minimum 40% weight, since ASR transcription
errors make word-level matching unreliable for short lyrics.

Usage:
    from lyrics_similarity import compute_lyrics_similarity
    sim = compute_lyrics_similarity(lyrics1, lyrics2)
    # returns float in [0, 1]
"""

import re
import numpy as np
from collections import Counter


def _tokenize(text):
    """Normalize and tokenize text. Handles CJK by splitting characters."""
    text = text.lower().strip()
    # Check if text is primarily CJK (no spaces between words)
    cjk_count = sum(1 for c in text if '一' <= c <= '鿿' or
                    '぀' <= c <= 'ヿ' or '가' <= c <= '힯')
    if cjk_count > len(text) * 0.3:
        # CJK text: split into individual characters as tokens
        text = re.sub(r"[^\w\s一-鿿぀-ヿ가-힯]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        tokens = text.split()
        # Also add character-level tokens for CJK
        chars = [c for c in text.replace(" ", "") if cjk_count > 0]
        return tokens + chars
    else:
        # Non-CJK: standard word tokenization
        text = re.sub(r"[^\w\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text.split()


def _char_ngrams(text, n=3):
    """Extract character n-grams from text (whitespace removed)."""
    text = text.lower()
    text = re.sub(r"\s+", "", text)
    if len(text) < n:
        return [text]  # fallback: use whole text as one n-gram
    return [text[i:i+n] for i in range(len(text) - n + 1)]


def _tfidf_cosine(tokens1, tokens2):
    """Compute TF-IDF cosine similarity between two token lists."""
    if not tokens1 or not tokens2:
        return 0.0

    tf1 = Counter(tokens1)
    tf2 = Counter(tokens2)

    vocab = set(tf1.keys()) | set(tf2.keys())
    n_docs = 2

    def idf(term):
        df = (1 if term in tf1 else 0) + (1 if term in tf2 else 0)
        return np.log(1 + n_docs / max(df, 1))

    vec1 = np.array([tf1.get(t, 0) * idf(t) for t in vocab])
    vec2 = np.array([tf2.get(t, 0) * idf(t) for t in vocab])

    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0

    return float(np.dot(vec1, vec2) / (norm1 * norm2))


def _ngram_similarity(text1, text2, n=3):
    """Compute character n-gram Jaccard similarity."""
    ngrams1 = set(_char_ngrams(text1, n))
    ngrams2 = set(_char_ngrams(text2, n))

    if not ngrams1 or not ngrams2:
        return 0.0

    intersection = ngrams1 & ngrams2
    union = ngrams1 | ngrams2
    return len(intersection) / len(union)


def _levenshtein_ratio(text1, text2):
    """Normalized Levenshtein similarity ratio (0-1)."""
    s1 = re.sub(r"\s+", "", text1.lower())
    s2 = re.sub(r"\s+", "", text2.lower())

    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0

    len1, len2 = len(s1), len(s2)

    # Use two-row DP for memory efficiency
    prev = list(range(len2 + 1))
    curr = [0] * (len2 + 1)

    for i in range(1, len1 + 1):
        curr[0] = i
        for j in range(1, len2 + 1):
            cost = 0 if s1[i-1] == s2[j-1] else 1
            curr[j] = min(
                prev[j] + 1,        # deletion
                curr[j-1] + 1,      # insertion
                prev[j-1] + cost,   # substitution
            )
        prev, curr = curr, prev

    distance = prev[len2]
    max_len = max(len1, len2)
    return 1.0 - (distance / max_len)


def compute_lyrics_similarity(lyrics1, lyrics2):
    """
    Compute lyrics similarity between two transcription results.

    Uses a weighted blend of three metrics:
    - Character n-gram (2-gram + 3-gram): robust to ASR errors
    - TF-IDF cosine: word-level semantic overlap
    - Levenshtein ratio: catches near-identical but garbled text

    The blend ensures n-gram (most robust for ASR) always has ≥40% weight.

    Args:
        lyrics1, lyrics2: dict with "full_text" key, or str, or None

    Returns:
        float in [0, 1]: similarity score
    """
    if lyrics1 is None or lyrics2 is None:
        return 0.5  # neutral when lyrics unavailable

    text1 = lyrics1 if isinstance(lyrics1, str) else lyrics1.get("full_text", "")
    text2 = lyrics2 if isinstance(lyrics2, str) else lyrics2.get("full_text", "")

    if not text1 or not text2:
        return 0.5

    if text1 == text2:
        return 1.0  # fast path for identical

    # Tokenize
    tokens1 = _tokenize(text1)
    tokens2 = _tokenize(text2)

    # Compute three metrics
    tfidf_sim = _tfidf_cosine(tokens1, tokens2)

    # N-gram: use best of 2-gram and 3-gram
    ngram2 = _ngram_similarity(text1, text2, n=2)
    ngram3 = _ngram_similarity(text1, text2, n=3)
    ngram_sim = max(ngram2, ngram3)

    # Levenshtein ratio (character-level edit distance)
    lev_sim = _levenshtein_ratio(text1, text2)

    # Blend: n-gram always ≥40%, TF-IDF weight scales with text length
    min_len = min(len(tokens1), len(tokens2))
    tfidf_weight = min(0.40, min_len / 60)     # max 40% for TF-IDF
    ngram_weight = 1.0 - tfidf_weight           # at least 60% for n-gram

    combined = ngram_weight * ngram_sim + tfidf_weight * tfidf_sim

    # Boost: if Levenshtein ratio is high, it's a strong signal of similarity
    if lev_sim > 0.6:
        combined = max(combined, lev_sim * 0.9)

    return round(min(1.0, combined), 4)


def compute_lyrics_boost(lyrics1, lyrics2):
    """
    Compute the boost factor for plagiarism score based on lyrics similarity.

    Formula: boost = 1.0 + 0.10 × (lyrics_sim - 0.5)

    This means:
    - Identical lyrics (sim=1.0):   +5% boost
    - Very similar (sim=0.8):        +3% boost
    - Different (sim=0.2):           -3% penalty
    - Completely different (sim=0):  -5% penalty
    - Unknown/neutral (sim=0.5):     1.0 (no effect)
    """
    sim = compute_lyrics_similarity(lyrics1, lyrics2)
    boost = 1.0 + 0.10 * (sim - 0.5)
    boost = max(0.90, min(1.10, boost))
    return boost, sim
