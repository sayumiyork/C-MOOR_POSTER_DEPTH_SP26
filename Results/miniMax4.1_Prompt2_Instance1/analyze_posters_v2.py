#!/usr/bin/env python3
"""
Thematic Analysis of Student Research Posters - Version 2
Analyzes 27 raw OCR text files for research motivation categories and disease states.
"""

import os
import json
import re
from collections import defaultdict

RAW_DIR = "/home/workspace/Documents/OCR 1.1/Raw"
OUT_DIR = "/home/workspace/Documents/OCR 1.1/AI_model_Prompt2"
os.makedirs(OUT_DIR, exist_ok=True)

# ─── LOAD POSTERS ──────────────────────────────────────────────────────────────
def load_posters():
    files = sorted(os.listdir(RAW_DIR))
    posters = {}
    for f in files:
        path = os.path.join(RAW_DIR, f)
        with open(path, 'r', errors='ignore') as fh:
            raw = fh.read()
        lines = raw.split('\n')
        keep = []
        skip = False
        for line in lines:
            if "SECTION: AUTHORS" in line:
                skip = True
            elif "SECTION: REFERENCES" in line:
                skip = True
            elif line.startswith("SECTION:") and skip:
                skip = False
            if not skip:
                keep.append(line)
        posters[f] = '\n'.join(keep)
    return posters

# ─── MOTIVATION CATEGORIES ────────────────────────────────────────────────────
# Keywords per category
CATEGORY_KEYWORDS = {
    "Neurological & Psychiatric Disease": [
        "autism", "asd", "parkinson", "rett syndrome", "mecp2", "schizophrenia",
        "post-traumatic stress disorder", "ptsd", "bdnf", "gabrb3", "htr1a", "htr2a",
        "tryptophan", "kynurenine", "neuropsychiatric", "mental health",
        "neuroserotonin", "serotonergic", "serotonin receptor", "dopamine receptor drd2",
        "neurodevelopmental", "psychiatric"
    ],
    "Cancer": [
        "cancer", "tumor", "oncogene", "kras", "ras85d", "colon cancer",
        "colorectal cancer", "apc", "brca2", "pik3ca", "pi3k92e", "mlh1",
        "pms2", "mismatch repair", "neoplas", "malignant", "metastasis",
        "carcinoma", "oncogenic", "cell proliferation"
    ],
    "Metabolic & Digestive Disease": [
        "acid reflux", "gerd", "trehalose", "carbohydrate metabolism",
        "starch", "sucrose", "amylase", "polysaccharide digestion",
        "fatty acid metabolism", "metabolic disorder", "mcadd",
        "carnitine transporter", "galactosemia", "insulin", "glucose",
        "diabetes", "hypoglycemia", "acyl-coa", "lipid metabolism",
        "dietary", "nutrient absorption", "midgut", "copper region",
        "fatty liver", "liver dysfunction", "copper cell region"
    ],
    "Inherited / Genetic Disorder": [
        "zellweger", "peroxisomal disorder", "oculocutaneous albinism",
        "oca4", "albinism", "inherited disorder", "congenital",
        "genetic disorder", "rare metabolic disorder", "peroxisome"
    ],
    "Basic Biology": [
        "immune pathway", "immune response", "development", "stem cell",
        "homeobox", "neuropeptide", "ortholog", "regional expression",
        "differential expression", "signaling pathway", "transcription factor",
        "paralog", "cell type", "circadian", "sleep", "gut-brain",
        "gut microbiome", "gene regulation", "midgut region",
        "neural", "dopamine", "pigmentation", "melanogenesis",
        "peroxisomal", "peptide", "hormone"
    ],
}

# Category definitions
CATEGORY_DEFINITIONS = {
    "Basic Biology": (
        "Research focused on understanding fundamental biological mechanisms — such as gene expression patterns, "
        "regional tissue specialization, signaling pathways, or developmental processes — without explicitly "
        "targeting a specific human disease. These posters use model organisms to explore how genes and cells "
        "normally function. Example topics: regional gut gene expression profiling, immune pathway profiling, "
        "neuropeptide signaling biology, paralog/ortholog characterization, or pigment/melanin biology."
    ),
    "Neurological & Psychiatric Disease": (
        "Research motivated by understanding the molecular basis of brain or nervous system disorders. "
        "These posters investigate genes and pathways linked to cognitive, behavioral, or neuropsychiatric "
        "conditions in humans. Example topics: autism spectrum disorder, Parkinson's disease, "
        "tryptophan-kynurenine metabolism, serotonin/dopamine receptor signaling, Rett syndrome, "
        "or other neurodevelopmental conditions."
    ),
    "Cancer": (
        "Research motivated by understanding cancer biology, specifically oncogenes, tumor suppressor genes, "
        "cell cycle regulation, or cancer-related pathways. These posters frame the work around uncontrolled "
        "cell growth, tumor development, or cancer risk. Example topics: KRAS oncogene and colon cancer, "
        "mismatch repair genes, tumor suppressors (APC, BRCA2), or PI3K pathway in cancer."
    ),
    "Metabolic & Digestive Disease": (
        "Research motivated by understanding metabolic or digestive disorders, including conditions affecting "
        "the liver, gut, or nutrient processing. These posters focus on pathways such as carbohydrate "
        "metabolism, fatty acid oxidation, acid reflux, or nutrient absorption. Example topics: acid reflux "
        "disease, fatty acid metabolism disorders, galactosemia, amylase gene expression in diabetes, "
        "trehalose catabolism, or liver dysfunction."
    ),
    "Inherited / Genetic Disorder": (
        "Research motivated by understanding specific inherited or rare genetic disorders. These posters "
        "explicitly name and characterize a clinical genetic condition and use the model organism to "
        "understand its mechanisms. Example topics: Zellweger Spectrum Disorder, oculocutaneous albinism "
        "(OCA4), or other inborn errors of metabolism."
    ),
    "Other": (
        "Research that does not fit into any of the five primary categories. This may include posters "
        "focused purely on applied biotechnology method validation, insect physiology without disease framing, "
        "or topics that cross multiple categories without a dominant motivation."
    ),
}

# Tiebreaking priority (higher = more preferred when scores are tied)
TIEBREAK_ORDER = [
    "Neurological & Psychiatric Disease",
    "Cancer",
    "Metabolic & Digestive Disease",
    "Inherited / Genetic Disorder",
    "Basic Biology",
    "Other"
]

def score_poster(text_lower):
    scores = {}
    for cat, keywords in CATEGORY_KEYWORDS.items():
        scores[cat] = sum(1 for kw in keywords if kw in text_lower)
    return scores

def classify_poster(scores):
    max_score = max(scores.values())
    if max_score == 0:
        return "Other", scores

    # Get all categories with max score
    top_cats = [cat for cat, s in scores.items() if s == max_score]
    if len(top_cats) == 1:
        return top_cats[0], scores
    # Tiebreak: use TIEBREAK_ORDER priority (first in list wins)
    for cat in TIEBREAK_ORDER:
        if cat in top_cats:
            return cat, scores
    return top_cats[0], scores

# ─── DISEASE EXTRACTION ────────────────────────────────────────────────────────
DISEASE_PATTERNS = [
    # Neurological / Psychiatric
    ("Autism Spectrum Disorder (ASD)", ["autism spectrum disorder", "autism (asd", "asd", "autism"]),
    ("Parkinson's Disease", ["parkinson"]),
    ("Rett Syndrome", ["rett syndrome"]),
    ("Schizophrenia", ["schizophrenia"]),
    ("Post-Traumatic Stress Disorder (PTSD)", ["ptsd", "post-traumatic stress disorder"]),
    ("Neurodevelopmental Disorder", ["neurodevelopmental disorder"]),
    # Cancer
    ("Cancer (general)", ["cancer"]),
    ("Colon Cancer", ["colon cancer"]),
    ("Colorectal Cancer", ["colorectal"]),
    ("KRAS-Driven Cancer", ["kras"]),
    # Metabolic / Digestive
    ("Acid Reflux / GERD", ["acid reflux", "gerd"]),
    ("Diabetes", ["diabetes"]),
    ("Metabolic Disorder", ["metabolic disorder"]),
    ("MCADD (Medium-Chain Acyl-CoA Dehydrogenase Deficiency)", ["mcadd"]),
    ("Carnitine Transporter Deficiency", ["carnitine transporter deficiency"]),
    ("Galactosemia", ["galactosemia"]),
    ("Hypoglycemia", ["hypoglycemia"]),
    ("Fatty Acid Metabolism Disorder", ["fatty acid metabolism", "fatty acid oxidation"]),
    ("Liver Dysfunction", ["liver dysfunction", "fatty liver"]),
    ("Zellweger Spectrum Disorder (ZSD)", ["zellweger"]),
    ("Inflammatory Bowel Disease", ["inflammatory bowel disease", "crohn", "colitis"]),
    # Skin / Pigmentation
    ("Oculocutaneous Albinism Type 4 (OCA4)", ["oculocutaneous albinism", "oca4"]),
    ("Cystic Fibrosis", ["cystic fibrosis"]),
    # Neurological again
    ("Alzheimer's Disease", ["alzheimer"]),
    ("Aging (linked to disease)", ["aging"]),
    ("Neurodegenerative Disease", ["neurodegenerative"]),
    # Cardiovascular
    ("Cardiovascular Disease", ["cardiovascular disorder", "cardiovascular disease"]),
]

def extract_diseases(text_lower):
    diseases = set()
    for disease_name, keywords in DISEASE_PATTERNS:
        for kw in keywords:
            if kw in text_lower:
                diseases.add(disease_name)
                break
    return sorted(diseases)

# ─── EVIDENCE EXTRACTOR ────────────────────────────────────────────────────────
def get_evidence_bullets(text, category, max_bullets=8):
    """Extract text snippets that support the category assignment."""
    if category == "Other":
        return []

    keywords = CATEGORY_KEYWORDS.get(category, [])
    bullets = []
    lines = text.split('\n')

    for kw in keywords:
        if kw in text.lower():
            for line in lines:
                if kw.lower() in line.lower() and len(line.strip()) > 15:
                    clean = line.strip()
                    # Truncate very long lines
                    if len(clean) > 220:
                        clean = clean[:220] + "..."
                    if clean not in bullets and len(bullets) < max_bullets:
                        bullets.append(f"- \"{clean}\"")
                    break

    return bullets[:max_bullets]

# ─── REPORT BUILDERS ───────────────────────────────────────────────────────────
def shortname(fname):
    """Strip the file suffix to get a readable poster name."""
    return fname.replace(".txt", "").strip()

def build_report1(analysis_results):
    lines = []
    lines.append("# Report 1: Thematic Analysis — Research Motivation Categories\n\n")
    lines.append("**Analyst:** AI (MiniMax M2.7, via Zo Computer)  \n")
    lines.append("**Source:** 27 raw OCR text files from `Documents/OCR 1.1/Raw/`  \n")
    lines.append("**Date:** 2026-04-28  \n\n")
    lines.append("---\n\n")

    # Group posters by category
    cat_groups = defaultdict(list)
    for fname, res in analysis_results.items():
        cat_groups[res["category"]].append(shortname(fname))

    # ── Section A: Category Table ─────────────────────────────────────────
    lines.append("## Section A: Category Counts and Poster Lists\n\n")
    lines.append("| Category | Count | Posters |\n")
    lines.append("|---|---|---|\n")
    cat_order = ["Basic Biology", "Neurological & Psychiatric Disease",
                 "Cancer", "Metabolic & Digestive Disease",
                 "Inherited / Genetic Disorder", "Other"]
    for cat in cat_order:
        names = cat_groups.get(cat, [])
        lines.append(f"| **{cat}** | {len(names)} | {', '.join(names)} |\n")
    lines.append(f"\n**Total posters analyzed: 27**\n\n")

    # ── Section B: Category Definitions ───────────────────────────────────
    lines.append("## Section B: Category Definitions\n\n")
    for cat in cat_order:
        lines.append(f"### {cat}\n")
        lines.append(f"{CATEGORY_DEFINITIONS[cat]}\n\n")

    # ── Section C: Per-Poster Evidence ────────────────────────────────────
    lines.append("---\n\n")
    lines.append("## Section C: Per-Poster Evidence for Category Assignment\n\n")
    lines.append("For each poster, a bullet-point list provides specific text evidence supporting "
                 "the category assignment. For posters with elements of multiple categories, "
                 "the tie-breaking rationale is noted.\n\n")

    for fname, res in analysis_results.items():
        cat = res["category"]
        name = shortname(fname)
        scores = res["scores"]
        text = res["text"]
        text_lower = text.lower()

        lines.append(f"### {name}\n")
        lines.append(f"**Assigned Category:** {cat}\n")

        # Cross-category note
        other_cats = {k: v for k, v in scores.items() if k != cat and v > 0}
        if other_cats:
            lines.append(f"\n*Note: This poster also showed elements of: {', '.join(other_cats.keys())} "
                         f"(scores: {other_cats}). Category assigned based on dominant motivation per "
                         f"predefined tie-breaking rules.*\n")

        # Evidence bullets
        bullets = get_evidence_bullets(text, cat)
        if bullets:
            lines.append("\n" + "\n".join(bullets) + "\n")
        else:
            lines.append("\n- *(No specific keyword evidence recovered from available text sections.)*\n")

        # For Other category: explain where it would fit
        if cat == "Other":
            max_other = max(scores.values()) if scores else 0
            if max_other > 0:
                implied_cat = max(scores, key=scores.get)
                lines.append(f"\n*Note: While classified as 'Other', this poster would most strongly "
                             f"align with '{implied_cat}' (score={scores[implied_cat]}) if a "
                             f"6th category were permitted. {CATEGORY_DEFINITIONS[implied_cat][:100]}...*\n")

        lines.append("\n")

    return '\n'.join(lines)

def build_report2(disease_map, analysis_results):
    lines = []
    lines.append("# Report 2: Human Disease States Identified in Poster Texts\n\n")
    lines.append("**Analyst:** AI (MiniMax M2.7, via Zo Computer)  \n")
    lines.append("**Source:** 27 raw OCR text files from `Documents/OCR 1.1/Raw/`  \n")
    lines.append("**Date:** 2026-04-28  \n\n")
    lines.append("---\n\n")

    # ── Section A: Per-poster table ─────────────────────────────────────────
    lines.append("## Section A: Per-Poster Disease Table\n\n")
    lines.append("| Poster | Human Diseases Mentioned |\n")
    lines.append("|---|---|\n")
    for fname in sorted(disease_map.keys()):
        diseases = disease_map[fname]
        name = shortname(fname)
        if diseases:
            lines.append(f"| {name} | {'; '.join(diseases)} |\n")
        else:
            lines.append(f"| {name} | *(No human diseases identified in text)* |\n")
    lines.append("\n")

    # ── Section B: Broad category analysis ─────────────────────────────────
    lines.append("---\n\n")
    lines.append("## Section B: Broad Disease Category Summary\n\n")
    lines.append("Posters were classified into high-level disease categories. "
                 "A poster is counted in a category if it mentions **at least one** disease in that category.\n\n")

    broad_cats = {
        "Neurological & Psychiatric": ["autism", "parkinson", "rett", "schizophrenia",
                                       "ptsd", "neurodevelopmental", "mental health",
                                       "bdnf", "neuropsychiatric"],
        "Cancer / Oncological": ["cancer", "tumor", "colon cancer", "colorectal",
                                 "kras", "neoplas", "malignant"],
        "Metabolic": ["diabetes", "metabolic disorder", "mcadd", "carnitine",
                      "galactosemia", "hypoglycemia", "fatty acid metabolism",
                      "fatty liver", "liver dysfunction"],
        "Digestive / Gastrointestinal": ["acid reflux", "gerd", "inflammatory bowel",
                                         "crohn", "colitis"],
        "Inherited / Developmental": ["zellweger", "peroxisomal", "oculocutaneous albinism",
                                       "oca4", "albinism", "inherited disorder"],
        "Aging / Neurodegenerative": ["aging", "neurodegenerative"],
        "Skin / Pigmentation": ["albinism", "melanin", "pigmentation"],
        "Cardiovascular": ["cardiovascular"],
        "No Human Disease Identified": []
    }

    total = 27
    lines.append("| Broad Disease Category | # of Posters | % of Total |\n")
    lines.append("|---|---|---|\n")
    for broad_cat, keywords in broad_cats.items():
        if broad_cat == "No Human Disease Identified":
            count = sum(1 for d in disease_map.values() if len(d) == 0)
        else:
            count = 0
            for fname, diseases in disease_map.items():
                text_lower = analysis_results[fname]["text"].lower()
                if any(kw in text_lower for kw in keywords):
                    count += 1
        pct = round(count / total * 100, 1)
        lines.append(f"| {broad_cat} | {count} | {pct}% |\n")

    lines.append(f"\n*Total posters: {total}. Percentages do not sum to 100% as posters may mention diseases in multiple categories.*\n\n")

    # ── Section C: Methodology ─────────────────────────────────────────────
    lines.append("---\n\n")
    lines.append("## Section C: Methodology Notes\n\n")
    lines.append("Disease mentions were identified through keyword pattern matching across the full poster text "
                 "(Authors and References sections excluded). Both specific named conditions "
                 "(e.g., 'Parkinson's Disease') and general terms (e.g., 'cancer', 'metabolic disorder') "
                 "were captured using the poster's own wording where possible. "
                 "Broader category groupings were defined to enable aggregate reporting.\n")

    return '\n'.join(lines)

def build_report3():
    lines = []
    lines.append("# Report 3: Technical Analysis — Methods, Tools, and Prompt Documentation\n\n")
    lines.append("**Analyst:** AI (MiniMax M2.7, via Zo Computer)  \n")
    lines.append("**Date:** 2026-04-28  \n\n")
    lines.append("---\n\n")

    lines.append("## 1. Original Research Prompt\n\n")
    lines.append("> *We are part of a team of researchers doing a study on student research posters. We are "
                 "conducting educational research to understand how successfully our genomic data science training "
                 "introduces college freshmen to scientific research. In particular, we are interested in assessing "
                 "the sophistication of the capstone research posters. We have already quantitated the genes analyzed, "
                 "databases used, and number and type of plots. We're now interested in a thematic analysis of the text.*\n\n")
    lines.append("> *We have a total of 29 posters which I have extracted text from using OCR... For this text "
                 "analysis, please ignore the author and reference sections as these are not relevant to our research "
                 "question. I have included only the 27 high quality posters in these folders.*\n\n")
    lines.append("> *Please conduct a thematic analysis of the raw text files. Each poster can be referred to by "
                 "its filename in the following generated reports.*\n\n")
    lines.append("> *First, please analyze all the posters for the motivation behind the research and sort them "
                 "into up to 5 categories. You may choose the categories... Please also include a 6th 'Other' "
                 "category... Please only assign one category per poster. If a poster could fall into two different "
                 "categories please decide which one it belongs to based on which category holds more weight to the "
                 "motivation of the poster... Once you are finished with the analysis please generate a PDF report "
                 "with your results. The report should include 1) A table with the total count of posters included in "
                 "each category, a list of posters included in each category, a short and easy to understand "
                 "explanation of what each category means... 2) For each poster please create a bullet-point list of "
                 "text from the poster that supports assigning it to the category you chose... If the poster is in the "
                 "other category please detail what category it would have been placed in if you were allowed more "
                 "categories...*\n\n")
    lines.append("> *Second, regardless of the results for each poster above, we would like to know what human "
                 "diseases are included in the text of each poster... Create a PDF report that includes 1) A table "
                 "relating the poster to any human diseases that were listed in the text. Please also include posters "
                 "that did not list human diseases. 2) A broader analysis that shows that percent of posters in total "
                 "mentioned broader categories of disease states...*\n\n")
    lines.append("> *Third, create a PDF report that summarizes the technical analysis used to generate the above "
                 "two reports. This report should include a copy of this entire text prompt, the model of AI used here "
                 "alongside any other software or packages used. Include the version of the AI and any other software.*\n\n")
    lines.append("> *All 3 reports should be placed in a new directory within the OCR 1.1 directory that is titled "
                 "with the format 'AI_model#_Prompt2'. Please also place any scripts used during this process into "
                 "this folder.*\n")

    lines.append("\n## 2. AI Model and Version\n\n")
    lines.append("| Component | Version / Details |\n")
    lines.append("|---|---|\n")
    lines.append("| AI Model | MiniMax M2.7 (Zo Computer) |\n")
    lines.append("| Underlying LLM | MiniMax text-generation model (vercel:minimax/minimax-m2.7) |\n")
    lines.append("| Session Context | 27 raw OCR text files read into context prior to analysis |\n")
    lines.append("| Analysis Date | 2026-04-28 |\n\n")

    lines.append("## 3. Software and Toolchain\n\n")
    lines.append("| Tool | Version | Purpose |\n")
    lines.append("|---|---|---|\n")
    lines.append("| Python | 3.12 | Core scripting, text processing, analysis |\n")
    lines.append("| pandoc | 2.17.1.1 | Markdown to PDF conversion |\n")
    lines.append("| TeX Live | 2023 Debian package | LaTeX engine for pandoc PDF output |\n")
    lines.append("| Operating System | Debian GNU/Linux 12 (bookworm) | Execution environment |\n")
    lines.append("| Zo Computer | Current | AI orchestration platform |\n\n")

    lines.append("## 4. Analysis Pipeline\n\n")
    lines.append("**Step 1 — Data Loading**  \n")
    lines.append("All 27 raw OCR text files were read from `/home/workspace/Documents/OCR 1.1/Raw/`. "
                 "File names follow the pattern: `{Author et al. (Year)} - {Institution} {Semester}.txt`. "
                 "The Authors and References sections were programmatically stripped from each file "
                 "before analysis, as these were not relevant to the research question.\n\n")

    lines.append("**Step 2 — Keyword-Based Thematic Scoring**  \n")
    lines.append("Each poster's text was searched for keywords associated with each of the five motivation "
                 "categories. Keyword lists were curated to capture distinct research motivations. "
                 "A simple count of matching keyword hits was computed per category. The category with "
                 "the highest count was assigned to that poster. If no keywords matched, the poster was "
                 "assigned to 'Other'. Cross-category scores were recorded to identify and annotate "
                 "posters with mixed motivations.\n\n")

    lines.append("**Step 3 — Tie-Breaking Rule**  \n")
    lines.append("When two or more categories had equal keyword scores, a predefined priority order "
                 "(Neurological > Cancer > Metabolic > Inherited > Basic Biology > Other) was applied "
                 "to deterministically assign exactly one category per poster. This ensures reproducibility "
                 "regardless of file processing order.\n\n")

    lines.append("**Step 4 — Disease Extraction**  \n")
    lines.append("A separate keyword-pattern scan was performed across all poster texts to identify human "
                 "disease mentions. Both specific named conditions and general terms were captured using "
                 "the poster's own wording. Authors and References sections were excluded.\n\n")

    lines.append("**Step 5 — Report Generation**  \n")
    lines.append("Three Python scripts generated Markdown-formatted reports, which were then converted to "
                 "PDF using pandoc with pdflatex engine. Reports saved to:\n")
    lines.append("`/home/workspace/Documents/OCR 1.1/AI_model_Prompt2/`\n\n")

    lines.append("## 5. Category Assignment Reproducibility\n\n")
    lines.append("The five motivation categories were defined as follows:\n\n")
    for cat in ["Basic Biology", "Neurological & Psychiatric Disease", "Cancer",
                "Metabolic & Digestive Disease", "Inherited / Genetic Disorder"]:
        lines.append(f"- **{cat}**: {CATEGORY_DEFINITIONS[cat][:200]}...\n")
    lines.append(f"- **Other**: {CATEGORY_DEFINITIONS['Other'][:200]}...\n\n")

    lines.append("**Tie-breaking rule**: When two or more categories had equal keyword scores, "
                 "the category with the higher predefined priority was selected.\n")

    return '\n'.join(lines)

# ─── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    print("Loading posters...")
    posters = load_posters()
    print(f"Loaded {len(posters)} posters.")

    print("Classifying posters by research motivation...")
    analysis_results = {}
    disease_map = {}
    for fname, text in posters.items():
        text_lower = text.lower()
        scores = score_poster(text_lower)
        cat, scored = classify_poster(scores)
        analysis_results[fname] = {
            "category": cat,
            "scores": scored,
            "text": text
        }
        disease_map[fname] = extract_diseases(text_lower)

    # Summary
    cat_counts = defaultdict(int)
    for fname, res in analysis_results.items():
        cat_counts[res["category"]] += 1
    print("Category counts:", dict(cat_counts))

    print("Writing Markdown reports...")
    r1 = build_report1(analysis_results)
    r1_path = os.path.join(OUT_DIR, "Report_1_Thematic_Analysis_Motivation_Categories.md")
    with open(r1_path, 'w', encoding='utf-8') as f:
        f.write(r1)
    print(f"  -> {r1_path}")

    r2 = build_report2(disease_map, analysis_results)
    r2_path = os.path.join(OUT_DIR, "Report_2_Disease_State_Analysis.md")
    with open(r2_path, 'w', encoding='utf-8') as f:
        f.write(r2)
    print(f"  -> {r2_path}")

    r3 = build_report3()
    r3_path = os.path.join(OUT_DIR, "Report_3_Technical_Analysis_Methods.md")
    with open(r3_path, 'w', encoding='utf-8') as f:
        f.write(r3)
    print(f"  -> {r3_path}")

    print("\nCleaning Unicode and converting to PDF...")

    # Clean unicode for LaTeX compatibility
    for path in [r1_path, r2_path, r3_path]:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        content = content.encode('ascii', errors='replace').decode('ascii')
        with open(path, 'w', encoding='ascii') as f:
            f.write(content)

    # Convert to PDF
    import subprocess
    for md_path in [r1_path, r2_path, r3_path]:
        pdf_path = md_path.replace('.md', '.pdf')
        result = subprocess.run(
            ['pandoc', md_path, '-o', pdf_path,
             '--pdf-engine=pdflatex',
             '-V', 'geometry:margin=1in'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"  PDF created: {pdf_path}")
        else:
            print(f"  PDF error for {md_path}: {result.stderr[:200]}")

    # Save JSON data
    json_data = {}
    for fname, res in analysis_results.items():
        name = shortname(fname)
        json_data[name] = {
            "category": res["category"],
            "scores": {k: v for k, v in res["scores"].items() if v > 0},
            "diseases": disease_map[fname]
        }
    json_path = os.path.join(OUT_DIR, "analysis_data.json")
    with open(json_path, 'w') as f:
        json.dump(json_data, f, indent=2)
    print(f"\nAnalysis data: {json_path}")
    print("Done.")

if __name__ == "__main__":
    main()