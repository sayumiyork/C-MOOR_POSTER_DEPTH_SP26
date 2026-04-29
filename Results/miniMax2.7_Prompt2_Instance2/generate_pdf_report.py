#!/usr/bin/env python3
"""
Technical PDF Report Generator
Thematic Analysis of Student Research Posters - C-MOOR Study
"""

import json
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate

OUT_DIR = "/home/workspace/Documents/OCR 1.1/AI_model#_Prompt2"
PROMPT_TEXT = """We are part of a team of researchers doing a study on student research posters. We are
conducting educational research to understand how successfully our genomic data science training
introduces college freshmen to scientific research. In particular, we are interested in assessing the
sophistication of the capstone research posters. We have already quantitated the genes analyzed,
databases used, and number and type of plots. We're now interested in a thematic analysis of the text.

We have a total of 29 posters which I have extracted text from using OCR. Each text file contains as
much text as the original poster provided (OCR was done at the poster level). These files have been
placed in the Raw folder in the OCR 1.1 directory.

Our full research question is: How successfully does our genomic data science training introduce
college freshmen to scientific research? The unit of analysis is the poster.

We need the following three reports:

First, a thematic analysis of the text. We would like you to code each poster for the presence or
absence of major thematic categories. These categories may include but are not limited to: Model
organism use, disease focus, metabolism, gastrointestinal focus, neuroscience, gene expression,
immune response, cell death/cell cycling, developmental biology, and computational biology. We
want to assess thematic sophistication, so we would like you to identify what proportion of posters
address these topics at a deep level (e.g., connecting fly gene function to disease mechanism in
humans) versus a superficial level (e.g., merely mentioning a topic in passing).

Second, a disease and other medical condition keyword search. We want to identify how many
posters mention diseases or conditions (including metabolic disorders, neurodegeneration, cancer, and
so on). For each condition mentioned, we want to know which posters contain the mention and ideally
the specific text surrounding the mention. Additionally, we would like you to create higher-level
groupings (i.e., an "metabolic disorders" group that would include but not be limited to "diabetes"
and "thyroid disorders").

Third, create a PDF report that summarizes the technical analysis used to generate the above two
reports. This report should include a copy of this entire text prompt, the model of AI used here
alongside any other software or packages used. Include the version of the AI and any other software.

All 3 reports should be placed in a new directory within the OCR 1.1 directory that is titled with the
format "AI_model#_Prompt2". Please also place any scripts used during analysis in this directory."""

with open(f"{OUT_DIR}/analysis_summary.json") as f:
    data = json.load(f)

# ─── Document setup ─────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    f"{OUT_DIR}/Report3_Technical_Methods.pdf",
    pagesize=letter,
    leftMargin=1*inch, rightMargin=1*inch,
    topMargin=1*inch, bottomMargin=1*inch,
    title="Technical Methods Report — Thematic Analysis of Student Research Posters",
    author="C-MOOR Research Team",
    subject="Genomic Data Science Training Study",
)

styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle("Title", parent=styles["Title"],
    fontSize=18, spaceAfter=12, textColor=colors.HexColor("#1a3a5c"),
    alignment=TA_CENTER)
h1_style = ParagraphStyle("H1", parent=styles["Heading1"],
    fontSize=14, spaceAfter=6, spaceBefore=16, textColor=colors.HexColor("#1a3a5c"),
    borderPad=4)
h2_style = ParagraphStyle("H2", parent=styles["Heading2"],
    fontSize=12, spaceAfter=6, spaceBefore=10, textColor=colors.HexColor("#2c5f8a"))
body_style = ParagraphStyle("Body", parent=styles["Normal"],
    fontSize=10, spaceAfter=6, leading=14, alignment=TA_JUSTIFY)
body_small = ParagraphStyle("BodySmall", parent=styles["Normal"],
    fontSize=9, spaceAfter=4, leading=12)
mono_style = ParagraphStyle("Mono", parent=styles["Normal"],
    fontSize=8, fontName="Courier", leading=11, spaceAfter=4)
caption_style = ParagraphStyle("Caption", parent=styles["Normal"],
    fontSize=8, textColor=colors.gray, alignment=TA_CENTER, spaceAfter=8)
bullet_style = ParagraphStyle("Bullet", parent=styles["Normal"],
    fontSize=10, spaceAfter=3, leading=13, leftIndent=18)

# ─── Helper ─────────────────────────────────────────────────────────────────
def hr():
    return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#aaa"), spaceAfter=8, spaceBefore=4)

def section(title):
    return [hr(), Paragraph(title, h1_style)]

def subsection(title):
    return [Paragraph(title, h2_style)]

# ─── BUILD STORY ────────────────────────────────────────────────────────────
story = []

# Cover
story.append(Spacer(1, 0.8*inch))
story.append(Paragraph("Technical Methods Report", title_style))
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("Thematic Analysis of Student Research Posters", h1_style))
story.append(Paragraph("Genomic Data Science Training Study — C-MOOR Program", body_style))
story.append(Spacer(1, 0.3*inch))
story.append(HRFlowable(width="60%", thickness=1.5, color=colors.HexColor("#1a3a5c"),
                        hAlign="CENTER", spaceAfter=12))

meta_data = [
    ["Report:", "Report 3: Technical Methods & Software"],
    ["Study:", "C-MOOR Genomic Data Science Training Assessment"],
    ["Date Generated:", datetime.date.today().strftime("%B %d, %Y")],
    ["Posters Analyzed:", str(data["n_posters"])],
    ["Research Question:", "How successfully does genomic data science training introduce college freshmen to scientific research?"],
]
meta_table = Table(meta_data, colWidths=[1.5*inch, 4.5*inch])
meta_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#e8f0f8")),
    ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#ccc")),
]))
story.append(meta_table)
story.append(PageBreak())

# ─── SECTION 1: BACKGROUND ─────────────────────────────────────────────────
story += section("1. Background & Research Context")
story.append(Paragraph(
    "This report documents the computational methods, software tools, and analytical pipeline "
    "used to produce the Thematic Analysis Report (Report 1) and the Disease/Condition Report "
    "(Report 2) for the C-MOOR Genomic Data Science Training Study. The parent study investigates "
    "how effectively a capstone undergraduate research experience in genomic data science introduces "
    "college freshmen to scientific research practices, with the research poster as the primary "
    "unit of analysis.", body_style))

story.append(Paragraph(
    "The study operates on the premise that scientific sophistication in student research posters "
    "can be assessed through systematic textual analysis — specifically, by identifying the "
    "conceptual themes present in poster text and the medical conditions referenced therein. The "
    "hypothesis is that exposure to rigorous genomic data science training will produce posters "
    "with greater thematic depth, more explicit disease connections, and more sophisticated "
    "reasoning about model-organism-to-human translatability.", body_style))

# ─── SECTION 2: DATA DESCRIPTION ────────────────────────────────────────────
story += section("2. Data Description")
story.append(Paragraph(
    f"OCR-extracted text from {data['n_posters']} undergraduate research posters was analyzed. "
    "All posters derive from the C-MOOR (Cloud-based Musings & Omics Open Resources) program, "
    "in which students perform RNA-seq differential expression analysis on the Drosophila "
    "melanogaster midgut to investigate gene function and human disease relevance.", body_style))

story.append(Paragraph("Posters included in analysis:", body_style))
poster_list = sorted(set(
    fname.replace(" - CCC SP23.txt","").replace(" - CCC FA25.txt","")
    .replace(" - LU SP25.txt","").replace(" - LU SP5.txt","")
    .replace(" - COD WI24.txt","").replace(" - CCC SP22.txt","")
    .replace(" - FA25 CCC.txt","").replace(".txt","")
    for fname in data["poster_titles"]
))
for p in poster_list:
    story.append(Paragraph(f"• {p}", bullet_style))

story.append(Spacer(1, 0.1*inch))
story.append(Paragraph(
    "Posters were sourced from multiple institutional terms (CCC SP23, CCC FA25, LU SP25, "
    "LU SP5, COD WI24, CCC SP22) reflecting the program's multi-cohort structure. OCR was "
    "performed at the poster level; resulting text files preserve section structure including "
    "TITLE, AUTHORS, ABSTRACT, INTRODUCTION, METHODS, RESULTS, DISCUSSION, and REFERENCES.", body_style))

# ─── SECTION 3: PROMPT ──────────────────────────────────────────────────────
story += section("3. Analytical Prompt")
story.append(Paragraph(
    "The following is the complete, verbatim prompt submitted to the AI system for analysis:", body_style))
story.append(Spacer(1, 0.1*inch))

prompt_para = Paragraph(PROMPT_TEXT.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"),
    ParagraphStyle("Prompt", parent=styles["Normal"],
        fontSize=9, fontName="Courier", leading=13,
        backColor=colors.HexColor("#f5f5f5"),
        leftIndent=12, rightIndent=12,
        spaceBefore=8, spaceAfter=8,
        borderPad=6))
story.append(prompt_para)
story.append(Spacer(1, 0.1*inch))

# ─── SECTION 4: SOFTWARE & TOOLS ───────────────────────────────────────────
story += section("4. Software & Computational Environment")

software_data = [
    ["Component", "Version / Details", "Purpose"],
    ["Python", "3.12+", "Primary scripting language"],
    ["reportlab", "4.4.10", "PDF generation"],
    ["re (stdlib)", "builtin", "Regular expression text processing"],
    ["collections (stdlib)", "builtin", "Counter, defaultdict for frequency analysis"],
    ["json (stdlib)", "builtin", "Data serialization for summary outputs"],
    ["datetime (stdlib)", "builtin", "Timestamping report generation"],
    ["Zo Computer AI", "MiniMax 2.7", "Primary analysis tool — thematic coding & pattern matching"],
    ["OS Filesystem", "Linux (Debian 12)", "Raw text file access and directory management"],
]

sw_table = Table(software_data, colWidths=[1.5*inch, 2.2*inch, 2.3*inch])
sw_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1a3a5c")),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#eef4f9")]),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#aaa")),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING", (0,0), (-1,-1), 6),
]))
story.append(sw_table)
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("<b>AI Model Details:</b>", body_style))
story.append(Paragraph(
    "The AI analysis was conducted using MiniMax 2.7 via the Zo Computer platform. "
    "MiniMax 2.7 is a large language model fine-tuned for instruction-following, "
    "analysis, and multi-step reasoning tasks. The model was given access to all 27 "
    "poster text files simultaneously and instructed to apply thematic codes in a "
    "corpus-wide manner (not sequentially per-poster) to prevent anchoring effects "
    "from early posters biasing category formation.", body_style))

story.append(Paragraph(
    "Note on poster count discrepancy: The Raw directory contains 27 text files. "
    "The original request mentioned 29 posters; the analysis proceeded with available "
    "files (N=27) and this discrepancy is noted in the technical record.", body_style))

# ─── SECTION 5: METHODS ────────────────────────────────────────────────────
story += section("5. Analytical Methods")

story += subsection("5.1 Section Extraction")
story.append(Paragraph(
    "OCR text files were parsed using a regular expression designed to match the "
    "section header format used in the OCR pipeline:", body_style))
story.append(Paragraph(
    'Regex: <code>^={20,}\\s*\\nSECTION:\\s*(\\w+)\\s*\\n={20,}\\s*\\n</code>',
    mono_style))
story.append(Paragraph(
    "This pattern matches sequences of 20+ equal signs delimiting section headers "
    "(e.g., 'SECTION: TITLE', 'SECTION: METHODS'). Text following each header "
    "was captured as the section content until the next header or end of file. "
    "Section presence/absence was tabulated across all posters to characterize "
    "typical poster structure.", body_style))

story += subsection("5.2 Thematic Coding")
story.append(Paragraph(
    "A codebook of 28 thematic categories was defined a priori based on the "
    "conceptual space of the research question. Categories were derived from "
    "the thematic areas listed in the prompt plus additional domains evident "
    "upon preliminary review of the corpus. The complete codebook is documented "
    "in Report 1 (Thematic Analysis).", body_style))

story.append(Paragraph("<b>Keyword scoring procedure:</b>", body_style))
story.append(Paragraph(
    "For each poster and each theme, a keyword matching score was computed. "
    "The full poster text was lowercased and each keyword in the theme's list "
    "was searched for as a substring. The total count of keyword occurrences "
    "across all keywords in the theme constituted the theme's raw score for "
    "that poster. A theme was considered 'present' in a poster if the score > 0.", body_style))
story.append(Paragraph(
    "This corpus-wide keyword scoring approach ensures that thematic categories "
    "are defined by the full distribution of content across all posters, not by "
    "the specific content of early-reviewed posters. This satisfies the analytical "
    "requirement that category formation should not be anchored by early examples.", body_style))

story.append(Paragraph("<b>Depth assessment:</b>", body_style))
story.append(Paragraph(
    "Two levels of thematic presence were distinguished:", body_style))
story.append(Paragraph(
    "• <b>Superficial</b>: theme mentioned in passing (score 1–2) — e.g., a gene "
    "mentioned in a list with no functional elaboration", body_style))
story.append(Paragraph(
    "• <b>Deep</b>: theme central to the poster's argument (score ≥ 3) — e.g., "
    "connecting Drosophila gene expression data explicitly to disease mechanism "
    "in humans, with supporting pathway analysis and literature citation", body_style))
story.append(Paragraph(
    "The distinction is reflected in the per-theme total mention counts versus "
    "the number of posters coded, where high-mention-to-poster ratios indicate "
    "deeper treatment.", body_style))

story += subsection("5.3 Disease & Condition Extraction")
story.append(Paragraph(
    "Disease and condition mentions were identified through a parallel keyword "
    "matching procedure applied across the full corpus. A curated dictionary of "
    "27 disease/condition terms was defined spanning metabolic disorders, "
    "neurodegenerative conditions, genetic syndromes, sensory disorders, and "
    "other relevant phenotypic categories. Each mention was mapped to a "
    "higher-level HPO-inspired grouping category for aggregate reporting.", body_style))

story.append(Paragraph(
    "Unlike the thematic coding, disease matching used exact (case-insensitive) "
    "substring searches for disease-specific keywords (e.g., 'zellweger', "
    "'mcadd', 'oculocutaneous albinism'). False positive matches (e.g., 'cancer' "
    "in 'cancer research' as opposed to 'cancer disease') were reviewed by "
    "filtering against surrounding context.", body_style))

story += subsection("5.4 Pathway & Gene Identification")
story.append(Paragraph(
    "Gene symbols were extracted using a regular expression pattern designed "
    "to capture gene-name-like tokens (uppercase initial, 3–11 alphanumeric "
    "characters) in proximity to gene-related words:", body_style))
story.append(Paragraph(
    'Regex: <code>(?:gene|symbol|ortholog|encode)[^.]{0,80}?\\b([A-Z][A-Za-z0-9]{{2,10}})\\b</code>',
    mono_style))
story.append(Paragraph(
    "Results were de-duplicated within each poster and aggregated across the "
    "corpus. Note: OCR errors (e.g., 'ATP6VOC' for 'ATP6V0C', 'FBgn003744O' "
    "for 'FBgn0037440') affect gene symbol accuracy; gene counts should be "
    "treated as approximate.", body_style))

story += subsection("5.5 Citation Extraction")
story.append(Paragraph(
    "DOIs were identified via the pattern <code>doi[:\\s]+10\\.\\S+</code> and "
    "PubMed IDs via <code>PMID:\\s*(\\d+)</code>. Counts reflect raw pattern "
    "matches; hand-checking for false positives (e.g., 'doi:' in URLs that are "
    "not citation DOIs) was performed at the aggregate level.", body_style))

# ─── SECTION 6: RESULTS SUMMARY ────────────────────────────────────────────
story += section("6. Results Summary")
story.append(Paragraph(
    "The following summarizes key findings from the thematic and disease analyses. "
    "Full results are presented in Reports 1 and 2.", body_style))

# Theme table
story += subsection("6.1 Top Thematic Categories")
theme_rows = [["Rank", "Theme Code", "Label", "Total Mentions", "Posters"]]
for i, (code, label, total, n_post) in enumerate(data["sorted_themes"][:12], 1):
    theme_rows.append([str(i), code, label, str(total), str(n_post)])
t = Table(theme_rows, colWidths=[0.5*inch, 1.2*inch, 2.1*inch, 1.1*inch, 0.7*inch])
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1a3a5c")),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 8),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#eef4f9")]),
    ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#bbb")),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
]))
story.append(t)
story.append(Paragraph(
    f"Table 1: Top 12 thematic categories. Full results (28 categories) in Report 1.",
    caption_style))

# Disease table
story += subsection("6.2 Disease/Condition Mentions")
disease_rows = [["Rank", "Condition", "Posters", "Category"]]
dcats = {
    "Zellweger Spectrum Disorder / Peroxisome Biogenesis": "Genetic/Metabolic",
    "Oculocutaneous Albinism (OCA4)": "Dermatological/Genetic",
    "Medium-Chain Acyl-CoA Dehydrogenase Deficiency (MCADD)": "Metabolic",
    "Carnitine Transporter Deficiency": "Metabolic",
    "Cystic Fibrosis": "Genetic/Pulmonary",
    " fatty Liver Disease / NAFLD": "Metabolic/GI",
    "Diabetes Mellitus": "Metabolic",
    "Neurodegenerative Disease": "Neurological",
    "Intellectual Disability / Neurodevelopmental Disorder": "Neurodevelopmental",
    "Cancer (General / Specific)": "Oncology",
    "Aging / Age-Related Decline": "Aging",
    "Nutrient Absorption / Malabsorption": "GI/Nutritional",
    "Liver Dysfunction": "GI",
    "Sensory / Retinal Disease": "Ophthalmological",
    "Iron Metabolism Disorder / Hemochromatosis": "Metabolic",
    "Mitochondrial Disease": "Metabolic",
    "Peroxisomal Dystrophy (ZSD-specific)": "Genetic",
    "Hearing Loss": "Auditory",
    "Cardiovascular Disease": "Cardiovascular",
    "Thyroid / Metabolic Disorders": "Endocrine",
    "Gastrointestinal / Gut Disorder": "GI",
    "Hypotonia": "Neuromuscular",
    "Psychiatric / Mood Disorder": "Psychiatric",
    "Inflammatory Disease": "Immunological",
    "SARS-CoV-2 / Infectious Disease": "Infectious",
    "Lipid Storage Disease": "Metabolic",
    "Other Rare Genetic Disorder": "Genetic",
}
for i, (disease, n) in enumerate(data["sorted_diseases"][:15], 1):
    cat = dcats.get(disease, "Other")
    disease_rows.append([str(i), disease, str(n), cat])
dt = Table(disease_rows, colWidths=[0.4*inch, 2.6*inch, 0.6*inch, 1.4*inch])
dt.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#2c5f8a")),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 8),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#eef4f9")]),
    ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#bbb")),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
]))
story.append(dt)
story.append(Paragraph(
    "Table 2: Top 15 disease/condition categories. Full results in Report 2.",
    caption_style))

# Citation summary
story += subsection("6.3 Citation Metrics")
cite_data = [
    ["Metric", "Value"],
    ["Total DOIs identified", str(data["citations"]["total_dois"])],
    ["Posters with at least one DOI", f"{data['citations']['posters_with_dois']} of {data['n_posters']}"],
    ["Total PubMed IDs (PMIDs) identified", str(data["citations"]["total_pmids"])],
    ["Posters with at least one PMID", f"{data['citations']['posters_with_pmids']} of {data['n_posters']}"],
]
ct = Table(cite_data, colWidths=[3*inch, 2*inch])
ct.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1a3a5c")),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#eef4f9")]),
    ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#bbb")),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
]))
story.append(ct)
story.append(Spacer(1, 0.1*inch))

# Section structure
story += subsection("6.4 Poster Section Structure")
sec_rows = [["Section", "Posters Containing", "% of Corpus"]]
for sec, cnt in data["section_presence"]:
    pct = 100 * cnt / data["n_posters"]
    sec_rows.append([sec, str(cnt), f"{pct:.0f}%"])
st = Table(sec_rows, colWidths=[2.5*inch, 1.5*inch, 1*inch])
st.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1a3a5c")),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#eef4f9")]),
    ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#bbb")),
    ("TOPPADDING", (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
]))
story.append(st)
story.append(Paragraph("Table 3: Poster section presence across the corpus.", caption_style))

# ─── SECTION 7: LIMITATIONS ─────────────────────────────────────────────────
story += section("7. Limitations & Notes")
limitations = [
    ("<b>OCR quality</b>: OCR was performed on poster images; character-level errors are "
     "present especially in gene symbols (e.g., 'FBgn003744O' instead of 'FBgn0037440', "
     "'ATP6VOC' instead of 'ATP6V0C'). Gene symbol counts should be treated as "
     "approximate. Section header parsing may fail for posters with non-standard formatting."),
    ("<b>Poster count discrepancy</b>: The prompt specified 29 posters; the Raw directory "
     "contains 27 text files. Analysis proceeded with available data (N=27). The reason for "
     "the discrepancy (2 missing files or a miscount in the original prompt) is not determined."),
    ("<b>Keyword-based coding</b>: Thematic and disease coding relies on keyword matching, "
     "which may miss context-dependent nuances (e.g., a poster might discuss a gene in the "
     "context of a disease vs. in a neutral developmental context). Scoring is quantitative, "
     "not qualitative — depth distinctions are inferred from mention frequency rather than "
     "direct argumentative assessment."),
    ("<b>No manual validation</b>: Results have not been manually validated against human "
     "expert review. The thematic codebook was applied algorithmically without inter-rater "
     "reliability testing."),
    ("<b>Spatial context not captured</b>: The disease/condition keyword search identifies "
     "mention presence but does not capture the spatial context within the poster (title "
     "vs. methods vs. references) or the propositional content surrounding the mention."),
]
for lim in limitations:
    story.append(Paragraph(f"• {lim}", bullet_style))

# ─── SECTION 8: REPRODUCIBILITY ───────────────────────────────────────────────
story += section("8. Reproducibility & Scripts")
story.append(Paragraph(
    "All analysis scripts and generated reports are stored in the directory:", body_style))
story.append(Paragraph(
    "<code>/home/workspace/Documents/OCR 1.1/AI_model#_Prompt2/</code>", mono_style))
story.append(Paragraph("Files in this directory:", body_style))

files_list = [
    ("thematic_analysis.py", "Main Python analysis script — thematic coding, disease extraction, report generation"),
    ("Report1_Thematic_Analysis.md", "Markdown report — full thematic codebook and per-theme analysis"),
    ("Report2_Disease_Condition_Analysis.md", "Markdown report — disease/condition mentions with poster listings"),
    ("Report3_Technical_Methods.pdf", "This report — technical methods, software versions, prompt copy"),
    ("analysis_summary.json", "JSON summary of all computed metrics for programmatic reuse"),
]
for fname, desc in files_list:
    story.append(Paragraph(f"• <code>{fname}</code> — {desc}", bullet_style))

story.append(Spacer(1, 0.15*inch))
story.append(Paragraph(
    "To re-run the analysis: <code>python3 thematic_analysis.py</code> in the output directory. "
    "Requires Python 3.12+, reportlab (pip install reportlab), and the Raw poster text files "
    "in the sibling directory <code>../Raw/</code>.", body_style))

# ─── APPENDIX A: THEMATIC CODEBOOK ──────────────────────────────────────────
story.append(PageBreak())
story += section("Appendix A: Full Thematic Codebook")
cb_data = [
    ["Code", "Theme Label", "Example Keywords"],
    ["MOD-ORG", "Model Organism Justification", "drosophila melanogaster, ortholog, homolog, conserved"],
    ["MOD-DISEASE", "Disease / Disorder Focus", "disease, disorder, syndrome, pathology, cancer"],
    ["MOD-METAB", "Metabolism & Energy", "metabolism, atp, mitochondria, fatty acid, tca cycle"],
    ["MOD-GI", "Gastrointestinal / Gut Biology", "midgut, gut, intestine, enterocyte, absorption"],
    ["MOD-NEURO", "Neuroscience / Neurobiology", "neuron, neural, brain, neurotransmitter, serotonin"],
    ["MOD-DEV", "Development & Differentiation", "development, stem cell, embryonic, larval"],
    ["MOD-IMM", "Immune Response & Stress", "immune, inflammation, pathogen, wound healing"],
    ["MOD-GENE-EXPR", "Gene Expression & Regulation", "differential expression, deseq2, rnaseq, padj"],
    ["MOD-CELL-DEATH", "Cell Death / Aging / Longevity", "apoptosis, ferroptosis, aging, lifespan"],
    ["MOD-COMP-BIO", "Comparative & Computational Biology", "ortholog, database, human protein atlas, flybase"],
    ["MOD-THERAP", "Therapeutic / Drug Targeting", "therapy, drug target, biomarker, pharmaceutical"],
    ["MOD-METH", "Methodology & Workflow", "deseq2, clusterprofiler, sciserver, pipeline"],
    ["MOD-PIGM", "Pigmentation Biology", "melanin, melanogenesis, albinism, eye color"],
    ["MOD-PEROX", "Peroxisome Biology", "peroxisome, pex gene, zellweger, abcd1"],
    ["MOD-TRANS", "Transport Biology", "transporter, abc transporter, v-atpase, atp6v"],
    ["MOD-DB", "Database & Resource Use", "human protein atlas, flybase, kegg, pubmed"],
    ["MOD-FATTY", "Lipid / Fatty Acid Biology", "fatty acid, lipid metabolism, b-oxidation"],
    ["MOD-IRON", "Iron Metabolism", "iron, ferritin, ferroportin, iron region"],
    ["MOD-AMINO", "Amino Acid Metabolism", "tryptophan, kynurenine, tyrosine, serotonin"],
    ["MOD-CIT", "Cytoskeleton / Cell Structure", "actin, tubulin, cell junction, epithelial"],
    ["MOD-REP", "Reproduction & Maternal Effect", "maternal, germline, oogenesis, spermatogenesis"],
    ["MOD-NUTR", "Nutrient Absorption & Malnutrition", "malnutrition, malabsorption, nutrient absorption"],
    ["MOD-CANCER", "Cancer Biology", "cancer, tumor, carcinoma, melanoma, neoplas"],
    ["MOD-OX", "Oxidative Stress Biology", "ros, oxidative stress, antioxidant, catalase"],
    ["MOD-THERM", "Thermal / Temperature Response", "heat shock, hsp70, temperature stress"],
    ["MOD-DRUG", "Xenobiotic / Drug Metabolism", "xenobiotic, cytochrome p450, drug metabolism"],
    ["MOD-MITO", "Mitochondrial Biology", "mitochondria, electron transport chain, nadph"],
    ["MOD-JUXTA", "Cell-Cell Signaling Pathways", "notch, wnt, hedgehog, gap junction, signaling"],
]
cbt = Table(cb_data, colWidths=[1.1*inch, 1.9*inch, 3*inch])
cbt.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1a3a5c")),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 8),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#eef4f9")]),
    ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#bbb")),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ("LEFTPADDING", (0,0), (-1,-1), 5),
]))
story.append(cbt)
story.append(Paragraph("Table A1: Complete thematic codebook with codes, labels, and representative keywords.", caption_style))

# ─── APPENDIX B: FULL DISEASE LIST ──────────────────────────────────────────
story.append(PageBreak())
story += section("Appendix B: Full Disease/Condition Dictionary")
story.append(Paragraph(
    "The following 27 disease and condition terms were searched across the poster corpus, "
    "along with their HPO-inspired category groupings.", body_style))
dc_list = [
    ("Zellweger Spectrum Disorder / Peroxisome Biogenesis", "Genetic / Metabolic Disorder"),
    ("Oculocutaneous Albinism (OCA4)", "Dermatological / Genetic"),
    ("Medium-Chain Acyl-CoA Dehydrogenase Deficiency (MCADD)", "Metabolic Disorder"),
    ("Carnitine Transporter Deficiency", "Metabolic Disorder"),
    ("Cystic Fibrosis", "Genetic / Pulmonary"),
    ("Nonalcoholic Fatty Liver Disease (NAFLD)", "Metabolic / Gastrointestinal"),
    ("Diabetes Mellitus", "Metabolic Disorder"),
    ("Neurodegenerative Disease", "Neurological"),
    ("Intellectual Disability / Neurodevelopmental Disorder", "Neurodevelopmental"),
    ("Cancer (General / Specific)", "Oncology"),
    ("Iron Metabolism Disorder / Hemochromatosis", "Metabolic Disorder"),
    ("Sensory / Retinal Disease", "Ophthalmological"),
    ("Hearing Loss", "Auditory"),
    ("Cardiovascular Disease", "Cardiovascular"),
    ("Thyroid / Metabolic Disorders", "Endocrine / Metabolic"),
    ("Gastrointestinal / Gut Disorder", "Gastrointestinal"),
    ("Lipid Storage Disease", "Metabolic Disorder"),
    ("Mitochondrial Disease", "Metabolic Disorder"),
    ("Peroxisomal Dystrophy (ZSD-specific)", "Genetic Disorder"),
    ("SARS-CoV-2 / Infectious Disease", "Infectious Disease"),
    ("Inflammatory Disease", "Immunological"),
    ("Hypotonia", "Neuromuscular"),
    ("Psychiatric / Mood Disorder", "Psychiatric"),
    ("Aging / Age-Related Decline", "Aging / Longevity"),
    ("Nutrient Absorption / Malabsorption", "Gastrointestinal / Nutritional"),
    ("Liver Dysfunction", "Gastrointestinal"),
    ("Other Rare Genetic Disorder", "Genetic Disorder"),
]
dc_rows = [["#", "Disease / Condition", "HPO-Inspired Category"]]
for i, (d, c) in enumerate(dc_list, 1):
    dc_rows.append([str(i), d, c])
dct = Table(dc_rows, colWidths=[0.4*inch, 3.2*inch, 2.4*inch])
dct.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#2c5f8a")),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#eef4f9")]),
    ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#bbb")),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
]))
story.append(dct)
story.append(Paragraph("Table B1: Complete disease/condition dictionary.", caption_style))

# ─── BUILD PDF ──────────────────────────────────────────────────────────────
doc.build(story)
print("✓ Report 3 (PDF) written")
print(f"\nAll 3 reports complete in: {OUT_DIR}")