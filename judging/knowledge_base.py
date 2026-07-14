"""
Music plagiarism knowledge base for RAG context.

Contains legal standards, famous cases, and musicological criteria
used as reference when the LLM judges potential plagiarism.
"""

# ============================================================
# LEGAL STANDARDS
# ============================================================

LEGAL_CRITERIA = r"""
## Music Plagiarism Legal Standards

### Two-Part Test (US Copyright Law)
1. **Access**: The defendant must have had access to the original work.
   - Direct access: provable exposure (radio play, sales, live performance)
   - Indirect access: widespread dissemination or chain of access
   - Striking similarity alone can substitute for proving access

2. **Substantial Similarity**: The works must be substantially similar.
   - Ordinary observer test: would an average listener recognize the copying?
   - Extrinsic test: objective analysis of musical elements (melody, harmony, rhythm)
   - Intrinsic test: subjective impression of an ordinary listener
   - De minimis defense: trivial copying is not infringement

### Key Legal Doctrines
- **Scènes à faire**: Common musical elements/techniques are not copyrightable
  (standard chord progressions, basic rhythms, generic arrangements)
- **Idea-Expression Dichotomy**: Musical ideas (genre, style, feel) are not
  protected; only the specific expression is
- **Independent Creation Defense**: If the defendant created the work
  independently without access to the original
- **Fair Use** (17 USC §107): Purpose/character, nature of work, amount used,
  market effect

### Similarity Thresholds (Empirical)
- Score < 0.30: Likely de minimis or coincidental similarity
- Score 0.30 - 0.45: Borderline — requires detailed musicological analysis
- Score 0.45 - 0.60: Substantial similarity possible — melody + structure overlap
- Score > 0.60: Strong evidence of copying — requires access verification
"""

# ============================================================
# FAMOUS CASES
# ============================================================

FAMOUS_CASES = r"""
## Landmark Music Plagiarism Cases

### 1. Williams v. Gaye — "Blurred Lines" (2015)
- **Verdict**: $5.3M awarded to Marvin Gaye's estate (later reduced to $4.98M)
- **Similarity**: "Blurred Lines" vs "Got to Give It Up"
- **Key Finding**: Copied the "feel" and "groove" — not just notes but overall
  character, including bass line, keyboard parts, and vocal style
- **Significance**: Expanded infringement beyond melody to include arrangement,
  rhythm, and production elements
- **Controversy**: Critics argued it protected an unprotectable "style" or "genre"

### 2. Skidmore v. Led Zeppelin — "Stairway to Heaven" (2016)
- **Verdict**: Led Zeppelin prevailed; no infringement found
- **Similarity**: "Stairway to Heaven" vs Spirit's "Taurus"
- **Key Finding**: The descending chromatic arpeggio was a centuries-old musical
  building block (scènes à faire), not original to Spirit
- **Significance**: 9th Circuit en banc ruling clarified scope of copyright
  protection — common musical elements are NOT protected

### 3. Three Boys Music v. Bolton — "Love Is a Wonderful Thing" (2000)
- **Verdict**: $5.4M against Michael Bolton
- **Similarity**: Bolton's "Love Is a Wonderful Thing" vs Isley Brothers' song
- **Key Finding**: Even without direct evidence of access, striking similarity
  combined with circumstantial evidence of access was sufficient

### 4. Selle v. Gibb — "How Deep Is Your Love" (1984)
- **Verdict**: Bee Gees prevailed
- **Similarity**: "How Deep Is Your Love" vs Selle's "Let It End"
- **Key Finding**: Plaintiff failed to prove access; similarity alone was
  insufficient when both songs used common musical elements

### 5. Gray v. Perry — "Dark Horse" (2019)
- **Verdict**: $2.78M against Katy Perry (later overturned on appeal 2022)
- **Similarity**: "Dark Horse" vs Flame's "Joyful Noise"
- **Key Finding**: Initially found infringement based on 8-note ostinato;
  overturned because the musical phrase was too short and common to be protected

### 6. Sheeran v. Gaye/Structured Asset Sales — "Thinking Out Loud" (2023)
- **Verdict**: Ed Sheeran prevailed
- **Similarity**: "Thinking Out Loud" vs "Let's Get It On"
- **Key Finding**: The chord progression (I-iii-IV-V) and harmonic rhythm were
  common building blocks, not unique expression
"""

# ============================================================
# MUSICOLOGICAL CRITERIA
# ============================================================

MUSICOLOGICAL_CRITERIA = r"""
## Musicological Plagiarism Analysis Criteria

### 1. Melody Analysis (Primary Criterion)
- **Pitch sequence**: Compare note-by-note pitch contours
- **Rhythmic pattern**: Compare note durations and timing
- **Melodic contour**: Shape of the melody (rising, falling, arch)
- **Phrase structure**: Length and grouping of melodic phrases
- **Ornamentation**: Melisma, grace notes, slides
- **Threshold**: 6-8 consecutive identical notes is highly probative

### 2. Harmony Analysis
- **Chord progressions**: Sequence of chords (common progressions are NOT protected)
- **Harmonic rhythm**: Rate of chord changes
- **Key/modulation**: Tonal center and key changes
- **Bass line**: Walking patterns, counter-melody
- **Threshold**: Unique chord progressions (not I-IV-V-I) carry more weight

### 3. Rhythm Analysis
- **Time signature**: Meter (4/4, 3/4, 6/8, etc.)
- **Tempo**: BPM similarity (considered weak evidence alone)
- **Groove pattern**: Distinctive rhythmic figures
- **Syncopation**: Off-beat emphasis patterns
- **Threshold**: Rhythmic similarity alone is rarely sufficient

### 4. Lyrics Analysis
- **Word sequence**: Verbatim or near-verbatim matching
- **Rhyme scheme**: Pattern of rhyming words
- **Thematic content**: Subject matter (weakest evidence — idea, not expression)
- **Phrase structure**: Line length, stanza organization
- **Threshold**: Verbatim matches of 4+ words are significant

### 5. Structure/Arrangement
- **Song form**: Verse-chorus-bridge structure
- **Section lengths**: Duration of each section
- **Instrumentation**: Choice and arrangement of instruments
- **Production elements**: Studio effects, mixing style

### 6. Timbre/Voice Quality
- **Vocal characteristics**: Range, timbre, vibrato
- **Delivery style**: Phrasing, breath control, articulation
- **Threshold**: Vocal similarity is rarely independently sufficient
  but supports melody/harmony findings

### Combined Assessment Framework
- **Strong plagiarism**: High melody similarity + high harmony similarity +
  access evidence + lyrics overlap
- **Moderate plagiarism**: Medium melody similarity + some harmony overlap +
  possible access
- **Weak/No plagiarism**: Low similarity across dimensions OR common elements
  (scènes à faire) OR independent creation evidence
"""

# ============================================================
# CASES BY SIMILARITY TYPE
# ============================================================

CASES_BY_TYPE = r"""
## Music Plagiarism Cases Categorized by Similarity Type

### Melody-Dominant Cases
- **"He's So Fine" v. "My Sweet Lord"** (Bright Tunes v. Harrisongs, 1976):
  George Harrison found to have subconsciously copied the melody. Score would
  likely be ~0.70+ due to nearly identical melodic contour and rhythm.
- **"Joyful Noise" v. "Dark Horse"** (Gray v. Perry, 2019/2022):
  8-note ostinato initially found infringing but overturned — too short/common.

### Rhythm/Groove Cases
- **"Got to Give It Up" v. "Blurred Lines"** (Williams v. Gaye, 2015):
  Primarily rhythmic and arrangement similarity. Would score ~0.40-0.50 on
  melody alone, but high on combined groove/timbre/arrangement.

### Harmony/Chord Cases
- **"Taurus" v. "Stairway to Heaven"** (Skidmore v. Led Zeppelin, 2016):
  Similar chromatic arpeggio but found to be common musical vocabulary.
  Melody similarity ~0.20-0.30, harmony ~0.60, BUT common element defense.

### Lyrics + Melody Cases
- **"Love Is a Wonderful Thing"** (Three Boys Music v. Bolton, 2000):
  Combined melody, lyrics, and arrangement similarity. Title phrase identical.

### Timbre/Performance Cases
- **Tom Waits v. Frito-Lay** (1992): Not plagiarism but voice misappropriation —
  distinctive vocal timbre used in commercial. Timbre alone can support findings
  when combined with other factors.
"""

# ============================================================
# JUDGMENT GUIDELINES FOR LLM
# ============================================================

JUDGMENT_GUIDELINES = r"""
## LLM Plagiarism Judgment Guidelines

### Input Data Interpretation
You will receive:
1. **Algorithmic scores** (0-1 scale) for melody matching
2. **Boost factors** indicating timbre similarity and lyrics similarity
3. **Song metadata**: title, BPM, key, detected language
4. **Time alignment**: which segments matched between the two songs

### How to Interpret Scores
- **Score 0.60+**: Very strong algorithmic match. Likely copying of melody/harmony.
  Recommend: DETAILED ANALYSIS — check if scènes à faire applies.
- **Score 0.45-0.60**: Strong match. Substantial similarity possible.
  Recommend: REVIEW WITH CAUTION — evaluate each dimension separately.
- **Score 0.30-0.45**: Moderate match. Could be coincidental or genre similarity.
  Recommend: PROBABLY COINCIDENTAL unless other evidence (access, lyrics).
- **Score < 0.30**: Weak match. Likely coincidental.
  Recommend: NO PLAGIARISM — unless lyrics are identical.

### Boost Factor Interpretation
- **Timbre boost > 1.03**: Vocal similarity detected. Supports plagiarism if
  melody also matches. Alone, not sufficient (different singers can sound alike).
- **Lyrics boost > 1.03**: Lyrics similarity detected. Weight heavily — lyrics
  copying is easier to prove than melody copying.
- **Lyrics boost > 1.04**: Very similar lyrics — this is independently strong
  evidence of copying.

### Judgment Output Format
For each match, produce:
1. **Judgment**: "Likely Plagiarism" / "Possible Plagiarism" /
   "Probably Coincidental" / "Insufficient Evidence"
2. **Confidence**: 0-100%
3. **Reasoning**: 2-3 sentence explanation citing specific dimensions
4. **Key Evidence**: Which dimensions support/refute plagiarism
5. **Recommendation**: Next steps (legal review, musicologist analysis, etc.)
"""

# ============================================================
# COMPLETE KNOWLEDGE BASE (for RAG)
# ============================================================

KNOWLEDGE_BASE = "\n\n".join([
    LEGAL_CRITERIA,
    FAMOUS_CASES,
    MUSICOLOGICAL_CRITERIA,
    CASES_BY_TYPE,
    JUDGMENT_GUIDELINES,
])
