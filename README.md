<div align="center">

<h1>MPD-Enhanced: Multi-Dimensional Music Plagiarism Detection</h1>

  <br>

<p>
  <b>Fork of</b> <a href="https://github.com/Mippia/Music-Plagiarism-Detection"><b>Mippia/Music-Plagiarism-Detection</b></a><br>
  <i>Music Plagiarism Detection: Problem Formulation And A Segment-based Solution</i><br>
  <sub>Seonghyeon Go* · Yumin Kim* (MIPPIA Inc.)</sub>
</p>

[![Paper](https://img.shields.io/badge/arXiv-2601.21260-b31b1b)](https://arxiv.org/abs/2601.21260)
[![Original Project Page](https://img.shields.io/badge/Project-Website-blue)](https://mippia.github.io/icassp-mpd/)
[![Demo Page](https://img.shields.io/badge/Demo-Page-red)](https://huggingface.co/spaces/mippia/MPD-demo)

</div>

## Overview

**MPD-Enhanced** extends the original Music Plagiarism Detection pipeline with three
independent similarity dimensions — **melody**, **timbre**, and **lyrics** — plus an
**LLM-based plagiarism judge** that produces reasoned verdicts using legal standards
and case precedents.

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

### LLM Judger (Phase 3)

After algorithmic scoring, **DeepSeek V4 Flash** analyzes each match with RAG context:

- **Legal Standards**: substantial similarity test, scènes à faire, idea-expression dichotomy
- **Famous Cases**: Blurred Lines, Stairway to Heaven, Dark Horse, Thinking Out Loud, etc.
- **Musicological Criteria**: melody, harmony, rhythm, lyrics, timbre, structure
- **Output**: verdict (Likely/Possible/Probably Coincidental) + confidence + reasoning + relevant precedent

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
│   ├── boosts.py              # Timbre boost + lyrics boost functions
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
      → Verdict + Confidence + Reasoning + Precedent
```

## Usage

### Quick Start

```bash
# Clone and install
git clone git@github.com:BaoZhuhan/MPD-Enhanced.git
cd MPD-Enhanced
conda create -n mpd python=3.10 -y && conda activate mpd
pip install -r requirements.txt

# Run with convenience script
bash run.sh /path/to/song.mp3

# Or directly
python inference.py /path/to/song.mp3
```

### With LLM Judge

```bash
# Set API key
export DEEPSEEK_API_KEY="sk-..."

# Full pipeline with LLM judgment
python inference.py /path/to/song.mp3 "" "" "$DEEPSEEK_API_KEY"
```

### Python API

```python
from inference import inference

result = inference(
    audio_path="/path/to/song.mp3",
    library_path="covers80",       # optional: custom library
    output_dir="/tmp/output",      # optional: JSON output dir
    api_key="sk-...",              # optional: enables Phase 3 LLM judge
)

# Returns JSON-serializable dict
# {
#   "success": true,
#   "data": {
#     "matches": [{
#       "rank": 1,
#       "score": 0.475,
#       "song_title": "...",
#       "chroma_score": 0.45,       # raw melody match
#       "timbre_boost": 1.05,       # voice similarity
#       "lyrics_boost": 1.03        # text similarity
#     }],
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

### Model Caching

Models are downloaded on first use. To pre-download:

```python
# Timbre model (SpeechBrain ECAPA-TDNN, ~80MB)
from transcription.vocal_embedding import extract_vocal_embedding
extract_vocal_embedding("any_audio.wav", device="cpu")

# Lyrics model (faster-whisper base, ~150MB)
from transcription.lyrics_transcription import transcribe_lyrics
transcribe_lyrics("any_audio.wav", device="cpu")
```

Set `HF_ENDPOINT=https://hf-mirror.com` for faster downloads in China.

## Installation

### Requirements

- Python 3.10 (madmom compatibility)
- CUDA 12.6 (4× NVIDIA RTX 4090 D tested)
- Ubuntu 22.04 LTS

### Conda Environment (Recommended)

```bash
conda create -n mpd python=3.10 -y
conda activate mpd

# PyTorch with CUDA 12.6
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu126

# Core dependencies
pip install numpy==1.23.5 scipy==1.12.0 Cython
pip install madmom --no-build-isolation
pip install -r requirements.txt

# Additional
pip install openai          # for LLM Judger (DeepSeek API)
pip install torchcodec      # for audio loading
```

### madmom Compatibility

Python 3.10+ requires two patches (applied automatically by pip install):

- `madmom/__init__.py`: `pkg_resources` → `importlib.metadata`
- `madmom/processors.py`: `collections.MutableSequence` → `collections.abc.MutableSequence`

### NVIDIA Driver Safety

Driver 560.35.03 has a known bug causing kernel NULL pointer dereference
with pinned memory operations. `safety.py` applies these mitigations
automatically:

- `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True,backend:native`
- `CUDA_MODULE_LOADING=LAZY`
- DataLoader `pin_memory` globally disabled
- GPU memory limited to 75% per process
- `torch.cuda.synchronize()` + `torch.cuda.empty_cache()` between model switches

## Adding New Detection Dimensions

The 3-phase architecture supports adding new dimensions without modifying core logic:

1. **Feature extraction** — add a new module in `transcription/`
2. **Boost function** — add `compute_<name>_boost()` in `scoring/boosts.py`
3. **LLM context** — add relevant criteria in `judging/knowledge_base.py`

The pipeline and scoring engine auto-discover new boosts via `compute_all_boosts()`.

## License

GPL License (inherited from original work).

## Citation

```bibtex
@article{go2025music,
  title={Music Plagiarism Detection: Problem Formulation And A Segment-based Solution},
  author={Go, Seonghyeon and Kim, Yumin},
  journal={arXiv preprint arXiv:2601.21260},
  year={2025}
}
```
