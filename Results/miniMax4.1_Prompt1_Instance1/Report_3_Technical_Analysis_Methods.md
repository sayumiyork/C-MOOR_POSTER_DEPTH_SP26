# Report 3: Technical Analysis Methods
## C-MOOR Genomic Data Science Training — Poster Thematic Analysis

---

## 1. Project Overview

This report documents the analytical methodology used to perform a thematic analysis of 27 student research posters from the C-MOOR (Collaborative Mechanism for Outstanding Research) genomic data science training program. The analysis addressed two classification tasks:

1. **Research Focus Category** — a topical classification of the primary scientific domain
2. **Disease-State Classification** — whether and how the poster engages with human disease states

---

## 2. Source Data

- **Total posters analyzed:** 27
- **Source directory:** `/home/workspace/Documents/OCR 1.1/Raw/`
- **File format:** Plain-text (.txt), extracted via OCR from poster PDFs
- **OCR system:** C-MOOR poster OCR pipeline
- **Posters spanning cohorts:** 2022–2025 (CCC, COD, LU programs)

---

## 3. Analytical Approach

### 3.1 Preprocessing

Each poster text file was loaded as raw UTF-8 text. All 27 files were processed as independent documents. No stemming, stopword removal, or lemmatization was applied — matching was performed on the full original text (case-insensitively) to preserve contextual fidelity.

### 3.2 Research Focus Classification

Posters were assigned to one of six Research Focus Categories using a **two-phase rule-based method**:

**Phase 1 — Poster-specific overrides:** For each poster, the label, title, and abstract were reviewed, and a manual assignment was recorded based on the poster's stated research question and primary scientific domain.

**Phase 2 — Keyword scoring (for any remaining unclassified):** Each category was defined by an expert-curated keyword set (listed below). A poster was assigned to the category with the highest keyword match count.

Six Research Focus Categories were defined:

| Category | Key Indicators |
|---|---|
| Neuroscience / Neurobiology | Brain regions (PFC, striatum, hippocampus); neurotransmitter receptors (serotonin, dopamine, GABA); neurodevelopmental genes (MECP2, BDNF); sleep/circadian pathways |
| Gastrointestinal / Digestive | Midgut copper cell; V-ATPase; acid reflux/GERD; digestive enzymes (amylase, trehalase, maltase); H. pylori; fatty acid oxidation; microbiome |
| Cancer / Oncology | KRAS/Ras85D; BRCA2; APC; tumor suppressors; mismatch repair genes; colorectal cancer |
| Metabolism / Metabolics | Mitochondria; NAD+/NADH; peroxisome; fatty acid oxidation (ACOX3); SCP2/SCPx gene family; Zellweger spectrum |
| Immunology / Host Defense | Toll pathway; IMD; JAK/STAT; cGAS-STING; TNFα/Eiger; Hippo; antimicrobial peptides |
| Cell Biology / Cellular Processes | CDC42/aPKC cell polarity; paralog analysis; gene families; ribosome biogenesis; epithelial polarity |

### 3.3 Disease-State Classification

Posters were assigned to one of seven Disease-State buckets:

1. **Neuropsychiatric / Mental Health** — autism (ASD), depression, anxiety, schizophrenia, sleep disorders, Rett syndrome, Parkinson's disease (CNS aspects)
2. **Neurological (Non-Psychiatric)** — neurodegenerative diseases with primarily motor phenotypes (Alzheimer's, Parkinson's motor, Huntington's, ALS, MS, epilepsy)
3. **Gastrointestinal / Digestive** — GERD/acid reflux, peptic ulcer disease, H. pylori infection, IBD
4. **Oncological / Cancer** — any cancer type
5. **Metabolic Disorders (Broad)** — diabetes, fatty acid oxidation disorders (MCADD), metabolic syndrome, Zellweger spectrum, thyroid disorders
6. **Lysosomal Storage / Peroxisomal** — peroxisomal biogenesis disorders, Zellweger syndrome, adrenoleukodystrophy
7. **Basic Biology / No Specific Disease State** — mechanistic biology studies without explicit disease framing

Assignment was performed via **poster-specific overrides** for all 27 posters, based on review of the title, abstract, and stated research motivation. Where a poster mentioned multiple disease areas, the category with greater thematic weight in the poster's stated motivation was selected. This approach was chosen over automated keyword scoring because disease-related terms (e.g., "nervous system," "neuron," "midgut") appear in many basic biology posters by necessity, which caused false-positive disease classifications in automated approaches.

---

## 4. Large Language Model Information

- **Model:** MiniMax 2.7 (via Zo Computer AI platform)
- **Mode:** Interactive chat session for thematic coding, rule definition, and report generation
- **Context:** 27 full poster OCR texts were loaded into the conversation context for analysis
- **Session date:** 2026-04-28

---

## 5. Software and Tools

| Tool | Version / Notes |
|---|---|
| Python | 3.12 (scripted analysis and report generation) |
| Operating System | Debian GNU/Linux 12 (bookworm) |
| Zo Computer | Latest (AI platform hosting this analysis) |
| Pandoc | Available for document format conversion |
| FFmpeg | Available for media processing (not used in this analysis) |

---

## 6. Output Files

All three reports were generated programmatically and saved to:

`/home/workspace/Documents/OCR 1.1/Thematic Analysis Reports/`

| Report | Filename |
|---|---|
| Report 1 | `Report_1_Research_Focus_and_Disease_State_Classifications.md` |
| Report 2 | `Report_2_Disease_State_Categories_Detailed_Breakdown.md` |
| Report 3 | `Report_3_Technical_Analysis_Methods.md` |

---

## 7. Classification Criteria Summary

### Research Focus Categories

| Category | Key Indicators |
|---|---|
| Neuroscience / Neurobiology | Brain regions (PFC, striatum); neurotransmitter receptors (HTR1A, HTR2A, DRD2, GABA); neurodevelopmental genes (MECP2, BDNF); sleep/circadian genes; gut-microbiome-brain axis |
| Gastrointestinal / Digestive | Copper cell region; V-ATPase; trehalose/amylase/maltase; acid reflux; H. pylori; fatty acid oxidation genes; microbiome |
| Cancer / Oncology | KRAS/Ras85D; BRCA2; APC; mismatch repair; cell proliferation |
| Metabolism / Metabolics | Mitochondria; NAD+/NADH; peroxisome; fatty acid oxidation; SCP2/SCPx; ACOX3; Zellweger |
| Immunology / Host Defense | Toll, IMD, JAK/STAT, cGAS-STING, TNFα, Hippo pathways; antimicrobial peptides |
| Cell Biology / Cellular Processes | CDC42/aPKC polarity; paralog analysis; gene families; ribosome biogenesis |

### Disease-State Buckets

| Bucket | Key Indicators |
|---|---|
| Neuropsychiatric / Mental Health | ASD, depression, anxiety, schizophrenia, Rett syndrome, sleep disorders, serotonergic signaling, Parkinson's (CNS) |
| Neurological (Non-Psychiatric) | Alzheimer's, Parkinson's (motor), Huntington's, ALS, MS, epilepsy |
| Gastrointestinal / Digestive | Acid reflux, GERD, peptic ulcer, H. pylori, IBD |
| Oncological / Cancer | Any cancer; KRAS mutation; colorectal cancer |
| Metabolic Disorders (Broad) | Diabetes, MCADD, fatty acid oxidation disorders, Zellweger, thyroid disorders |
| Lysosomal Storage / Peroxisomal | Peroxisomal biogenesis; Zellweger; adrenoleukodystrophy |
| Basic Biology / No Specific Disease State | Mechanistic biology; model organism studies without explicit disease framing |

---

*Report generated: 2026-04-28 | MiniMax 2.7 via Zo Computer | C-MOOR Poster Study*
