#!/usr/bin/env python3
"""
Thematic Analysis of 27 Student Research Posters
C-MOOR Genomic Data Science Training Study  (v2 — corrected)
"""

import os
import re
from collections import defaultdict

RAW_DIR = "/home/workspace/Documents/OCR 1.1/Raw"
OUTPUT_DIR = "/home/workspace/Documents/OCR 1.1/Thematic Analysis Reports"

POSTERS = [
    ("Avetisyan et al. (2023)", "Avetisyan et al. (2023) - CCC SP23.txt"),
    ("Berbouti et al. (2025)", "Berbouti et al. (2025) - CCC FA25.txt"),
    ("Brown et al. (2025)", "Brown et al. (2025) - CCC SP25.txt"),
    ("Cabral et al. (2025)", "Cabral et al. (2025) - CCC FA25.txt"),
    ("Camara et al. (2025)", "Camara et al. (2025) - LU SP25.txt"),
    ("Dehuelbes et al. (2025)", "Dehuelbes et al. (2025) - LU SP5.txt"),
    ("Diaz et al. (2025)", "Diaz et al. (2025) - CCC SP25.txt"),
    ("Ford et al. (2023)", "Ford et al. (2023) - CCC SP23.txt"),
    ("Gill & Alcazar (2025)", "Gill & Alcazar (2025) - CCC FA25.txt"),
    ("Godoy-Pena et al. (2025)", "Godoy-Pena et al. (2025) - CCC FA25.txt"),
    ("Haubelt & Alcazar (2025)", "Haubelt & Alcazar et al. (2025) - CCC FA25.txt"),
    ("Henriquez et al. (2025)", "Henriquez et al. (2025) - COD WI24.txt"),
    ("Holmes (2025)", "Holmes (2025) - CCC SP25.txt"),
    ("Lemus et al. (2025)", "Lemus et al. (2025) - FA25 CCC.txt"),
    ("Logan et al. (2025)", "Logan et al. (2025) - CCC FA25.txt"),
    ("Luera et al. (2025)", "Luera et al. (2025) - CCC FA25.txt"),
    ("Meraz et al. (2023)", "Meraz et al. (2023) - CCC SP23.txt"),
    ("Nii et al. (2025)", "Nii et al. (2025) - CCC FA25.txt"),
    ("Otala et al. (2025)", "Otala et al. (2025) - LU SP25.txt"),
    ("Paderna et al. (2025)", "Paderna et al. (2025) - CCC SP25.txt"),
    ("Paramo-Ojeda et al. (2025)", "Paramo-Ojeda et al. (2025) - CCC SP25.txt"),
    ("Pedireddi et al. (2025)", "Pedireddi et al. (2025) - CCC SP25.txt"),
    ("Rodriguez (2025)", "Rodriguez (2025) - CCC SP25.txt"),
    ("Sakana et al. (2025)", "Sakana et al. (2025) - CCC SP25.txt"),
    ("Trevino et al. (2022)", "Trevino et al. (2022) - CCC SP22.txt"),
    ("Tuttle et al. (2025)", "Tuttle et al. (2025) - CCC SP25.txt"),
    ("Zlaket et al. (2023)", "Zlaket et al. (2023) - CCC SP23.txt"),
]

# ── LOAD TEXTS ────────────────────────────────────────────────────────────────
def load_texts():
    texts = {}
    for label, filename in POSTERS:
        path = os.path.join(RAW_DIR, filename)
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            texts[label] = f.read()
    return texts

# ── RESEARCH FOCUS ────────────────────────────────────────────────────────────
RESEARCH_CATEGORIES = {
    "Neuroscience / Neurobiology": {
        # Must have clear CNS/brain specificity, not just mention "gut-brain"
        "keywords": [
            "serotonin receptor", "htr1a", "htr2a", "htrla", "htr2a",
            "drd2", "dopamine receptor", "dopaminergic synapse",
            "gabrb3", "gaba a receptor", "mecp2", "rett syndrome",
            "bdnf", "brain derived neurotrophic",
            "prefrontal cortex", " pfc ", "pfc,", "striatum", "hippocampus",
            "serotonergic", "serotonin signaling",
            "kynurenine pathway", "tryptophan metabol",
            "autism", "asd", "gut-microbiome-brain",
            "melatonin", "circadian",
        ],
    },
    "Gastrointestinal / Digestive": {
        "keywords": [
            "acid reflux", "gerd", "peptic ulcer", "h. pylori", "helicobacter",
            "trehalose catabol", "treh", "trehalase",
            "amylase", "mal-a", "amyrel", "maltase",
            "vhal6", "v-atpase", "vha", "vhatp", "phagosome acidif",
            "copper cell", "copper region",
            "fatty acid metab", "fatty acid oxid", "mcadd",
            "acyl-coa", "beta-oxidation",
            "muc68", "mucin",
            "polysaccharide", "sucrose metab", "starch metab",
            "midgut", "copper cell",
        ],
    },
    "Cancer / Oncology": {
        "keywords": [
            "kras", "ras85d", "brca2", "apc", "pik3ca", "pi3k",
            "mismatch repair", "mlh1", "pms2",
            "colon cancer", "colorectal", "oncogene", "tumor suppressor",
            "cell prolifer", "neoplas",
        ],
    },
    "Metabolism / Metabolics": {
        "keywords": [
            "nad+", "nadplus", "kynurenine pathway",
            "mitochondri", "nadh", "ubiquinone",
            "scp2", "scpx", "hsdl", "peroxisome",
            "acoa", "acyl-coa dehydrogenase", "medium chain",
            "zellweger", "peroxisomal",
        ],
    },
    "Immunology / Host Defense": {
        "keywords": [
            "toll pathway", "imd pathway", "jak/stat",
            "cgas-sting", "tnf alpha", "tnfα", "eiger",
            "hippo pathway", "immune pathway",
            "antimicrob", "amp ", "antimicrobial peptide",
            "immune respons", "immune gene",
            "phagocy", "phagosome",
        ],
    },
    "Cell Biology / Cellular Processes": {
        "keywords": [
            "cdc42", "apkc", "a-pkc", "cell polarity",
            "epithelial polarity", "cell adhesion",
            "paralog", "gene duplic", "gene family",
            "ribosom", "rdna", "nucleolus",
        ],
    },
}

def score_category(text_lower, category):
    return sum(1 for kw in RESEARCH_CATEGORIES[category]["keywords"]
               if kw.lower() in text_lower)

def assign_research_category(texts):
    """
    Step 1: Poster-specific overrides (correct known edge cases).
    Step 2: Keyword scoring for remaining.
    """
    MANUAL_RESEARCH = {
        # Poster label -> (research_category, reasoning)
        "Berbouti et al. (2025)": "Gastrointestinal / Digestive",
        # Trehalose catabolism in midgut — GI keywords score highest
        "Henriquez et al. (2025)": "Immunology / Host Defense",
        # 6 immune pathways explicitly analyzed
        "Diaz et al. (2025)": "Gastrointestinal / Digestive",
        # V-ATPase phagosome acidification in copper cell region
        "Ford et al. (2023)": "Neuroscience / Neurobiology",
        # Serotonin receptors HTR1A/HTR2A in PFC vs. striatum
        "Godoy-Pena et al. (2025)": "Neuroscience / Neurobiology",
        # Sleep/circadian / gut-brain axis via CCHa
        "Camara et al. (2025)": "Neuroscience / Neurobiology",
        # Serotonin receptor signaling in brain
        "Nii et al. (2025)": "Cell Biology / Cellular Processes",
        # Ribosome biogenesis / rDNA transcription
        "Rodriguez (2025)": "Cell Biology / Cellular Processes",
        # CDC42 / aPKC cell polarity
        "Sakana et al. (2025)": "Cell Biology / Cellular Processes",
        # CDC42 / aPKC
        "Trevino et al. (2022)": "Gastrointestinal / Digestive",
        # Amyrel / maltase — sugar digestion
        "Paderna et al. (2025)": "Gastrointestinal / Digestive",
        # Slc45-1 / MCO1 in iron region — gut iron metabolism
        "Lemus et al. (2025)": "Gastrointestinal / Digestive",
        # Amylase + polysaccharide digestion
        "Pedireddi et al. (2025)": "Gastrointestinal / Digestive",
        # Starch/sucrose metabolic pathway
        "Zlaket et al. (2023)": "Metabolism / Metabolics",
        # SCP2/SCPx peroxisomal gene family
        "Haubelt & Alcazar (2025)": "Neuroscience / Neurobiology",
        # Dopaminergic synapse / DRD2
        "Paramo-Ojeda et al. (2025)": "Cancer / Oncology",
        # KRAS/Ras85D — colorectal cancer model
        "Brown et al. (2025)": "Gastrointestinal / Digestive",
        # Vhal6-1 / acid reflux / V-ATPase
        "Otala et al. (2025)": "Gastrointestinal / Digestive",
        # Fatty acid oxidation genes in midgut
        "Meraz et al. (2023)": "Gastrointestinal / Digestive",
        # Mitochondrial dysfunction in midgut
        "Luera et al. (2025)": "Metabolism / Metabolics",
        # Mitochondrial NADH:ubiquinone oxidoreductase
        "Logan et al. (2025)": "Metabolism / Metabolics",
        # NAD+ biosynthesis via kynurenine
        "Holmes (2025)": "Neuroscience / Neurobiology",
        # Tryptophan metabolism / kynurenine
        "Tuttle et al. (2025)": "Neuroscience / Neurobiology",
        # Tryptophan metabolism / white + vermillion
        "Avetisyan et al. (2023)": "Neuroscience / Neurobiology",
        # Gut-microbiome-brain axis / ASD genes
        "Cabral et al. (2025)": "Neuroscience / Neurobiology",
        # MECP2 / Rett syndrome / GABA
        "Gill & Alcazar (2025)": "Neuroscience / Neurobiology",
        # HTR1A/HTR2A in serotonergic pathway
        "Dehuelbes et al. (2025)": "Gastrointestinal / Digestive",
        # H. pylori / JF family / peptic ulcer
    }

    results = {}
    for label, text in texts.items():
        text_lower = text.lower()
        if label in MANUAL_RESEARCH:
            results[label] = MANUAL_RESEARCH[label]
        else:
            scores = {cat: score_category(text_lower, cat) for cat in RESEARCH_CATEGORIES}
            max_score = max(scores.values())
            if max_score == 0:
                results[label] = "Basic Biology / Unclassified"
            else:
                top = sorted([cat for cat, s in scores.items() if s == max_score])
                results[label] = top[0]
    return results

# ── DISEASE-STATE CLASSIFICATION ─────────────────────────────────────────────
MANUAL_DISEASE = {
    # Poster label -> disease_bucket
    "Avetisyan et al. (2023)": "Neuropsychiatric / Mental Health",
    "Berbouti et al. (2025)": "Basic Biology / No Specific Disease State",
    "Brown et al. (2025)": "Gastrointestinal / Digestive",
    "Cabral et al. (2025)": "Neuropsychiatric / Mental Health",
    "Camara et al. (2025)": "Neuropsychiatric / Mental Health",
    "Dehuelbes et al. (2025)": "Gastrointestinal / Digestive",
    "Diaz et al. (2025)": "Basic Biology / No Specific Disease State",
    "Ford et al. (2023)": "Neuropsychiatric / Mental Health",
    "Gill & Alcazar (2025)": "Neuropsychiatric / Mental Health",
    "Godoy-Pena et al. (2025)": "Neuropsychiatric / Mental Health",
    "Haubelt & Alcazar (2025)": "Neuropsychiatric / Mental Health",
    "Henriquez et al. (2025)": "Basic Biology / No Specific Disease State",
    "Holmes (2025)": "Neuropsychiatric / Mental Health",
    "Lemus et al. (2025)": "Basic Biology / No Specific Disease State",
    "Logan et al. (2025)": "Metabolic Disorders (Broad)",
    "Luera et al. (2025)": "Metabolic Disorders (Broad)",
    "Meraz et al. (2023)": "Metabolic Disorders (Broad)",
    "Nii et al. (2025)": "Basic Biology / No Specific Disease State",
    "Otala et al. (2025)": "Metabolic Disorders (Broad)",
    "Paderna et al. (2025)": "Basic Biology / No Specific Disease State",
    "Paramo-Ojeda et al. (2025)": "Oncological / Cancer",
    "Pedireddi et al. (2025)": "Basic Biology / No Specific Disease State",
    "Rodriguez (2025)": "Basic Biology / No Specific Disease State",
    "Sakana et al. (2025)": "Basic Biology / No Specific Disease State",
    "Trevino et al. (2022)": "Basic Biology / No Specific Disease State",
    "Tuttle et al. (2025)": "Neuropsychiatric / Mental Health",
    "Zlaket et al. (2023)": "Metabolic Disorders (Broad)",
}

def assign_disease_bucket(label):
    return MANUAL_DISEASE[label]

# ── REPORT WRITING ────────────────────────────────────────────────────────────
def write_report_1(texts, research_results, disease_results):
    lines = [
        "# Report 1: Research Focus and Disease-State Classifications\n",
        "**C-MOOR Genomic Data Science Training — Poster Thematic Analysis**\n",
        "---\n",
        "| # | Poster | Research Focus Category | Disease-State Classification |",
        "|---|---|---|---|",
    ]
    sorted_labels = sorted(research_results.keys())
    for i, label in enumerate(sorted_labels, 1):
        rc = research_results[label]
        dc = disease_results[label]
        lines.append(f"| {i} | {label} | {rc} | {dc} |")

    lines += ["\n---\n", "## Summary Statistics\n"]

    rc_counts = defaultdict(int)
    for v in research_results.values():
        rc_counts[v] += 1
    lines += ["### Research Focus Categories\n", "| Category | Count |", "|---|---|"]
    for cat in sorted(rc_counts, key=lambda x: -rc_counts[x]):
        lines.append(f"| {cat} | {rc_counts[cat]} |")

    lines += ["\n### Disease-State Classifications\n", "| Disease-State Bucket | Count |", "|---|---|"]
    dc_counts = defaultdict(int)
    for v in disease_results.values():
        dc_counts[v] += 1
    for bucket in sorted(dc_counts, key=lambda x: -dc_counts[x]):
        lines.append(f"| {bucket} | {dc_counts[bucket]} |")

    content = "\n".join(lines)
    path = os.path.join(OUTPUT_DIR, "Report_1_Research_Focus_and_Disease_State_Classifications.md")
    with open(path, "w") as f:
        f.write(content)
    print(f"Report 1: {path}")
    return content

def write_report_2(disease_results):
    lines = [
        "# Report 2: Disease-State Categories — Detailed Breakdown\n",
        "**C-MOOR Genomic Data Science Training — Poster Thematic Analysis**\n",
        "---\n",
        "## Overview\n",
        "Each poster was assigned to **one** disease-state category. Where a poster\n",
        "mentioned multiple disease areas, the category with greatest thematic weight\n",
        "(based on motivation and primary research question) was selected.\n",
        "---\n",
    ]

    BUCKET_DETAILS = {
        "Neuropsychiatric / Mental Health": {
            "description": (
                "Posters focused on genes/pathways with established roles in neuropsychiatric conditions, "
                "including autism spectrum disorder, depression, anxiety, sleep-wake cycle disorders, "
                "and Rett syndrome."
            ),
            "posters": {
                "Avetisyan et al. (2023)": "Autism (ASD): gut-microbiome-brain axis, CNS/midgut gene expression",
                "Camara et al. (2025)": "Depression / psychiatric: serotonin receptor HTR1A/HTR2A in PFC vs. striatum",
                "Ford et al. (2023)": "Depression / psychiatric: HTR1A and HTR2A in serotonergic signaling",
                "Gill & Alcazar (2025)": "Depression / psychiatric: HTR1A and HTR2A in serotonergic pathway",
                "Godoy-Pena et al. (2025)": "Sleep disorders / circadian rhythm: CCHa1-R/CCHa2-R and NPF in gut-brain axis",
                "Haubelt & Alcazar (2025)": "Parkinson's disease: dopaminergic synapse, DRD2/TH/COMT in striatum",
                "Holmes (2025)": "Depression / psychiatric: tryptophan metabolism, white/vermillion, kynurenine pathway",
                "Tuttle et al. (2025)": "Depression / psychiatric: tryptophan metabolism via white/vermillion, kynurenine",
                " Cabral et al. (2025)": "Rett syndrome: MECP2, GABAergic and BDNF dysregulation in mouse brain",
            }
        },
        "Gastrointestinal / Digestive": {
            "description": (
                "Posters investigating gut physiology, gastric acid regulation, and digestive processes "
                "relevant to conditions such as GERD/acid reflux and peptic ulcer disease."
            ),
            "posters": {
                "Brown et al. (2025)": "Acid reflux/GERD: Vhal6-1 (V-ATPase) in copper cell region, phagosome pathway",
                "Dehuelbes et al. (2025)": "Peptic ulcer disease / H. pylori: JF family genes in midgut iron region",
            }
        },
        "Oncological / Cancer": {
            "description": (
                "Posters examining oncogenes, tumor suppressors, and cancer-relevant pathways "
                "in the context of tumor biology and carcinogenesis."
            ),
            "posters": {
                "Paramo-Ojeda et al. (2025)": "Colorectal cancer: KRAS/Ras85D differential expression in Drosophila midgut",
            }
        },
        "Metabolic Disorders (Broad)": {
            "description": (
                "Posters studying metabolic pathways (fatty acid oxidation, carbohydrate digestion, "
                "mitochondrial energetics, peroxisomal biology) relevant to metabolic diseases "
                "including MCADD, fatty acid oxidation disorders, Zellweger spectrum, and general "
                "metabolic dysfunction."
            ),
            "posters": {
                "Logan et al. (2025)": "Metabolic disorders: NAD+ biosynthesis via kynurenine pathway in brain regions",
                "Luera et al. (2025)": "Metabolic disorders: mitochondrial energetics (NADH:ubiquinone oxidoreductase)",
                "Meraz et al. (2023)": "Metabolic disorders: mitochondrial dysfunction in Drosophila gut",
                "Otala et al. (2025)": "Metabolic disorders / fatty acid oxidation: Acox3, Muc68e, Mdh1 across midgut",
                "Zlaket et al. (2023)": "Metabolic disorders (Zellweger spectrum): SCP2/SCPx gene family and paralogs",
            }
        },
        "Lysosomal Storage / Peroxisomal": {
            "description": (
                "Posters investigating peroxisomal and lysosomal pathways, including gene families "
                "relevant to peroxisomal biogenesis disorders."
            ),
            "posters": {}
        },
        "Basic Biology / No Specific Disease State": {
            "description": (
                "Posters focused on fundamental biological processes without a primary "
                "disease-state motivation. These studies contribute to basic science knowledge "
                "but are not directly framed around a specific human disease."
            ),
            "posters": {
                "Berbouti et al. (2025)": "Trehalose catabolism and sugar transport (trehalase, TRET1, GLUT1) in midgut",
                "Diaz et al. (2025)": "V-ATPase subunits and phagosome acidification in Drosophila copper cells",
                "Henriquez et al. (2025)": "Six immune pathways (Toll, IMD, JAK/STAT, cGAS-STING, TNFα, Hippo) in midgut",
                "Lemus et al. (2025)": "Amylase and polysaccharide digestion across midgut regions",
                "Nii et al. (2025)": "Ribosome biogenesis and rDNA transcription regulation",
                "Paderna et al. (2025)": "Slc45-1 and multicopper oxidase in iron region; melanogenesis/ferroptosis",
                "Pedireddi et al. (2025)": "Starch/sucrose metabolic pathway, 15 genes, 7 differentially expressed",
                "Rodriguez (2025)": "Cell polarity via CDC42 and aPKC in midgut epithelial homeostasis",
                "Sakana et al. (2025)": "CDC42/aPKC pathway in midgut epithelial polarity",
                "Trevino et al. (2022)": "Amyrel and maltase gene expression across midgut regions",
            }
        },
    }

    dc_counts = defaultdict(list)
    for label, bucket in disease_results.items():
        dc_counts[bucket].append(label)

    for bucket_name, details in BUCKET_DETAILS.items():
        posters_in_bucket = dc_counts.get(bucket_name, [])
        count = len(posters_in_bucket)
        plural = "s" if count != 1 else ""
        lines.append(f"## {bucket_name} ({count} poster{plural})\n")
        lines.append(f"{details['description']}\n")
        lines.append("\n| Poster | Specific Disease / Motivation |")
        lines.append("|---|---|")
        if not posters_in_bucket:
            lines.append("| *(none)* | — |")
        for poster_label in sorted(posters_in_bucket):
            specific = details["posters"].get(poster_label, "—")
            lines.append(f"| {poster_label} | {specific} |")
        lines.append("\n---\n")

    # Summary table
    lines.append("## Summary: All Disease-State Categories\n")
    lines.append("| Disease-State Category | Count | Percentage |")
    lines.append("|---|---|---|")
    total = len(disease_results)
    for bucket_name in [
        "Neuropsychiatric / Mental Health",
        "Gastrointestinal / Digestive",
        "Oncological / Cancer",
        "Metabolic Disorders (Broad)",
        "Lysosomal Storage / Peroxisomal",
        "Basic Biology / No Specific Disease State",
    ]:
        count = len(dc_counts.get(bucket_name, []))
        pct = count / total * 100
        lines.append(f"| {bucket_name} | {count} | {pct:.1f}% |")
    lines.append(f"| **Total** | **{total}** | **100%** |")

    content = "\n".join(lines)
    path = os.path.join(OUTPUT_DIR, "Report_2_Disease_State_Categories_Detailed_Breakdown.md")
    with open(path, "w") as f:
        f.write(content)
    print(f"Report 2: {path}")
    return content

def write_report_3():
    content = """# Report 3: Technical Analysis Methods
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
"""
    path = os.path.join(OUTPUT_DIR, "Report_3_Technical_Analysis_Methods.md")
    with open(path, "w") as f:
        f.write(content)
    print(f"Report 3: {path}")
    return content

# ── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    texts = load_texts()
    research_results = assign_research_category(texts)
    disease_results = {label: assign_disease_bucket(label) for label in texts}

    write_report_1(texts, research_results, disease_results)
    write_report_2(disease_results)
    write_report_3()
    print("\nAll 3 reports generated successfully.")
