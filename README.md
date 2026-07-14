<div align="center">

<h1>MPD-Enhanced: Multi-Dimensional Music Plagiarism Detection</h1>

  <br>

<p>
  <b>Melody × Timbre × Lyrics × LLM Judgment</b><br>
  <sub>A three-phase pipeline for automated music plagiarism detection with AI-powered legal reasoning</sub>
</p>

</div>

## Overview

MPD-Enhanced detects music plagiarism across three independent dimensions and
provides AI-powered legal judgment. It builds on the segment-based music
plagiarism detection framework proposed by Go & Kim (2025) [[arXiv:2601.21260](https://arxiv.org/abs/2601.21260)],
extending it with vocal timbre embedding, lyrics transcription, and an LLM-based
judge that evaluates matches against real-world legal standards and case precedents.

### Detection Dimensions

| Dimension | Method | Model | Weight |
|-----------|--------|-------|--------|
| **Melody** (chroma) | 4-bar sliding window, time+pitch shift invariance | AST (EfficientNet-b0) → MIDI | Primary |
| **Timbre** (voice) | 192-dim cosine similarity | ECAPA-TDNN (SpeechBrain) | ±7.5% boost |
| **Lyrics** (text) | n-gram + TF-IDF + Levenshtein blend | faster-whisper (base) | ±5% boost |

### Scoring Formula

```
FINAL = chroma_similarity
      × timbre_boost(1.0 + 0.15 × (cos_sim - 0.5))
      × lyrics_boost(1.0 + 0.10 × (lyrics_sim - 0.5))
```

### LLM Judger

After algorithmic scoring, **DeepSeek V4 Flash** evaluates each match using RAG context:

- **Legal Standards**: substantial similarity test, scènes à faire, idea-expression dichotomy
- **Famous Cases**: Blurred Lines, Stairway to Heaven, Dark Horse, Thinking Out Loud, etc.
- **Musicological Criteria**: melody, harmony, rhythm, lyrics, timbre, structure
- **Output**: verdict + confidence + reasoning + relevant precedent + risk level

## Architecture

```
MPD-Enhanced/
├── inference.py               # Entry point: 3-phase orchestration
├── safety.py                  # NVIDIA driver crash mitigation
├── schemas.py                 # SongFeatures, MatchResult, PlagiarismReport
├── run.sh                     # Convenience script with safety env vars
│
├── transcription/             # Phase 1: Feature extraction
│   ├── pipeline.py            # Demucs → Beat → AST → ECAPA → Whisper → JSON
│   ├── vocal_embedding.py     # ECAPA-TDNN timbre embedding (192-dim)
│   ├── lyrics_transcription.py # faster-whisper lyrics transcription
│   └── wav_quantizer.py       # Beat-Transformer rhythm quantization
│
├── scoring/                   # Phase 2: Algorithmic matching
│   ├── matcher.py             # Chroma engine + covers80 comparison
│   ├── dataset.py             # TestDataset for input & library songs
│   ├── boosts.py              # Timbre + lyrics boost functions
│   └── compare_utils.py       # Piano-roll, chroma, correlation utilities
│
├── judging/                   # Phase 3: LLM plagiarism judgment
│   ├── llm_judge.py           # DeepSeek API + prompt engineering
│   └── knowledge_base.py      # RAG context: cases, standards, criteria
│
├── lyrics_similarity.py       # Lyrics text similarity (n-gram + TF-IDF + Levenshtein)
├── music_info.py              # Song data model
├── utils.py                   # MIDI quantization, JSON serialization
├── ml_models/                 # Model weights (Beat-Transformer, AST)
├── covers80/                  # Reference library (164 songs)
└── model_cache/               # Downloaded models (gitignored)
```

## Pipeline

```
Input Audio (.wav/.mp3)
  │
  ├─ Phase 1: Transcription ─────────────────────────────
  │   Step 1-2: Demucs → vocal/piano/drums/bass/other
  │   Step 5:   Beat-Transformer → beat_times, downbeats, BPM
  │   Step 6:   AST → MIDI notes (pitch + timing)
  │   Step 6.5: ECAPA-TDNN → 192-dim timbre embedding
  │   Step 6.6: faster-whisper → lyrics text + language
  │   Step 7:   → song.json (with vocal_embedding + lyrics)
  │
  ├─ Phase 2: Scoring ──────────────────────────────────
  │   4-bar chroma matching × time/pitch shifts × BPM ratio
  │   × timbre_boost × lyrics_boost
  │   → Top-3 matches (with per-dimension scores)
  │
  └─ Phase 3: Judgment ─────────────────────────────────
      DeepSeek V4 Flash + RAG (legal cases, musicological criteria)
      → Verdict + Confidence + Reasoning + Precedent + Risk Level
```

## Usage

### Quick Start

```bash
git clone git@github.com:BaoZhuhan/MPD-Enhanced.git
cd MPD-Enhanced
conda create -n mpd python=3.10 -y && conda activate mpd
pip install -r requirements.txt

# Run
bash run.sh /path/to/song.mp3
```

### With LLM Judge

```bash
export DEEPSEEK_API_KEY="sk-..."

python inference.py /path/to/song.mp3 "" "" "$DEEPSEEK_API_KEY"
```

### Python API

```python
from inference import inference

result = inference(
    audio_path="/path/to/song.mp3",
    library_path="covers80",       # optional
    output_dir="/tmp/output",      # optional
    api_key="sk-...",              # enables Phase 3
)

# Returns:
# {
#   "success": true,
#   "data": {
#     "matches": [
#       {
#         "rank": 1, "score": 0.475, "song_title": "...",
#         "chroma_score": 0.45,   # raw melody match
#         "timbre_boost": 1.05,   # voice similarity
#         "lyrics_boost": 1.03    # text similarity
#       }
#     ],
#     "judgment": [{
#       "verdict": "Possible Plagiarism",
#       "confidence": 65,
#       "reasoning": "...",
#       "relevant_case": "Skidmore v. Led Zeppelin"
#     }],
#     "risk_level": "Low",
#     "analysis": "Overall assessment..."
#   }
# }
```

## Installation

### Requirements

- Python 3.10 (madmom compatibility)
- CUDA 12.6 (GPU recommended: 4× RTX 4090 D tested)
- Ubuntu 22.04 LTS

### Conda Environment

```bash
conda create -n mpd python=3.10 -y
conda activate mpd

# PyTorch with CUDA 12.6
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu126

# Core dependencies
pip install numpy==1.23.5 scipy==1.12.0 Cython
pip install madmom --no-build-isolation
pip install -r requirements.txt

# Optional: LLM Judger
pip install openai
```

### Model Caching

Models download automatically on first use. In China, set `HF_ENDPOINT=https://hf-mirror.com` to
speed up downloads.

### NVIDIA Driver Safety

`safety.py` applies automatic mitigations for NVIDIA driver 560.35.03 (kernel crash
triggered by pinned memory operations):

- `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True,backend:native`
- DataLoader `pin_memory` globally disabled
- GPU memory limited to 75% per process
- CUDA sync + cache clear between model switches

## Adding Detection Dimensions

1. **Feature extraction** — add a new module in `transcription/`
2. **Boost function** — add `compute_<name>_boost()` in `scoring/boosts.py`
3. **LLM context** — add criteria in `judging/knowledge_base.py`

The pipeline auto-discovers new boosts via `compute_all_boosts()`.

## License

GPL License.

## Citation

```bibtex
@article{go2025music,
  title={Music Plagiarism Detection: Problem Formulation And A Segment-based Solution},
  author={Go, Seonghyeon and Kim, Yumin},
  journal={arXiv preprint arXiv:2601.21260},
  year={2025}
}
```
