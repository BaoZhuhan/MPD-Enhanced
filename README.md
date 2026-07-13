<div align="center">

<h1>MPD-Enhanced: Music Plagiarism Detection with Timbre Embedding</h1>

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

**MPD-Enhanced** builds on the original [Music-Plagiarism-Detection](https://github.com/Mippia/Music-Plagiarism-Detection) (MPD) pipeline by adding **vocal timbre embedding** as an additional similarity dimension for plagiarism detection.

### What's New

- **Vocal timbre embedding** (SpeechBrain ECAPA-TDNN, 192-dim) extracted from the separated vocal track
- Timbre cosine similarity fused into the existing chroma-based matching score:
  ```
  final_score = chroma_similarity × (1.0 + 0.15 × (timbre_cos_sim - 0.5))
  ```
  - Same vocal timbre: +7.5% boost
  - Different vocal timbre: -7.5% penalty  
  - No embedding available (legacy data): neutral (factor = 1.0)
- Fully backward-compatible with existing covers80 JSON files

### Original Features (preserved)

- **Demucs** audio source separation (vocals, piano, drums, bass, other)
- **Beat-Transformer** for beat/downbeat tracking
- **AST** (EfficientNet-b0) for vocal-to-MIDI transcription
- **Segment-based matching** — 4-bar window comparison using chroma features
- Covers80 dataset (164 songs) as the reference library

## Pipeline

```
Input Audio (.wav/.mp3)
  │
  ├─ Demucs → vocal / piano / drums / bass / other
  │
  ├─ Beat-Transformer → beat_times, downbeats, BPM
  │
  ├─ AST → MIDI notes (pitch + timing)
  │
  ├─ ECAPA-TDNN → 192-dim timbre embedding (NEW)
  │
  └─ Compare → chroma similarity × timbre boost → Top 3 matches
```

## Usage

```bash
# Transcribe and compare a song against the covers80 library
python inference.py /path/to/song.wav
```

This generates:
1. A `<song>.json` transcription file (with `vocal_embedding` field)
2. Top 3 plagiarism matches with similarity scores

## Dataset

### SMP Dataset
The original SMP (Segment-based Music Plagiarism) dataset contains 175 segment pair annotations (99 plag + 76 remake) across 72 song pairs.

### covers80 Library
164 pre-transcribed songs used as the reference comparison database.

## Installation

```bash
# Python 3.9+ required (madmom compatibility)
pip install -r requirements.txt

# Additional: timbre embedding
pip install speechbrain
```

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
