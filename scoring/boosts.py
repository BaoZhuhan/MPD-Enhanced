"""
Scoring boost functions for MPD-Enhanced.

Each boost is an independent function that modifies the chroma similarity
score based on a specific dimension (timbre, lyrics, etc.).

Adding a new boost:
1. Write a function compute_<name>_boost(test_label, lib_label) -> (boost, detail)
2. Add it to compute_all_boosts()
"""

import numpy as np
from lyrics_similarity import compute_lyrics_boost


def compute_timbre_boost(test_label, lib_label):
    """
    Compute timbre similarity boost from ECAPA-TDNN embeddings.

    Formula: boost = 1.0 + 0.15 * (cos_sim - 0.5)
      - Same vocal timbre: up to +7.5%
      - Different timbre: up to -7.5%
      - No embedding: neutral (1.0)

    Returns (boost, detail_dict)
    """
    test_emb = test_label.get("vocal_embedding")
    lib_emb = lib_label.get("vocal_embedding")

    if test_emb is None or lib_emb is None:
        return 1.0, {"available": False}

    t_vec = np.array(test_emb, dtype=np.float64)
    l_vec = np.array(lib_emb, dtype=np.float64)
    t_norm = np.linalg.norm(t_vec)
    l_norm = np.linalg.norm(l_vec)

    if t_norm == 0 or l_norm == 0:
        return 1.0, {"available": True, "cos_sim": 0.0}

    cos_sim = float(np.dot(t_vec, l_vec) / (t_norm * l_norm))
    cos_sim = max(-1.0, min(1.0, cos_sim))
    boost = 1.0 + 0.15 * (cos_sim - 0.5)

    return boost, {"available": True, "cos_sim": round(cos_sim, 4)}


def compute_lyrics_boost_fn(test_label, lib_label):
    """
    Compute lyrics similarity boost from Whisper transcriptions.

    Formula: boost = 1.0 + 0.10 * (lyrics_sim - 0.5)
      - Identical lyrics: +5%
      - Different lyrics: -5%
      - No lyrics: neutral (1.0)

    Returns (boost, detail_dict)
    """
    test_lyrics = test_label.get("lyrics")
    lib_lyrics = lib_label.get("lyrics")

    if test_lyrics is None or lib_lyrics is None:
        return 1.0, {"available": False}

    boost, sim = compute_lyrics_boost(test_lyrics, lib_lyrics)

    return boost, {"available": True, "lyrics_sim": sim}


def compute_all_boosts(test_label, lib_label):
    """
    Compute all boost factors for a test-library song pair.

    Returns (total_boost, details)
    where total_boost = timbre_boost * lyrics_boost * ...
    and details = { "timbre": {...}, "lyrics": {...} }
    """
    details = {}
    total_boost = 1.0

    # Timbre boost
    tb, t_detail = compute_timbre_boost(test_label, lib_label)
    total_boost *= tb
    details["timbre"] = t_detail

    # Lyrics boost
    lb, l_detail = compute_lyrics_boost_fn(test_label, lib_label)
    total_boost *= lb
    details["lyrics"] = l_detail

    return total_boost, details
