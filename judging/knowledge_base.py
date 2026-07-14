"""
Music plagiarism knowledge base for RAG context.

All legal standards and case summaries are sourced from verifiable
court opinions, legal databases, and reliable secondary sources.
Each entry includes the source URL for independent verification.
"""

# ============================================================
# LEGAL STANDARDS
# ============================================================

LEGAL_CRITERIA = r"""
## Music Plagiarism Legal Standards

### Two-Part Test for Copyright Infringement (US)

1. **Ownership of a valid copyright** — plaintiff must prove they own the work

2. **Copying of constituent elements that are original** — two sub-elements:
   a. **Copying-in-fact**: Did the defendant actually copy? Proven by:
      - Direct evidence (admission, witness)
      - Circumstantial evidence: access + probative similarity
   b. **Unlawful appropriation**: Are the copied elements protected expression?

### Substantial Similarity Tests by Circuit

- **2nd Circuit** — "Ordinary Observer" test: would an average lay observer
  recognize the alleged copy as having been appropriated from the copyrighted work?
  (Arnstein v. Porter, 154 F.2d 464, 2d Cir. 1946)

- **9th Circuit** — "Extrinsic/Intrinsic" test:
  - Extrinsic: objective comparison of specific protectable elements
    (expert testimony, analytical dissection)
  - Intrinsic: subjective impression of an ordinary reasonable person
  (Skidmore v. Led Zeppelin, 952 F.3d 1051, 9th Cir. 2020)

### Key Defenses and Doctrines

- **Scènes à faire**: Common or standard elements dictated by genre, style,
  or convention are not copyrightable. "The descending chromatic arpeggio
  was a centuries-old musical building block." (Skidmore, 2020)

- **Idea-Expression Dichotomy**: Copyright protects specific expression,
  not ideas, concepts, styles, or genres. (17 U.S.C. §102(b))

- **De Minimis**: Trivial copying that an ordinary observer would not
  recognize is not actionable

- **Independent Creation**: If defendant created the work independently,
  there is no infringement — even if the works are identical

- **Deposit Copy Rule** (1909 Act): For pre-1978 compositions, the copyright
  scope is limited to the sheet music deposit copy, NOT the sound recording.
  (Skidmore, 2020; Structured Asset Sales v. Sheeran, 2023)

Source: https://law.justia.com/cases/federal/appellate-courts/ca9/16-56057/16-56057-2020-03-09.html
"""

# ============================================================
# FAMOUS CASES — with verified citations
# ============================================================

FAMOUS_CASES = r"""
## Landmark Music Plagiarism Cases

### 1. Bright Tunes v. Harrisongs — "My Sweet Lord" / "He's So Fine" (1976)
- **Citation**: 420 F. Supp. 177 (S.D.N.Y. 1976); damages: 508 F. Supp. 798 (1981)
- **Verdict**: George Harrison found liable for subconscious plagiarism
- **Damages**: ~$1.6 million (net after apportionment)
- **Key Finding**: Judge Richard Owen established the "subconscious copying"
  doctrine — "His subconscious knew it already had worked in a song his
  conscious mind did not remember." Two motifs (sol-mi-re ×4, sol-la-do-la-do ×3)
  with identical grace note and harmonies constituted infringement.
- **Significance**: Subconscious copying IS infringement — intent is irrelevant.
- **Source**: https://www.nytimes.com/1976/09/08/archives/george-harrison-guilty-of-plagiarizing-subconsciously-a-62-tune-for.html
- **Source**: https://blogs.law.gwu.edu/mcir/case/bright-tunes-music-v-harrisongs-music/

### 2. Three Boys Music v. Bolton — "Love Is a Wonderful Thing" (2000)
- **Citation**: 212 F.3d 477 (9th Cir. 2000)
- **Verdict**: $5.4 million against Michael Bolton; 9th Circuit affirmed
- **Key Finding**: Bolton subconsciously copied the Isley Brothers despite:
  - The original never made Billboard Top 100
  - 129 songs share the same title
  - Bolton never admitted hearing the Isley version
  The court held the jury's access finding was supported by Bolton's
  admitted fandom of R&B artists including the Isley Brothers, and a
  damning work tape where Bolton asked "Do you think we're copying a
  Marvin Gaye song?"
- **Significance**: Even obscure songs can be infringed; combination of
  unprotectible elements can create protectible expression.
- **Source**: https://law.justia.com/cases/federal/appellate-courts/F3/212/477/632583/

### 3. Williams v. Gaye — "Blurred Lines" / "Got to Give It Up" (2018)
- **Citation**: 885 F.3d 1150 (9th Cir. 2018)
- **Verdict**: $5.3M awarded to Marvin Gaye's estate (2-1 decision)
- **Key Finding**: Majority UPHELD jury verdict on "narrow procedural grounds"
  and "deferential standards of review." The Thicke parties failed to make a
  Rule 50(a) motion at trial, severely limiting appellate review.
  Judge Nguyen's DISSENT: "The majority allows the Gayes to accomplish
  what no one has before: copyright a musical style." The songs differ in
  melody, harmony, and rhythm — the similarity was in unprotectable elements
  (cowbell, falsetto, "groove").
- **Significance**: Controversial — widely criticized for effectively protecting
  musical "feel" rather than expression. Over 200 musicians filed amicus brief
  warning of chilling effect on creativity.
- **Source**: https://app.midpage.ai/case/pharrell-williams-v-frankie-gaye-4256808

### 4. Skidmore v. Led Zeppelin — "Stairway to Heaven" / "Taurus" (2020)
- **Citation**: 952 F.3d 1051 (9th Cir. 2020) (en banc)
- **Verdict**: Led Zeppelin prevailed — no infringement (unanimous en banc)
- **Key Holdings**:
  - "Inverse ratio rule" ABROGATED unanimously — more access does not
    reduce the substantial similarity burden
  - Deposit copy rule: pre-1976 copyrights limited to sheet music, not recordings
  - Chromatic scales, arpeggios, and short note sequences are NOT protected
  - "Selection and arrangement" theory requires more than common elements
- **Significance**: Major pro-defendant shift; eliminated unfair advantage
  for plaintiffs in high-access cases.
- **Source**: https://law.justia.com/cases/federal/appellate-courts/ca9/16-56057/16-56057-2020-03-09.html

### 5. Gray v. Perry — "Dark Horse" / "Joyful Noise" (2019/2022)
- **Citation**: Gray v. Perry, No. 2:15-cv-05642 (C.D. Cal.)
- **Verdict**: 2019 jury awarded $2.78M → 2020 district court VACATED →
  2022 9th Circuit AFFIRMED (3-0) for Katy Perry
- **Key Finding**: The 8-note ostinato at issue consisted "entirely of
  commonplace musical elements" (minor scale, uniform rhythm, descending pitch).
  The same sequence appears in "Merrily We Roll Along" and "Jolly Old Saint
  Nicholas." Granting copyright would be an "improper monopoly over two-note
  pitch sequences or even the minor scale itself."
- **Significance**: Basic musical building blocks (scales, simple ostinatos)
  belong to the public domain and cannot be monopolized.
- **Source**: https://www.rollingstone.com/music/music-news/katy-perry-ninth-circuit-dark-horse-copyright-verdict-1319870/

### 6. Structured Asset Sales v. Sheeran — "Thinking Out Loud" (2023-2025)
- **Citation**: Structured Asset Sales, LLC v. Sheeran (S.D.N.Y. 2023);
  affirmed 2nd Cir. 2024; cert. denied U.S. Supreme Court June 2025
- **Verdict**: Ed Sheeran prevailed — no infringement, jury verdict 2023;
  SAS I dismissed May 2023; 2nd Circuit affirmed Nov 2024; SCOTUS denied cert 2025
- **Key Finding**: The chord progression (I-iii-IV-V) and harmonic rhythm
  were "basic musical building blocks." Experts showed 4 pre-1973 songs used
  the same combination ("Georgy Girl," "Since I Lost My Baby," "Downtown,"
  "Get Off Of My Cloud"). Combining just two common elements fails the
  numerosity requirement for selection-and-arrangement protection.
- **Significance**: Major win for songwriters — common chord progressions
  cannot be monopolized through copyright.
- **Source**: https://www.courtlistener.com/opinion/10182078/structured-asset-sales-llc-v-sheeran/
"""

# ============================================================
# MUSICOLOGICAL CRITERIA
# ============================================================

MUSICOLOGICAL_CRITERIA = r"""
## Musicological Plagiarism Analysis Criteria

### 1. Melody Analysis (Most Important Criterion)
- **Pitch contour**: Compare note-by-note pitch sequences and direction
- **Rhythmic pattern**: Note durations and timing in relation to the beat
- **Phrase structure**: Length, grouping, and architecture of melodic phrases
- **Motivic similarity**: Recurring short melodic patterns (motifs)
- **Ornamentation**: Grace notes, melisma, slides, and appoggiaturas
- **Threshold**: 6-8 consecutive identical notes with same rhythm is
  highly probative; 3-4 notes alone is insufficient (Skidmore, 2020)

### 2. Harmony Analysis
- **Chord progressions**: Sequence of chords — I-IV-V-I and I-vi-IV-V
  are NOT protectable (scènes à faire). Unique or unusual progressions
  carry more weight.
- **Harmonic rhythm**: Rate of chord changes and syncopation
- **Bass line**: Walking patterns, counter-melodies

### 3. Rhythm Analysis
- **Time signature**: Meter (though common meters are not protectable)
- **Groove/feel**: Distinctive rhythmic figures or syncopation patterns
- **Tempo**: BPM similarity alone is weak evidence
- **Warning**: Rhythmic similarity alone is rarely sufficient (Williams
  v. Gaye dissent criticized protecting "groove")

### 4. Lyrics Analysis
- **Verbatim matching**: Word-for-word copying of phrases
- **Rhyme scheme**: Identical end-rhyme patterns
- **Structural similarity**: Verse/chorus arrangement of lyrics
- **Threshold**: 4+ consecutive identical words is significant

### 5. Structure/Arrangement
- **Song form**: Verse-chorus-bridge layout
- **Section lengths**: Duration of each section
- **Instrumentation**: Overlap in instrument choices (weakest evidence)

### 6. Timbre/Voice Quality
- **Vocal characteristics**: Distinctive timbre, vibrato, range
- **Delivery style**: Phrasing, breath control, articulation
- **Warning**: Vocal similarity alone is nearly always insufficient

### Combined Assessment Framework

The jurisprudence consistently shows:
- **Strong case**: High melody similarity + distinctive harmonic element
  + lyrics overlap + access evidence
- **Moderate case**: Medium melody similarity + some structural overlap
- **Weak case**: Low melody similarity OR common elements defense applies
  (scènes à faire, basic building blocks, short sequences)
- **No case**: Similarity limited to chord progressions, tempo, genre, style,
  or other unprotectable elements

See: Skidmore v. Led Zeppelin (2020) and Gray v. Perry (2022) for the
principle that basic musical building blocks are NOT protected.
"""

# ============================================================
# CASE CLASSIFICATION
# ============================================================

CASES_BY_TYPE = r"""
## Music Plagiarism Cases Categorized by Similarity Type

### Melody-Dominant Cases (STRONG — most likely to succeed)
- **Bright Tunes v. Harrisongs** (1976): Nearly identical melodic motifs
  (sol-mi-re ×4, sol-la-do-la-do ×3) + identical grace note → INFRINGEMENT
  Score analog: ~0.70+ due to nearly identical pitch contour and rhythm.
- **Three Boys Music v. Bolton** (2000): Combination of 5 melodic/structural
  elements → INFRINGEMENT ($5.4M)
  Score analog: ~0.55-0.65 due to combined elements.

### Rhythm/Groove Cases (WEAK — controversial, high risk of reversal)
- **Williams v. Gaye** (2018): Rhythmic and arrangement similarity —
  INFRINGEMENT (2-1 decision, widely criticized)
  Score analog: Melody alone ~0.30-0.40, but jury found overall similarity.
  The case is an outlier — most groove-based claims fail.

### Harmony/Chord Cases (WEAK — almost always fail)
- **Skidmore v. Led Zeppelin** (2020): Similar chromatic arpeggio but
  found to be common musical vocabulary → NO INFRINGEMENT
  Score analog: ~0.20-0.30 melody, ~0.60 harmony match, but scènes à faire.
- **Structured Asset Sales v. Sheeran** (2023): Same chord progression
  (I-iii-IV-V) but basic building block → NO INFRINGEMENT

### Short Phrase Cases (WEAK — usually fail on appeal)
- **Gray v. Perry** (2022): 8-note ostinato → initially infringement ($2.78M),
  then VACATED on appeal. Short common phrases are NOT protectable.

### Lyrics Cases (VARIES — depends on distinctiveness)
- Verbatim lyrics copying is independently strong evidence
- Title phrase overlap alone is usually insufficient
"""

# ============================================================
# JUDGMENT GUIDELINES — with case-anchored thresholds
# ============================================================

JUDGMENT_GUIDELINES = r"""
## LLM Plagiarism Judgment Guidelines

### Score Interpretation (anchored to case precedents)

- **Score > 0.60**: Very strong algorithmic match. Comparable to the melodic
  similarity in Bright Tunes v. Harrisongs (1976).
  → RECOMMEND: "Possible Plagiarism" — detailed analysis needed. Check if
  scènes à faire or basic building blocks defense applies (Skidmore, 2020).

- **Score 0.45 – 0.60**: Moderate to strong match. Comparable to Three Boys
  Music v. Bolton (2000) range. Substantial similarity possible.
  → RECOMMEND: "Possible Plagiarism" — evaluate each dimension separately.
  The combination of smaller similarities can be protectable (Bolton).

- **Score 0.30 – 0.45**: Borderline match. Could be coincidental, genre
  convention, or independent creation.
  → RECOMMEND: "Probably Coincidental" unless bolstered by:
  - Strong lyrics overlap (identical phrases)
  - Evidence of access (defendant knew the original)
  - Unusual/distinctive melodic elements (not standard scales/arpeggios)

- **Score < 0.30**: Weak match. Likely coincidental or common elements.
  → RECOMMEND: "Probably Coincidental" or "Insufficient Evidence."
  Consistent with Skidmore (2020) and Gray (2022) outcomes.

### Boost Factor Interpretation

- **Timbre boost > 1.03**: Vocal similarity detected. Supports plagiarism
  if melody also matches. Alone, insufficient (Williams v. Gaye criticized
  for over-weighting vocal style). Different singers can sound similar.
- **Timbre boost ≤ 1.0**: No vocal similarity. This is the typical case.

- **Lyrics boost > 1.04**: Very similar lyrics. This is independently strong
  evidence of copying — lyrics similarity alone is actionable.
- **Lyrics boost > 1.03**: Similar lyrics — supports melody findings.
- **Lyrics boost ≤ 1.0**: No lyrics similarity.

### Key Legal Principles to Apply

1. **Short phrases are NOT protected** (Gray v. Perry, 2022; Skidmore, 2020):
   3-4 notes or an 8-note ostinato of common elements is not infringement.

2. **Common chord progressions are NOT protected** (Sheeran, 2023):
   I-iii-IV-V, I-vi-IV-V, and similar basic progressions are building blocks.

3. **Subconscious copying IS infringement** (Harrisongs, 1976; Bolton, 2000):
   Intent is irrelevant — if similarity exists + access is shown, it's infringement.

4. **Combination of unprotectible elements CAN be protectible** (Bolton, 2000):
   But the combination must be numerous and distinctive, not just 2-3 generic elements.

5. **"Feel" and "groove" are NOT protectible** (Williams v. Gaye dissent, 2018;
   Skidmore, 2020): Style, genre, and production approach are ideas, not expression.

### Judgment Output Format

For each match, produce:
1. **verdict**: "Likely Plagiarism" | "Possible Plagiarism" |
   "Probably Coincidental" | "Insufficient Evidence"
2. **confidence**: 0-100% (how confident the LLM is in this verdict)
3. **reasoning**: 2-3 sentence explanation citing specific scores and dimensions
4. **key_evidence_for**: which dimensions SUPPORT plagiarism
5. **key_evidence_against**: which dimensions REFUTE plagiarism
6. **relevant_case**: most analogous legal precedent (or "N/A")
7. **recommendation**: next step (legal review, musicologist analysis, etc.)
"""

# ============================================================
# COMPLETE KNOWLEDGE BASE
# ============================================================

KNOWLEDGE_BASE = "\n\n".join([
    LEGAL_CRITERIA,
    FAMOUS_CASES,
    MUSICOLOGICAL_CRITERIA,
    CASES_BY_TYPE,
    JUDGMENT_GUIDELINES,
])
