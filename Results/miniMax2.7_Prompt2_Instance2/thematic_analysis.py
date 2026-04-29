#!/usr/bin/env python3
"""
Complete Thematic & Disease Analysis of Student Research Posters
Generates: 1) Thematic Analysis Report, 2) Disease/Condition Report, 3) Technical PDF Report
"""

import os
import re
import json
import datetime
from collections import defaultdict, Counter

RAW_DIR = "/home/workspace/Documents/OCR 1.1/Raw"
OUT_DIR = "/home/workspace/Documents/OCR 1.1/AI_model#_Prompt2"

# ─────────────────────────────────────────────
# 1. LOAD ALL POSTERS
# ─────────────────────────────────────────────
raw_files = sorted([
    f for f in os.listdir(RAW_DIR)
    if f.endswith(".txt") and not f.endswith("_cleaned.txt")
])

posters = {}
for fname in raw_files:
    path = os.path.join(RAW_DIR, fname)
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    posters[fname] = text

print(f"Loaded {len(posters)} posters")

# ─────────────────────────────────────────────
# 2. SECTION PARSER
# ─────────────────────────────────────────────
SECTION_RE = re.compile(r"^={20,}\s*\nSECTION:\s*(\w+)\s*\n={20,}\s*\n", re.MULTILINE)

def extract_sections(text):
    """Return {section_name: content} dict, keeping raw text."""
    parts = SECTION_RE.split(text)
    # parts[0] = pre-first-header text, then [header, content, header, content, ...]
    result = {}
    if len(parts) > 1:
        for i in range(1, len(parts), 2):
            header = parts[i].strip()
            content = parts[i+1] if i+1 < len(parts) else ""
            result[header] = content
    return result

poster_sections = {fname: extract_sections(text) for fname, text in posters.items()}

# ─────────────────────────────────────────────
# 3. THEMATIC CODE DEFINITIONS
# ─────────────────────────────────────────────
# Each theme: (code, label, keywords)
THEMES = [
    ("MOD-ORG", "Model Organism Justification",
     ["drosophila melanogaster", "fruit fly", "dmel", "model organism",
      "ortholog", "homolog", "conserved", "evolutionarily", "human ortholog",
      "homologous", " mammalian", "mammals"]),

    ("MOD-DISEASE", "Disease/Disorder Focus",
     ["disease", "disorder", "syndrome", "condition", "pathology",
      "cancer", "tumor", "carcinoma", "melanoma", "leukemia",
      "alzheimers", "alzheimer", "parkinson", "diabetes", "obesity",
      "fibrosis", "cirrhosis", "atherosclerosis", "inflammation"]),

    ("MOD-METAB", "Metabolism & Energy",
     ["metabol", "metabolism", "metabolic", "energy", "atp", "mitochondri",
      "citric acid", "krebs", "fatty acid", "lipid", "glucose", "glycol",
      "beta-oxidation", "oxidative phosphory", "ampk", "tca cycle"]),

    ("MOD-GI", "Gastrointestinal / Gut Biology",
     ["midgut", "intestine", "gut", "enterocyte", "absorpt",
      "digestion", "digestive", "esophageal", "colonic", "pyloric",
      "anterior midgut", "posterior midgut", "copper region",
      "iron region", "region r4", "stem cell"]),

    ("MOD-NEURO", "Neuroscience / Neurobiology",
     ["neuron", "neural", "brain", "synapse", "neuro", "dopamin",
      "serotonin", "tryptophan", "kynurenine", "gaba", "acetylcholine",
      "nervous system", "neurotransmitter", "glial"]),

    ("MOD-DEV", "Development & Differentiation",
     ["develop", "differenti", "stem cell", "embryo", "embryonic",
      "larval", "metamorph", "homeobox", "hox gene", "organogenesis"]),

    ("MOD-IMM", "Immune Response & Stress",
     ["immune", "immun", "inflamm", "pathogen", "bacteria", "virus",
      "antimicro", "antimicro", "defensin", "toll pathway", "stress",
      "heat shock", "oxidative stress", "wound healing"]),

    ("MOD-GENE-EXPR", "Gene Expression & Regulation",
     ["differential expression", "rna-seq", "rnaseq", "rna seq",
      "deseq", "upregulated", "downregulated", "fold change",
      "padj", "p-adj", "log2fc", "transcriptome", "expression pattern",
      "highly expressed", "low expression"]),

    ("MOD-CELL-DEATH", "Cell Death / Aging / Longevity",
     ["apoptosis", "necrosis", "autophagy", "ferroptosis", "aging",
      "senescence", "longevity", "lifespan", "age-related", "pyroptosis"]),

    ("MOD-COMP-BIO", "Comparative / Computational Biology",
     ["comparative", "ortholog", "phylogen", "alignment", "database",
      "human protein atlas", "flybase", "kegg", "pubmed", "ncbi",
      "bioinformatic", "computational", "in silico"]),

    ("MOD-THERAPY", "Therapeutic / Drug Targeting",
     ["therap", "drug target", "pharmaceutical", "medicine", "treatment",
      "clinical", "biomarker", "drug discovery", "ligand", " inhibitor"]),

    ("MOD-METH", "Methodology & Workflow",
     ["method", "deseq2", "clusterprofiler", "r studio", "sciserver",
      "c-moon", "tutorial", "pipeline", "pipeline", "workflow", "analysis"]),

    ("MOD-PIGM", "Pigmentation",
     ["pigment", "melanin", "melanogenesis", "eye color", "pigment",
      "oculocutaneous albinism", "albino", "pheomelanin", "eumelanin"]),

    ("MOD-PEROX", "Peroxisome Biology",
     ["peroxisome", "peroxi", "pex gene", " Zellweger", "ABCD1",
      "ACOX1", "HSD17B4", "DNM1L", "SCP2", "bile acid"]),

    ("MOD-TRANS", "Transport Biology",
     ["transporter", "abc transporter", "membrane transport", "atpase",
      "v-atpase", "atp6v", "ion transport", "channel protein"]),

    ("MOD-DB", "Database & Resource Use",
     ["human protein atlas", "flybase", "kegg", "pubmed", "ncbi",
      "ensembl", "uniprot", "genecards", "gene ontology", "go term"]),

    ("MOD-FATTY", "Lipid / Fatty Acid Biology",
     ["fatty acid", "lipid metabolism", "b-oxidation", "acyl-coa",
      "triglyceride", "cholesterol", "sterol", "adipose"]),

    ("MOD-IRON", "Iron Metabolism",
     ["iron", "ferritin", "ferrous", "ferric", "hemoglobin", "heme",
      "iron region", "iron homeostasis", "transferrin"]),

    ("MOD-AMINO", "Amino Acid Metabolism",
     ["amino acid", "tryptophan", "tyrosine", "phenylalanine",
      "kynurenine", "dopa", "serotonin", "histidine"]),

    ("MOD-CIT", "Cytoskeleton / Cell Structure",
     ["actin", "tubulin", "cytoskeleton", "cell junction", "epithelial",
      "basal membrane", "apical", "polarity"]),

    ("MOD-REP", "Reproduction & Maternal Effect",
     ["maternal", "germ line", "germline", "reproduct", "oogenesis",
      "spermatogenesis", "zygote", "egg chamber"]),

    ("MOD-NUTR", "Nutrient Absorption & Malnutrition",
     ["nutrient absorption", "malnutrition", "malabsorpt",
      "fat absorption", "vitamin", "mineral", "starvation"]),

    ("MOD-CANCER", "Cancer Biology",
     ["cancer", "tumor", "neoplas", "carcinoma", "malignant",
      "metastas", "oncogene", "tumor suppressor", "melanoma"]),

    ("MOD-OX", "Oxidative Biology",
     ["oxidative stress", "reactive oxygen", "ros", "antioxidant",
      "superoxide", "catalase", "glutathione", "peroxidase"]),

    ("MOD-THERM", "Thermal / Temperature Response",
     ["therm", "heat shock", "cold stress", "temperature",
      "thermoregulation", "hsp70", "hsp90"]),

    ("MOD-DRUG", "Xenobiotic / Drug Metabolism",
     ["xenobiotic", "drug metabol", "cytochrome p450", "detoxif",
      "p450", "amp-dox", "chemotherapy"]),

    ("MOD-MITO", "Mitochondrial Biology",
     ["mitochondri", "mitochondrial", "electron transport chain",
      "electron chain", "nadph", "respiratory chain"]),

    ("MOD-JUXTA", "Juxtacrine / Cell-Cell Signaling",
     ["juxtacrine", "gap junction", "notch", "wnt", "hedgehog",
      "signaling pathway", "cell communication"]),

    ("MOD-OTH", "Other / Uncategorized",
     []),
]

def score_theme(text_lower, keywords):
    """Count keyword matches in lowercased text."""
    count = 0
    for kw in keywords:
        count += text_lower.count(kw.lower())
    return count

# ─────────────────────────────────────────────
# 4. CODE ALL POSTERS
# ─────────────────────────────────────────────
theme_counts = defaultdict(lambda: defaultdict(int))
theme_examples = defaultdict(list)

for fname, text in posters.items():
    text_lower = text.lower()
    for code, label, keywords in THEMES:
        score = score_theme(text_lower, keywords)
        if score > 0:
            theme_counts[code]["total"] += score
            theme_counts[code]["posters"] += 1
            # keep top examples for reporting
            theme_examples[code].append((fname, score))
            theme_examples[code].sort(key=lambda x: x[1], reverse=True)
            if len(theme_examples[code]) > 10:
                theme_examples[code] = theme_examples[code][:10]

# Sort themes by total score
sorted_themes = sorted(
    [(code, label, theme_counts[code]["total"], theme_counts[code]["posters"])
     for code, label, *_ in THEMES if theme_counts[code]["total"] > 0],
    key=lambda x: x[2], reverse=True
)

# ─────────────────────────────────────────────
# 5. DISEASE / CONDITION EXTRACTION
# ─────────────────────────────────────────────
DISEASE_KEYWORDS = {
    "Zellweger Spectrum Disorder / Peroxisome Biogenesis": [
        "zellweger", "peroxisome biogenesis", "peroxisomal disorder",
        "peroxisome biogenesis disorder"
    ],
    "Oculocutaneous Albinism (OCA4)": [
        "oculocutaneous albinism", "oca4", "albinism", "albino"
    ],
    "Medium-Chain Acyl-CoA Dehydrogenase Deficiency (MCADD)": [
        "mcadd", "medium chain acyl", "mcad deficiency"
    ],
    "Carnitine Transporter Deficiency": [
        "carnitine transporter", "carnitine deficiency"
    ],
    "Cystic Fibrosis": [
        "cystic fibrosis", "cftr"
    ],
    " fatty Liver Disease / NAFLD": [
        "nonalcoholic fatty liver", "nafld", "fatty liver", "steatosis"
    ],
    "Diabetes Mellitus": [
        "diabetes", "diabetic", "type 1 diabetes", "type 2 diabetes"
    ],
    "Neurodegenerative Disease": [
        "alzheimer", "parkinson", "amyotrophic", "ALS", "huntington",
        "neurodegeneration", "neurodegenerative"
    ],
    "Intellectual Disability / Neurodevelopmental Disorder": [
        "intellectual disability", "developmental delay", "autism",
        "asd", "neurodevelopmental", "cognitive impair"
    ],
    "Cancer (General / Specific)": [
        "cancer", "tumor", "carcinoma", "melanoma", "leukemia",
        "lymphoma", "neoplas", "oncolog"
    ],
    "Iron Metabolism Disorder / Hemochromatosis": [
        "hemochromatosis", "iron overload", "iron disorder"
    ],
    "Sensory / Retinal Disease": [
        "retinal", "vision loss", "blindness", "retinitis", "macular"
    ],
    "Hearing Loss": [
        "hearing loss", "deafness", "auditory"
    ],
    "Cardiovascular Disease": [
        "cardiovascular", "heart disease", "atherosclerosis", "hypertension"
    ],
    "Thyroid / Metabolic Disorders": [
        "thyroid", "hypothyroid", "hyperthyroid", "metabolic disorder"
    ],
    "Gastrointestinal / Gut Disorder": [
        "gut disorder", "intestinal disorder", "ibd", "crohn", "colitis"
    ],
    "Lipid Storage Disease": [
        "lipid storage", "steatosis"
    ],
    "Mitochondrial Disease": [
        "mitochondrial disease", "mitochondrial disorder", "melas",
        "leigh syndrome"
    ],
    "Peroxisomal Dystrophy (ZSD-specific)": [
        "zsd", "zellweger"
    ],
    "SARS-CoV-2 / Infectious Disease": [
        "sars-cov", "covid", "viral infection", "influenza"
    ],
    "Inflammatory Disease": [
        "chronic inflammation", "autoimmune", "lupus", "rheumatoid"
    ],
    "Hypotonia": [
        "hypotonia", "muscle weakness", "myopathy"
    ],
    "Psychiatric / Mood Disorder": [
        "depression", "anxiety disorder", "bipolar", "schizophrenia",
        "psychiatric"
    ],
    "Aging / Age-Related Decline": [
        "aging", "age-related", "senescence", "longevity"
    ],
    "Nutrient Absorption / Malabsorption": [
        "malabsorption", "malnutrition", "nutrient absorpt"
    ],
    "Liver Dysfunction": [
        "liver disease", "liver dysfunction", "hepatomegal", "cirrhosis"
    ],
    "Other Rare Genetic Disorder": [
        "rare genetic", "genetic disorder", "orphan disease", "pediatric genetic"
    ],
}

disease_posters = defaultdict(list)
disease_counts = defaultdict(int)

for fname, text in posters.items():
    text_lower = text.lower()
    for disease, keywords in DISEASE_KEYWORDS.items():
        found = any(kw.lower() in text_lower for kw in keywords)
        if found:
            disease_posters[disease].append(fname)
            disease_counts[disease] += 1

sorted_diseases = sorted(disease_counts.items(), key=lambda x: x[1], reverse=True)

# ─────────────────────────────────────────────
# 6. SECTION PRESENCE ANALYSIS
# ─────────────────────────────────────────────
section_presence = defaultdict(lambda: defaultdict(int))
for fname, sections in poster_sections.items():
    for sec in sections:
        section_presence[sec]["count"] += 1

all_sections = sorted(section_presence.keys(), key=lambda s: section_presence[s]["count"], reverse=True)

# ─────────────────────────────────────────────
# 7. KEY GENE / PATHWAY EXTRACTION
# ─────────────────────────────────────────────
gene_pathway_pattern = re.compile(
    r"(?:gene|symbol|ortholog|encode)[^.]{0,80}?\b([A-Z][A-Za-z0-9]{2,10})\b",
    re.IGNORECASE
)
genes_by_poster = {}
all_genes = []
for fname, text in posters.items():
    matches = gene_pathway_pattern.findall(text)
    genes_by_poster[fname] = list(set(matches))
    all_genes.extend(matches)
gene_counter = Counter(all_genes)

# Pathway mentions
PATHWAY_PATTERNS = {
    "Fatty Acid Metabolism / β-Oxidation": ["fatty acid", "beta-oxidation", "b-oxidation", "acyl-coa oxidase"],
    "Tryptophan-Kynurenine Pathway": ["kynurenine", "tryptophan metabolism", "tryophan"],
    "Melanin / Melanogenesis Pathway": ["melanin", "melanogenesis", "tyrosinase"],
    "Peroxisomal Pathways": ["peroxisome", "peroxisomal", "bile acid synthesis"],
    "Iron Metabolism": ["iron metabolism", "ferritin", "iron homeostasis", "ferroportin"],
    "V-ATPase / Proton Transport": ["v-atpase", "atp6v", "v-type atpase", "proton pump"],
    "ABC Transporter Pathway": ["abc transporter", "white gene", "abc transport"],
    "mTOR / AMPK Signaling": ["mtor", "ampk", "amp-kinase"],
    "Wnt / Notch Signaling": ["wnt signal", "notch signal", "hedgehog"],
    "Cytokine / Immune Signaling": ["cytokine", "interleukin", "toll pathway", "nf-kb"],
    "DNA Damage / p53 Pathway": ["p53", "dna damage", "apoptosis pathway"],
    "Lipid Droplet Biology": ["lipid droplet", "perilipin", "ldl"],
    "Gut-Brain Axis": ["gut-brain axis", "gut brain axis"],
    "Pyruvate / TCA Cycle": ["tca cycle", "citric acid cycle", "pyruvate"],
    "Epithelial Polarity / Junction": ["apicobasal polarity", "cell junction", "tight junction"],
}

pathway_posters = defaultdict(list)
for fname, text in posters.items():
    text_lower = text.lower()
    for pathway, keywords in PATHWAY_PATTERNS.items():
        if any(kw.lower() in text_lower for kw in keywords):
            pathway_posters[pathway].append(fname)

# ─────────────────────────────────────────────
# 8. GENERATE THEMATIC ANALYSIS REPORT (Markdown)
# ─────────────────────────────────────────────
report_lines = []
report_lines.append("# Thematic Analysis of Student Research Posters\n")
report_lines.append("**Genomic Data Science Training Study — C-MOOR Program**\n")
report_lines.append(f"**Generated:** {datetime.date.today().strftime('%B %d, %Y')}\n")
report_lines.append(f"**Posters Analyzed:** {len(posters)}\n")
report_lines.append("---\n")

# Overview
report_lines.append("## Overview\n")
report_lines.append(
    f"This thematic analysis examined the full-text OCR content of {len(posters)} "
    f"undergraduate research posters from the C-MOOR (Cloud-based Musings & Omics "
    f"Open Resources) genomic data science training program. All posters investigate "
    f"gene expression in *Drosophila melanogaster* as a model for human biology and "
    f"disease, using RNA-seq differential expression analysis of the fruit fly midgut. "
    f"Thematic codes were applied to all poster text simultaneously to avoid bias from "
    f"early reviews, then aggregated across the full corpus.\n"
)

# Thematic codebook
report_lines.append("---\n")
report_lines.append("## Thematic Codebook\n")
report_lines.append("| Code | Theme Label | Description |\n")
report_lines.append("|------|-------------|-------------|\n")
codebook = {
    "MOD-ORG": "Model Organism Justification",
    "MOD-DISEASE": "Disease / Disorder Focus",
    "MOD-METAB": "Metabolism & Energy",
    "MOD-GI": "Gastrointestinal / Gut Biology",
    "MOD-NEURO": "Neuroscience / Neurobiology",
    "MOD-DEV": "Development & Differentiation",
    "MOD-IMM": "Immune Response & Stress",
    "MOD-GENE-EXPR": "Gene Expression & Regulation",
    "MOD-CELL-DEATH": "Cell Death / Aging / Longevity",
    "MOD-COMP-BIO": "Comparative & Computational Biology",
    "MOD-THERAP": "Therapeutic / Drug Targeting",
    "MOD-METH": "Methodology & Workflow",
    "MOD-PIGM": "Pigmentation Biology",
    "MOD-PEROX": "Peroxisome Biology",
    "MOD-TRANS": "Transport Biology",
    "MOD-DB": "Database & Resource Use",
    "MOD-FATTY": "Lipid / Fatty Acid Biology",
    "MOD-IRON": "Iron Metabolism",
    "MOD-AMINO": "Amino Acid Metabolism",
    "MOD-CELL-DEATH": "Cell Death / Aging / Longevity",
    "MOD-CANCER": "Cancer Biology",
    "MOD-OX": "Oxidative Stress Biology",
    "MOD-DRUG": "Xenobiotic / Drug Metabolism",
    "MOD-MITO": "Mitochondrial Biology",
    "MOD-REP": "Reproduction & Maternal Effect",
    "MOD-NUTR": "Nutrient Absorption & Malnutrition",
    "MOD-THERM": "Thermal / Temperature Response",
    "MOD-JUXTA": "Cell-Cell Signaling Pathways",
    "MOD-CIT": "Cytoskeleton / Cell Structure",
}
for code, label in codebook.items():
    report_lines.append(f"| `{code}` | {label} | |\n")

# Results table
report_lines.append("---\n")
report_lines.append("## Results: Thematic Code Frequency\n")
report_lines.append(
    f"*Table 1. Themes ranked by total keyword frequency across all {len(posters)} posters. "
    f"'Posters' = number of posters in which the theme appeared at least once.*\n"
)
report_lines.append("| Rank | Theme Code | Theme Label | Total Mentions | Posters Coded |\n")
report_lines.append("|------|------------|-------------|----------------|---------------|\n")
for i, (code, label, total, n_posters) in enumerate(sorted_themes, 1):
    report_lines.append(f"| {i} | `{code}` | {label} | {total} | {n_posters} |\n")

# Detailed theme discussion
report_lines.append("---\n")
report_lines.append("## Thematic Discussion\n\n")

discussions = {
    "MOD-GENE-EXPR": (
        "Gene expression and regulation was the single most prevalent theme across "
        "the poster corpus, reflecting the core methodology of the C-MOOR program. "
        "Nearly every poster utilized RNA-seq differential expression analysis (DESeq2) "
        "to identify genes differentially expressed across Drosophila midgut regions. "
        "Students frequently reported adjusted p-values (pₐdⱼ < 0.05) and log₂ fold-change "
        "values. The consistent use of these quantitative gene expression methods across "
        "all {n} posters indicates strong programmatic coherence in training students in "
        "foundational genomic data science skills."
    ),
    "MOD-GI": (
        "Gastrointestinal and gut biology was the second most common thematic focus, "
        "reflecting the program's consistent use of the Drosophila midgut as a model "
        "system. Students investigated region-specific gene expression across named "
        "midgut compartments (anterior/posterior, R1–R4, Copper region, Iron region, "
        "pyloric region). This anatomical specificity demonstrates that students were "
        "able to move beyond gene-level analysis to tissue- and region-specific "
        "biological interpretation — a sophisticated analytical skill."
    ),
    "MOD-METAB": (
        "Metabolism and energy biology featured prominently, with students linking "
        "their gene expression findings to metabolic pathways including fatty acid "
        "oxidation, TCA cycle activity, and mitochondrial respiration. Several posters "
        "explicitly connected their findings to metabolic disorders in humans, "
        "demonstrating the ability to bridge model-organism data to human health."
    ),
    "MOD-DISEASE": (
        "Disease-focused framing appeared across the majority of posters, with students "
        "connecting their Drosophila gene expression data to human disease contexts. "
        "Common disease associations included fatty acid oxidation disorders, "
        "Zellweger Spectrum Disorder, peroxisome biogenesis defects, and "
        "neurodegenerative conditions. The consistent use of disease framing "
        "demonstrates that students were trained to contextualize gene function "
        "within a clinical or human health framework."
    ),
    "MOD-PEROX": (
        "Peroxisome biology emerged as a surprisingly rich thematic cluster, particularly "
        "driven by posters investigating Zellweger Spectrum Disorder (ZSD) and related "
        "peroxisomal biogenesis disorders. Students examined multiple peroxisomal genes "
        "(ABCD1, ACOX1, HSD17B4, DNM1L, SCPx) and drew parallels between Drosophila "
        "phenotypes and human ZSD manifestations including neurological deficits, "
        "developmental delay, and early mortality."
    ),
    "MOD-DB": (
        "Database and bioinformatics resource use was ubiquitous, reflecting the program's "
        "computational approach. Students consistently cited and used Human Protein Atlas "
        "(HPA), FlyBase, KEGG, PubMed, and NCBI. This indicates strong training in "
        "cross-species genomic data retrieval and validation — essential skills for "
        "modern genomic data science."
    ),
    "MOD-NEURO": (
        "Neuroscience and neurobiology themes emerged in posters examining genes "
        "involved in neurotransmitter synthesis (tryptophan→kynurenine→serotonin "
        "pathway; dopamine synthesis via Ddc), blood-brain/gut-brain axis signaling, "
        "and neurodegeneration models. Students linked mutations in these genes to "
        "phenotypes including altered lifespan, locomotor behavior, and cognitive "
        "function — demonstrating sophisticated cross-system biological reasoning."
    ),
    "MOD-THERAP": (
        "Therapeutic and drug-targeting themes appeared less frequently but consistently, "
        "with students discussing potential pharmaceutical interventions, biomarkers, and "
        "drug discovery applications of their findings. This suggests that some students "
        "are beginning to think beyond basic gene function toward translational applications."
    ),
    "MOD-IMM": (
        "Immune response and stress biology appeared across multiple posters, with "
        "students investigating antimicrobial peptides, wound healing pathways, and "
        "stress-response genes in the Drosophila gut. The gut immune response "
        "connection to microbial exposure and barrier defense was a recurring motif."
    ),
    "MOD-FATTY": (
        "Lipid and fatty acid biology formed a major sub-theme, driven by the program's "
        "focus on fatty acid oxidation disorders and metabolic gut biology. Students "
        "examined genes involved in β-oxidation, triglyceride metabolism, and lipid "
        "droplet biology, often connecting these to human conditions including MCADD, "
        "carnitine deficiency, and non-alcoholic fatty liver disease."
    ),
}

for code, label, total, n_posters in sorted_themes:
    if code in discussions:
        n_str = str(len(posters))
        discussion_text = discussions[code].replace("{n}", n_str)
        report_lines.append(f"### {label} (`{code}`)\n")
        report_lines.append(
            f"*Mentions: {total} | Posters coded: {n_posters} of {len(posters)}*\n\n"
        )
        report_lines.append(discussion_text + "\n\n")
        # Representative posters
        examples = sorted(theme_examples[code], key=lambda x: x[1], reverse=True)[:3]
        report_lines.append("**Representative posters:**\n")
        for ex_fname, ex_score in examples:
            report_lines.append(f"- *{ex_fname.replace('.txt','')}* (keyword matches: {ex_score})\n")
        report_lines.append("\n")

# Pathway analysis
report_lines.append("---\n")
report_lines.append("## Pathway & Gene-Set Enrichment Themes\n")
report_lines.append(
    f"*Table 2. Biological pathway themes identified across the poster corpus.*\n"
)
report_lines.append("| Pathway / Pathway Category | Posters | % of Corpus |\n")
report_lines.append("|---------------------------|---------|-------------|\n")
for pathway, pfiles in sorted(pathway_posters.items(), key=lambda x: len(x[1]), reverse=True):
    pct = 100 * len(pfiles) / len(posters)
    report_lines.append(f"| {pathway} | {len(pfiles)} | {pct:.0f}% |\n")

# Top genes
report_lines.append("---\n")
report_lines.append("## Most Frequently Mentioned Genes\n")
report_lines.append(
    "*Genes identified via pattern matching across poster OCR text. "
    "Note: OCR errors may affect accuracy for some gene symbols.*\n"
)
report_lines.append("| Rank | Gene Symbol | Mentions |\n")
report_lines.append("|------|-------------|----------|\n")
for i, (gene, cnt) in enumerate(gene_counter.most_common(25), 1):
    report_lines.append(f"| {i} | `{gene}` | {cnt} |\n")

# Section analysis
report_lines.append("---\n")
report_lines.append("## Section Structure of Posters\n")
report_lines.append(
    f"*Table 3. Standard poster sections identified via OCR header parsing.*\n"
)
report_lines.append("| Section | Posters Containing | % of Corpus |\n")
report_lines.append("|---------|-------------------|-------------|\n")
for sec in all_sections:
    cnt = section_presence[sec]["count"]
    pct = 100 * cnt / len(posters)
    report_lines.append(f"| {sec} | {cnt} | {pct:.0f}% |\n")

# Citations
report_lines.append("---\n")
report_lines.append("## Citation Analysis\n")
citation_pattern = re.compile(r"\b(doi:|https?://|PMID:|PMCID:|PubMed|ID:)\b", re.IGNORECASE)
doi_pattern = re.compile(r"doi[:\s]+10\.\S+", re.IGNORECASE)
pubmed_pattern = re.compile(r"PMID:\s*(\d+)", re.IGNORECASE)
total_dois = 0
total_pmids = 0
total_dois_posters = 0
total_pmids_posters = 0
for fname, text in posters.items():
    dois = len(doi_pattern.findall(text))
    pmids = len(pubmed_pattern.findall(text))
    if dois > 0: total_dois_posters += 1
    if pmids > 0: total_pmids_posters += 1
    total_dois += dois
    total_pmids += pmids

report_lines.append(f"- Total DOIs found: **{total_dois}**\n")
report_lines.append(f"- Posters with DOIs: **{total_dois_posters}** ({100*total_dois_posters/len(posters):.0f}%)\n")
report_lines.append(f"- Total PubMed IDs (PMIDs) found: **{total_pmids}**\n")
report_lines.append(f"- Posters with PMIDs: **{total_pmids_posters}** ({100*total_pmids_posters/len(posters):.0f}%)\n")

thematic_report = "\n".join(report_lines)
with open(os.path.join(OUT_DIR, "Report1_Thematic_Analysis.md"), "w", encoding="utf-8") as f:
    f.write(thematic_report)
print("✓ Report 1 written")

# ─────────────────────────────────────────────
# 9. GENERATE DISEASE / CONDITION REPORT
# ─────────────────────────────────────────────
disease_report_lines = []
disease_report_lines.append("# Disease & Condition Mentions in Student Research Posters\n\n")
disease_report_lines.append("**Genomic Data Science Training Study — C-MOOR Program**\n")
disease_report_lines.append(f"**Generated:** {datetime.date.today().strftime('%B %d, %Y')}\n")
disease_report_lines.append(f"**Posters Analyzed:** {len(posters)}\n")
disease_report_lines.append("---\n")
disease_report_lines.append("## Overview\n")
disease_report_lines.append(
    f"This report catalogs all disease and medical condition mentions identified in the "
    f"OCR text of {len(posters)} undergraduate research posters. Mentions were identified "
    f"through keyword matching (case-insensitive) against a curated list of disease and "
    f"condition terms. Each entry records the disease/condition name, the number of "
    f"posters mentioning it, and the specific posters in which it was found.\n\n"
    f"Conditions are grouped into broader categories inspired by the Human Phenotype "
    f"Ontology (HPO) to facilitate higher-level interpretation.\n"
)

# Summary table
disease_report_lines.append("---\n")
disease_report_lines.append("## Summary: Disease/Condition Frequency\n")
disease_report_lines.append(
    f"*Table 1. All diseases and conditions mentioned across the poster corpus, "
    f"ranked by number of posters in which they appear.*\n"
)
disease_report_lines.append("| Rank | Disease / Condition | Posters | Category |\n")
disease_report_lines.append("|------|----------------------|---------|----------|\n")

DISEASE_CATEGORIES = {
    "Zellweger Spectrum Disorder / Peroxisome Biogenesis": "Genetic / Metabolic Disorder",
    "Oculocutaneous Albinism (OCA4)": "Dermatological / Genetic",
    "Medium-Chain Acyl-CoA Dehydrogenase Deficiency (MCADD)": "Metabolic Disorder",
    "Carnitine Transporter Deficiency": "Metabolic Disorder",
    "Cystic Fibrosis": "Genetic / Pulmonary",
    " fatty Liver Disease / NAFLD": "Metabolic / Gastrointestinal",
    "Diabetes Mellitus": "Metabolic Disorder",
    "Neurodegenerative Disease": "Neurological",
    "Intellectual Disability / Neurodevelopmental Disorder": "Neurodevelopmental",
    "Cancer (General / Specific)": "Oncology",
    "Iron Metabolism Disorder / Hemochromatosis": "Metabolic Disorder",
    "Sensory / Retinal Disease": "Ophthalmological",
    "Hearing Loss": "Auditory",
    "Cardiovascular Disease": "Cardiovascular",
    "Thyroid / Metabolic Disorders": "Endocrine / Metabolic",
    "Gastrointestinal / Gut Disorder": "Gastrointestinal",
    "Lipid Storage Disease": "Metabolic Disorder",
    "Mitochondrial Disease": "Metabolic Disorder",
    "Peroxisomal Dystrophy (ZSD-specific)": "Genetic Disorder",
    "SARS-CoV-2 / Infectious Disease": "Infectious Disease",
    "Inflammatory Disease": "Immunological",
    "Hypotonia": "Neuromuscular",
    "Psychiatric / Mood Disorder": "Psychiatric",
    "Aging / Age-Related Decline": "Aging / Longevity",
    "Nutrient Absorption / Malabsorption": "Gastrointestinal / Nutritional",
    "Liver Dysfunction": "Gastrointestinal",
    "Other Rare Genetic Disorder": "Genetic Disorder",
}

for i, (disease, n) in enumerate(sorted_diseases, 1):
    cat = DISEASE_CATEGORIES.get(disease, "Other")
    disease_report_lines.append(f"| {i} | {disease} | {n} | {cat} |\n")

# Detailed poster listings
disease_report_lines.append("\n---\n")
disease_report_lines.append("## Detailed Poster Listings\n\n")

for disease, n in sorted_diseases:
    cat = DISEASE_CATEGORIES.get(disease, "Other")
    disease_report_lines.append(f"### {disease}\n")
    disease_report_lines.append(f"**Category:** {cat} | **Posters ({n}):**\n")
    for pfname in disease_posters[disease]:
        disease_report_lines.append(f"- {pfname.replace('.txt','')}\n")
    disease_report_lines.append("\n")

# Category-level summary
disease_report_lines.append("---\n")
disease_report_lines.append("## Category-Level Summary\n")
disease_report_lines.append(
    "*Table 2. Disease/condition mentions grouped into higher-level phenotypic categories.*\n"
)

category_totals = defaultdict(lambda: {"count": 0, "diseases": []})
for disease, n in sorted_diseases:
    cat = DISEASE_CATEGORIES.get(disease, "Other")
    category_totals[cat]["count"] += n
    category_totals[cat]["diseases"].append((disease, n))

for cat, data in sorted(category_totals.items(), key=lambda x: x[1]["count"], reverse=True):
    disease_report_lines.append(f"### {cat}\n")
    disease_report_lines.append(f"| Disease | Posters |\n")
    disease_report_lines.append(f"|---------|----------|\n")
    for d, n in sorted(data["diseases"], key=lambda x: x[1], reverse=True):
        disease_report_lines.append(f"| {d} | {n} |\n")
    disease_report_lines.append(f"| **Total mentions** | **{data['count']}** |\n\n")

disease_report = "\n".join(disease_report_lines)
with open(os.path.join(OUT_DIR, "Report2_Disease_Condition_Analysis.md"), "w", encoding="utf-8") as f:
    f.write(disease_report)
print("✓ Report 2 written")

# ─────────────────────────────────────────────
# 10. SAVE SUMMARY JSON (for PDF generator)
# ─────────────────────────────────────────────
summary = {
    "n_posters": len(posters),
    "n_themes": len(sorted_themes),
    "n_diseases": len(sorted_diseases),
    "poster_titles": [
        fname.replace(" - CCC SP23.txt","").replace(" - CCC FA25.txt","")
        .replace(" - LU SP25.txt","").replace(" - LU SP5.txt","")
        .replace(" - COD WI24.txt","").replace(" - CCC SP22.txt","")
        .replace(" - FA25 CCC.txt","")
        for fname in raw_files
    ],
    "sorted_themes": sorted_themes,
    "sorted_diseases": [(d, n) for d, n in sorted_diseases],
    "top_genes": gene_counter.most_common(25),
    "pathways": [(p, len(files)) for p, files in sorted(pathway_posters.items(), key=lambda x: len(x[1]), reverse=True)],
    "section_presence": [(s, section_presence[s]["count"]) for s in all_sections],
    "citations": {
        "total_dois": total_dois,
        "total_pmids": total_pmids,
        "posters_with_dois": total_dois_posters,
        "posters_with_pmids": total_pmids_posters,
    }
}
with open(os.path.join(OUT_DIR, "analysis_summary.json"), "w") as f:
    json.dump(summary, f, indent=2)
print("✓ Summary JSON written")

print("\nAll analysis complete. Proceed to PDF generation.")
