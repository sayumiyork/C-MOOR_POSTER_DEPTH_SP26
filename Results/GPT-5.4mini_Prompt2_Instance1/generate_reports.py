from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    ListFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

CATEGORY_INFO = {
    "disease_model": {
        "label": "Human disease models and translational health",
        "definition": "Posters where a named human disease, disorder, or direct health model is the main reason for the work. Examples include autism, Rett syndrome, Parkinson’s disease, cardiovascular disease, galactosemia, acid reflux, colon cancer, albinism, and Zellweger spectrum disorder.",
    },
    "metabolism": {
        "label": "Metabolism, digestion, and energy homeostasis",
        "definition": "Posters focused on sugar, lipid, or amino-acid metabolism; digestion; absorption; or energy balance. Examples include trehalase, amylase, fatty acid metabolism, galactose metabolism, and carbohydrate digestion.",
    },
    "neurobiology": {
        "label": "Neurobiology, behavior, and signaling",
        "definition": "Posters centered on nervous-system signaling, sleep, feeding behavior, gut-brain communication, or related signaling pathways without a named disease being the main driver.",
    },
    "basic_biology": {
        "label": "Basic gene regulation, development, and cell biology",
        "definition": "Posters mainly about gene function, patterning, pigmentation, transcriptional control, or cell biology. These tend to be foundational biology studies with only a secondary disease connection, if any.",
    },
    "defense": {
        "label": "Defense, detoxification, and stress response",
        "definition": "Posters focused on immune defense, phagocytosis, detoxification, or environmental resistance. Examples include immune pathways, phagosome acidification, and insecticide resistance.",
    },
    "other": {
        "label": "Other",
        "definition": "Posters that do not fit the five main categories above.",
    },
}

BROAD_DISEASE_INFO = {
    "metabolic_digestive": "Metabolic / digestive / energy disorders",
    "neuro": "Neurodevelopmental / neurodegenerative disorders",
    "cardio": "Cardiovascular disorders",
    "cancer": "Cancer / neoplasia",
    "genetic": "Genetic / inherited syndromes",
    "pigment": "Pigmentation / dermatologic disorders",
}

POSTERS = [
    {
        "file": "Avetisyan et al. (2023) - CCC SP23.txt",
        "category": "disease_model",
        "evidence_tokens": ["autism", "asd", "gut-microbiome-brain axis", "autism management"],
        "diseases": ["autism", "Autism Spectrum Disorder (ASD)"],
        "broad_categories": ["neuro"],
        "notes": "Primary motivation is autism-related gene expression in the gut-brain axis.",
    },
    {
        "file": "Berbouti et al. (2025) - CCC FA25.txt",
        "category": "metabolism",
        "evidence_tokens": ["trehalase", "trehalose", "energy metabolism", "digestive roles"],
        "diseases": [],
        "broad_categories": [],
        "notes": "Carbohydrate metabolism and regional digestion are the main themes.",
    },
    {
        "file": "Brown et al. (2025) - CCC SP25.txt",
        "category": "disease_model",
        "evidence_tokens": ["acid reflux", "acidification", "human gene ortholog", "backflow of stomach acid"],
        "diseases": ["acid reflux"],
        "broad_categories": ["metabolic_digestive"],
        "notes": "A disease mechanism study, but the poster still focuses on midgut gene expression.",
    },
    {
        "file": "Cabral et al. (2025) - CCC FA25.txt",
        "category": "disease_model",
        "evidence_tokens": ["MECP2", "Rett syndrome", "neurodevelopmental disorders", "prefrontal cortex"],
        "diseases": ["Rett syndrome", "neurodevelopmental disorders"],
        "broad_categories": ["neuro", "genetic"],
        "notes": "The disease link is central, even though the poster also contains basic brain-expression work.",
    },
    {
        "file": "Camara et al. (2025) - LU SP25.txt",
        "category": "metabolism",
        "evidence_tokens": ["amylase genes", "diabetes", "Alzheimer", "digestive"],
        "diseases": ["diabetes", "Alzheimer’s"],
        "broad_categories": ["metabolic_digestive", "neuro"],
        "notes": "The main motivation is amylase function and digestion; disease examples are secondary context.",
    },
    {
        "file": "Dehuelbes et al. (2025) - LU SP5.txt",
        "category": "metabolism",
        "evidence_tokens": ["fatty acid metabolism", "energy homeostasis", "metabolic disorders", "obesity", "metabolic syndrome"],
        "diseases": ["metabolic disorders", "obesity", "metabolic syndrome", "fatty acid oxidation disorders"],
        "broad_categories": ["metabolic_digestive"],
        "notes": "Metabolism and energy balance are the dominant themes.",
    },
    {
        "file": "Diaz et al. (2025) - CCC SP25.txt",
        "category": "defense",
        "evidence_tokens": ["immune defense", "phagosome acidification", "phagocytosis", "cellular defense", "infections"],
        "diseases": [],
        "broad_categories": [],
        "notes": "This is a cellular defense / immunity poster, not a named disease poster.",
    },
    {
        "file": "Ford et al. (2023) - CCC SP23.txt",
        "category": "defense",
        "evidence_tokens": ["insecticide resistance", "DDT", "Cytochrome P450", "detoxification"],
        "diseases": [],
        "broad_categories": [],
        "notes": "Environmental defense and xenobiotic resistance are the main motivations.",
    },
    {
        "file": "Gill & Alcazar (2025) - CCC FA25.txt",
        "category": "neurobiology",
        "evidence_tokens": ["serotonin receptor signaling", "prefrontal cortex", "striatum", "serotonin"],
        "diseases": [],
        "broad_categories": [],
        "notes": "A basic neuroscience signaling study.",
    },
    {
        "file": "Godoy-Pena et al. (2025) - CCC FA25.txt",
        "category": "neurobiology",
        "evidence_tokens": ["sleep", "circadian rhythm", "feeding behavior", "gut-brain region", "sleep quality"],
        "diseases": [],
        "broad_categories": [],
        "notes": "Sleep and behavior regulation are the key ideas.",
    },
    {
        "file": "Haubelt & Alcazar et al. (2025) - CCC FA25.txt",
        "category": "disease_model",
        "evidence_tokens": ["Parkinson", "dopaminergic synapse", "Drd2", "neuropsychiatric disorder"],
        "diseases": ["Parkinson's Disease"],
        "broad_categories": ["neuro"],
        "notes": "Parkinson’s disease is the organizing theme of the poster.",
    },
    {
        "file": "Henriquez et al. (2025) - COD WI24.txt",
        "category": "defense",
        "evidence_tokens": ["immune pathways", "bacterial invasion", "immune response", "immune active"],
        "diseases": [],
        "broad_categories": [],
        "notes": "Immune-pathway activity is the core motivation.",
    },
    {
        "file": "Holmes (2025) - CCC SP25.txt",
        "category": "basic_biology",
        "evidence_tokens": ["melanogenesis", "neuromelanin", "dopamine", "pigmentation", "Parkinson"],
        "diseases": ["Parkinson's"],
        "broad_categories": ["neuro"],
        "notes": "Primarily pigmentation and dopamine biology, with a secondary neurodegenerative connection.",
    },
    {
        "file": "Lemus et al. (2025) - FA25 CCC.txt",
        "category": "metabolism",
        "evidence_tokens": ["macromolecule breakdown", "starch and sucrose metabolism", "absorption", "human digestion", "metabolic disorders"],
        "diseases": ["metabolic disorders"],
        "broad_categories": ["metabolic_digestive"],
        "notes": "Digestive carbohydrate processing is the dominant theme.",
    },
    {
        "file": "Logan et al. (2025) - CCC FA25.txt",
        "category": "disease_model",
        "evidence_tokens": ["cardiovascular disorders", "blood pressure", "hypertension", "ACE", "obesity"],
        "diseases": ["cardiovascular disorders", "hypertension", "obesity"],
        "broad_categories": ["cardio", "metabolic_digestive"],
        "notes": "A translational cardiovascular model built around ACE/ANCE genes.",
    },
    {
        "file": "Luera et al. (2025) - CCC FA25.txt",
        "category": "neurobiology",
        "evidence_tokens": ["feeding behavior", "gut-brain axis", "NPF", "NPFR", "homeostasis"],
        "diseases": [],
        "broad_categories": [],
        "notes": "Neuropeptide signaling and feeding behavior are the main ideas.",
    },
    {
        "file": "Meraz et al. (2023) - CCC SP23.txt",
        "category": "basic_biology",
        "evidence_tokens": ["tyrosine kinases", "cell growth and development", "tumor-suppression", "human ortholog"],
        "diseases": [],
        "broad_categories": [],
        "notes": "This is mostly a gene-family / function poster with only a light cancer hint.",
    },
    {
        "file": "Nii et al. (2025) - CCC FA25.txt",
        "category": "metabolism",
        "evidence_tokens": ["lipid metabolism", "energy storage", "fatty acid synthesis", "iron", "ACC"],
        "diseases": [],
        "broad_categories": [],
        "notes": "Metabolic regulation and energy storage dominate.",
    },
    {
        "file": "Otala et al. (2025) - LU SP25.txt",
        "category": "disease_model",
        "evidence_tokens": ["fatty acid metabolism disorders", "MCADD", "Carnitine transporter deficiency", "hypoglycemia", "liver dysfunction"],
        "diseases": ["MCADD", "Carnitine transporter deficiency", "hypoglycemia", "liver dysfunction", "muscle weakness"],
        "broad_categories": ["metabolic_digestive", "genetic"],
        "notes": "A clear inherited metabolic-disorder framing.",
    },
    {
        "file": "Paderna et al. (2025) - CCC SP25.txt",
        "category": "disease_model",
        "evidence_tokens": ["oculocutaneous albinism type 4", "albinism", "skin, eyes, and hair", "melanin"],
        "diseases": ["oculocutaneous albinism type 4"],
        "broad_categories": ["pigment", "genetic"],
        "notes": "A pigmentation disorder with a direct human-disease connection.",
    },
    {
        "file": "Paramo-Ojeda et al. (2025) - CCC SP25.txt",
        "category": "disease_model",
        "evidence_tokens": ["KRAS-driven colon cancer", "human cancers", "tumor suppressor", "cell growth"],
        "diseases": ["colon cancer", "human cancers"],
        "broad_categories": ["cancer"],
        "notes": "Cancer is the central motivation.",
    },
    {
        "file": "Pedireddi et al. (2025) - CCC SP25.txt",
        "category": "metabolism",
        "evidence_tokens": ["sugar metabolism", "starch and sucrose metabolic pathway", "polysaccharide digestion", "nutrient absorption"],
        "diseases": [],
        "broad_categories": [],
        "notes": "Carbohydrate digestion and absorption are the focus.",
    },
    {
        "file": "Rodriguez (2025) - CCC SP25.txt",
        "category": "disease_model",
        "evidence_tokens": ["galactosemia", "rare metabolic disorder", "Leloir pathway", "galactose"],
        "diseases": ["galactosemia"],
        "broad_categories": ["metabolic_digestive", "genetic"],
        "notes": "A direct metabolic-disorder model.",
    },
    {
        "file": "Sakana et al. (2025) - CCC SP25.txt",
        "category": "basic_biology",
        "evidence_tokens": ["TALE homeobox genes", "patterning", "development", "differentiation", "gene expression control"],
        "diseases": [],
        "broad_categories": [],
        "notes": "Developmental gene regulation and midgut patterning are the main goals.",
    },
    {
        "file": "Trevino et al. (2022) - CCC SP22.txt",
        "category": "disease_model",
        "evidence_tokens": ["Zellweger Spectrum Disorder", "peroxisomes", "mutation", "disorder"],
        "diseases": ["Zellweger Spectrum Disorder (ZSD)"],
        "broad_categories": ["metabolic_digestive", "genetic"],
        "notes": "A classic disease-model poster built around peroxisomal biology.",
    },
    {
        "file": "Tuttle et al. (2025) - CCC SP25.txt",
        "category": "metabolism",
        "evidence_tokens": ["tryptophan metabolism", "kynurenine pathway", "aging", "stress responses", "immune response"],
        "diseases": [],
        "broad_categories": [],
        "notes": "Metabolic pathway analysis with broader physiological implications.",
    },
    {
        "file": "Zlaket et al. (2023) - CCC SP23.txt",
        "category": "disease_model",
        "evidence_tokens": ["Zellweger's Syndrome", "peroxisomes", "fatty acid chains", "cholesterol uptake"],
        "diseases": ["Zellweger's Syndrome"],
        "broad_categories": ["metabolic_digestive", "genetic"],
        "notes": "Peroxisomal disease biology is central.",
    },
]

FILE_RE = re.compile(r"SECTION: ([A-Z ]+)\n=+\n(.*?)(?=\n=+\nSECTION: |\Z)", re.S)


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.replace("’", "'").replace("“", '"').replace("”", '"').replace("–", "-").replace("—", "-")
    return text.lower()


def split_sentences(text: str) -> list[str]:
    collapsed = re.sub(r"\s+", " ", text.strip())
    if not collapsed:
        return []
    parts = re.split(r"(?<=[.!?])\s+", collapsed)
    return [p.strip() for p in parts if p.strip()]


def parse_sections(text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    for match in FILE_RE.finditer(text):
        sections[match.group(1).strip()] = match.group(2).strip()
    return sections


def extract_title(sections: dict[str, str]) -> str:
    raw = sections.get("TITLE", "").strip()
    if not raw:
        return "[title not found in OCR]"
    return re.sub(r"\s+", " ", raw)


def extract_snippets(sections: dict[str, str], tokens: list[str], limit: int = 3) -> list[str]:
    token_norm = [normalize(t) for t in tokens]
    snippets: list[str] = []
    seen = set()
    section_order = ["ABSTRACT", "INTRODUCTION", "DISCUSSION", "RESULTS", "METHODS"]
    for sec in section_order:
        body = sections.get(sec, "")
        if not body:
            continue
        for sentence in split_sentences(body):
            norm = normalize(sentence)
            if any(tok in norm for tok in token_norm):
                key = norm[:240]
                if key not in seen:
                    seen.add(key)
                    snippets.append(sentence)
                    if len(snippets) >= limit:
                        return snippets
    if snippets:
        return snippets
    for sec in section_order:
        body = sections.get(sec, "")
        if not body:
            continue
        for sentence in split_sentences(body):
            if len(sentence) > 30:
                snippets.append(sentence)
                if len(snippets) >= limit:
                    return snippets
    return snippets


def reg_fonts() -> tuple[str, str, str, str]:
    font_dir = Path("/usr/share/fonts/truetype/dejavu")
    regular = str(font_dir / "DejaVuSans.ttf")
    bold = str(font_dir / "DejaVuSans-Bold.ttf")
    italic = str(font_dir / "DejaVuSans-Oblique.ttf")
    bold_italic = str(font_dir / "DejaVuSans-BoldOblique.ttf")
    pdfmetrics.registerFont(TTFont("DejaVuSans", regular))
    pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", bold))
    pdfmetrics.registerFont(TTFont("DejaVuSans-Oblique", italic))
    pdfmetrics.registerFont(TTFont("DejaVuSans-BoldOblique", bold_italic))
    return "DejaVuSans", "DejaVuSans-Bold", "DejaVuSans-Oblique", "DejaVuSans-BoldOblique"


def make_styles(font_regular: str, font_bold: str, font_italic: str) -> dict[str, ParagraphStyle]:
    sample = getSampleStyleSheet()
    sample.add(ParagraphStyle(name="DocTitle", parent=sample["Title"], fontName=font_bold, fontSize=18, leading=22, alignment=TA_CENTER, spaceAfter=12))
    sample.add(ParagraphStyle(name="DocSubTitle", parent=sample["Normal"], fontName=font_regular, fontSize=10.5, leading=13, alignment=TA_CENTER, spaceAfter=10))
    sample.add(ParagraphStyle(name="H1", parent=sample["Heading1"], fontName=font_bold, fontSize=14, leading=17, spaceAfter=8, spaceBefore=6))
    sample.add(ParagraphStyle(name="H2", parent=sample["Heading2"], fontName=font_bold, fontSize=11.5, leading=14, spaceAfter=5, spaceBefore=5))
    sample.add(ParagraphStyle(name="Body", parent=sample["Normal"], fontName=font_regular, fontSize=9.2, leading=12))
    sample.add(ParagraphStyle(name="BodySmall", parent=sample["Normal"], fontName=font_regular, fontSize=8.1, leading=10))
    sample.add(ParagraphStyle(name="BodyItalic", parent=sample["Normal"], fontName=font_italic, fontSize=9.1, leading=12))
    sample.add(ParagraphStyle(name="Tiny", parent=sample["Normal"], fontName=font_regular, fontSize=7.5, leading=9))
    return {
        "title": sample["DocTitle"],
        "subtitle": sample["DocSubTitle"],
        "h1": sample["H1"],
        "h2": sample["H2"],
        "body": sample["Body"],
        "body_small": sample["BodySmall"],
        "italic": sample["BodyItalic"],
        "tiny": sample["Tiny"],
    }


def raw_paragraph(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text, style)


def p(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(escape(text), style)


def bullet_paragraph(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(f"• {escape(text)}", style)


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("DejaVuSans", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawRightString(doc.pagesize[0] - doc.rightMargin, 0.45 * inch, f"Page {canvas.getPageNumber()}")
    canvas.restoreState()


def load_posters(source_dir: Path) -> dict[str, dict[str, Any]]:
    posters: dict[str, dict[str, Any]] = {}
    for txt in sorted(source_dir.glob("*.txt")):
        sections = parse_sections(txt.read_text(errors="ignore"))
        posters[txt.name] = {
            "file": txt.name,
            "title": extract_title(sections),
            "sections": sections,
        }
    return posters


def make_summary_table_rows(posters: list[dict[str, Any]]) -> list[list[Any]]:
    rows = [[p("Category", styles["body"]), p("Definition", styles["body"]), p("Count", styles["body"]), p("Posters", styles["body"])] ]
    by_cat = defaultdict(list)
    for item in posters:
        by_cat[item["category"]].append(item)
    for key in ["disease_model", "metabolism", "neurobiology", "basic_biology", "defense", "other"]:
        info = CATEGORY_INFO[key]
        items = by_cat.get(key, [])
        poster_lines = "<br/>".join(escape(it['file']) for it in items) if items else "—"
        rows.append([
            p(info["label"], styles["body_small"]),
            p(info["definition"], styles["body_small"]),
            p(str(len(items)), styles["body_small"]),
            raw_paragraph(poster_lines, styles["body_small"]),
        ])
    return rows


def build_motivation_pdf(output_path: Path, annotated_posters: list[dict[str, Any]], source_files: dict[str, dict[str, Any]]) -> None:
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        leftMargin=0.65 * inch,
        rightMargin=0.65 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
        title="Thematic analysis of poster motivation",
        author="Zo Computer",
    )
    story: list[Any] = []
    story.append(p("Thematic Analysis Report 1: Poster Motivation", styles["title"]))
    story.append(p("Raw OCR poster text from Documents/OCR 1.1/Raw; authors and references were ignored.", styles["subtitle"]))
    story.append(p("Categories were defined after reviewing the full poster set so the analysis does not depend on poster order.", styles["body"]))
    story.append(Spacer(1, 0.14 * inch))
    story.append(p("1) Category summary", styles["h1"]))

    table = Table(make_summary_table_rows(annotated_posters), colWidths=[1.5 * inch, 2.35 * inch, 0.45 * inch, 2.45 * inch], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "DejaVuSans-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "DejaVuSans"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.1),
        ("LEADING", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#94a3b8")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.HexColor("#eef2ff")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.18 * inch))
    story.append(p("2) Poster-by-poster evidence", styles["h1"]))

    for item in annotated_posters:
        file_info = source_files[item["file"]]
        sections = file_info["sections"]
        title = file_info["title"]
        category = CATEGORY_INFO[item["category"]]["label"]
        story.append(p(f"{item['file']} — {title}", styles["h2"]))
        story.append(p(f"Assigned category: {category}", styles["body_small"]))
        story.append(p(f"Definition: {CATEGORY_INFO[item['category']]['definition']}", styles["body_small"]))
        if item.get("notes"):
            story.append(p(f"Note: {item['notes']}", styles["italic"]))
        snippets = extract_snippets(sections, item["evidence_tokens"], limit=3)
        if snippets:
            story.append(p("Evidence from the poster text:", styles["body_small"]))
            story.append(ListFlowable([bullet_paragraph(sn, styles["body_small"]) for sn in snippets], bulletType="bullet", start="bullet", leftIndent=12))
        else:
            story.append(p("Evidence from the poster text: no matching sentence could be automatically extracted, so the category was assigned from the overall poster theme.", styles["body_small"]))
        if item["category"] == "other":
            story.append(p("Other category note: this poster would have been placed in a more specific category if a stronger thematic match existed.", styles["body_small"]))
        story.append(Spacer(1, 0.12 * inch))

    if not any(poster["category"] == "other" for poster in annotated_posters):
        story.append(PageBreak())
        story.append(p("Other category", styles["h1"]))
        story.append(p("No posters were assigned to Other; every poster fit one of the five main categories.", styles["body"]))

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)


def build_disease_pdf(output_path: Path, annotated_posters: list[dict[str, Any]], source_files: dict[str, dict[str, Any]]) -> None:
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        leftMargin=0.6 * inch,
        rightMargin=0.6 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch,
        title="Human disease mention analysis",
        author="Zo Computer",
    )
    story: list[Any] = []
    story.append(p("Thematic Analysis Report 2: Human Disease Mentions", styles["title"]))
    story.append(p("This report lists every poster and the exact disease wording that appears in the raw OCR text. Posters with no explicit human disease mention are included as well.", styles["subtitle"]))
    story.append(p("Broader disease-state categories overlap, so a poster can appear in more than one category.", styles["body"]))
    story.append(Spacer(1, 0.1 * inch))
    story.append(p("1) Poster-to-disease table", styles["h1"]))

    rows = [[p("Poster", styles["body"]), p("Human disease wording found in the text", styles["body"]), p("Broad disease-state category", styles["body"])] ]
    for item in annotated_posters:
        disease_text = "; ".join(item["diseases"]) if item["diseases"] else "No human disease explicitly named"
        broad = "; ".join(BROAD_DISEASE_INFO[key] for key in item["broad_categories"])
        if not broad:
            broad = "—"
        rows.append([
            p(item['file'], styles["body_small"]),
            p(disease_text, styles["body_small"]),
            p(broad, styles["body_small"]),
        ])
    table = Table(rows, colWidths=[2.35 * inch, 2.65 * inch, 1.85 * inch], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "DejaVuSans-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "DejaVuSans"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.0),
        ("LEADING", (0, 0), (-1, -1), 9.8),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#94a3b8")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.HexColor("#eef2ff")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.18 * inch))
    story.append(p("2) Broader disease-state analysis", styles["h1"]))

    cat_counts = Counter()
    cat_posters = defaultdict(list)
    disease_poster_count = 0
    for item in annotated_posters:
        if item["diseases"]:
            disease_poster_count += 1
        for key in item["broad_categories"]:
            cat_counts[key] += 1
            cat_posters[key].append(item["file"])

    broad_rows = [[p("Broad disease-state category", styles["body"]), p("Posters", styles["body"]), p("Count", styles["body"]), p("Percent of all 27 posters", styles["body"])] ]
    total = len(annotated_posters)
    for key in ["metabolic_digestive", "neuro", "genetic", "cardio", "cancer", "pigment"]:
        count = cat_counts.get(key, 0)
        percent = (count / total) * 100 if total else 0
        poster_lines = "<br/>".join(escape(name) for name in cat_posters.get(key, [])) if cat_posters.get(key) else "—"
        broad_rows.append([
            p(BROAD_DISEASE_INFO[key], styles["body_small"]),
            raw_paragraph(poster_lines, styles["body_small"]),
            p(str(count), styles["body_small"]),
            p(f"{percent:.1f}%", styles["body_small"]),
        ])
    broad_table = Table(broad_rows, colWidths=[2.15 * inch, 2.95 * inch, 0.55 * inch, 1.2 * inch], repeatRows=1)
    broad_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "DejaVuSans-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "DejaVuSans"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.2),
        ("LEADING", (0, 0), (-1, -1), 9.8),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#94a3b8")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.HexColor("#eef2ff")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(broad_table)
    story.append(Spacer(1, 0.12 * inch))
    story.append(p(f"{disease_poster_count} of {total} posters explicitly named at least one human disease term in the raw text.", styles["body_small"]))
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)


def build_technical_pdf(output_path: Path, prompt_text: str, source_files: dict[str, dict[str, Any]], output_names: list[str]) -> None:
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        leftMargin=0.65 * inch,
        rightMargin=0.65 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
        title="Technical analysis summary",
        author="Zo Computer",
    )
    story: list[Any] = []
    story.append(p("Thematic Analysis Report 3: Technical Summary", styles["title"]))
    story.append(p("This report documents the method, software, AI model, and the exact user prompt used for the analysis.", styles["subtitle"]))

    story.append(p("Method", styles["h1"]))
    story.append(p("Raw OCR text files were read from Documents/OCR 1.1/Raw. The analysis ignored author and reference sections, parsed the remaining poster text into sections, and assigned one motivation category per poster using a fixed set of categories defined after reviewing the full poster set. Disease mentions were captured as exact wording from the raw text and then grouped into broader disease-state categories.", styles["body"]))
    story.append(Spacer(1, 0.08 * inch))

    story.append(p("Software and model", styles["h1"]))
    software_rows = [
        [p("AI model", styles["body"]), p("GPT-5.4 mini", styles["body"])],
        [p("Python", styles["body"]), p(f"{sys_version()}", styles["body"])],
        [p("reportlab", styles["body"]), p(reportlab_version(), styles["body"])],
        [p("pandoc", styles["body"]), p(pandoc_version(), styles["body"])],
        [p("Source files", styles["body"]), p(f"{len(source_files)} raw poster text files from Documents/OCR 1.1/Raw", styles["body"])],
    ]
    sw_table = Table(software_rows, colWidths=[1.5 * inch, 4.55 * inch])
    sw_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#94a3b8")),
        ("FONTNAME", (0, 0), (-1, -1), "DejaVuSans"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.1),
        ("LEADING", (0, 0), (-1, -1), 11),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(sw_table)
    story.append(Spacer(1, 0.12 * inch))

    story.append(p("Prompt used", styles["h1"]))
    for para in prompt_text.strip().split("\n\n"):
        para = para.strip()
        if para:
            story.append(p(para.replace("\n", " "), styles["body_small"]))
            story.append(Spacer(1, 0.05 * inch))

    story.append(Spacer(1, 0.05 * inch))
    story.append(p("Output files", styles["h1"]))
    for name in output_names:
        story.append(p(name, styles["body_small"]))

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)


def sys_version() -> str:
    import sys

    return sys.version.replace("\n", " ")


def reportlab_version() -> str:
    import reportlab

    return reportlab.Version


def pandoc_version() -> str:
    import subprocess

    try:
        out = subprocess.check_output(["pandoc", "--version"], text=True, stderr=subprocess.DEVNULL)
        return out.splitlines()[0].strip()
    except Exception:
        return "not available"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate PDF reports from OCR poster text files.")
    parser.add_argument("--source-dir", default=None, help="Directory containing raw OCR txt files.")
    parser.add_argument("--output-dir", default=None, help="Directory to write the PDFs into.")
    parser.add_argument("--prompt-file", default=None, help="Text file containing the full user prompt.")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    source_dir = Path(args.source_dir) if args.source_dir else script_dir.parent / "Raw"
    output_dir = Path(args.output_dir) if args.output_dir else script_dir
    prompt_file = Path(args.prompt_file) if args.prompt_file else script_dir / "analysis_prompt.txt"

    output_dir.mkdir(parents=True, exist_ok=True)

    font_regular, font_bold, font_italic, _ = reg_fonts()
    global styles
    styles = make_styles(font_regular, font_bold, font_italic)

    source_files = load_posters(source_dir)
    source_lookup = source_files

    annotated_posters = []
    for item in POSTERS:
        if item["file"] not in source_lookup:
            raise FileNotFoundError(f"Missing expected raw file: {item['file']}")
        annotated_posters.append(item)

    prompt_text = prompt_file.read_text(encoding="utf-8")

    motivation_pdf = output_dir / "motivation_thematic_analysis.pdf"
    disease_pdf = output_dir / "disease_thematic_analysis.pdf"
    technical_pdf = output_dir / "technical_report.pdf"

    build_motivation_pdf(motivation_pdf, annotated_posters, source_lookup)
    build_disease_pdf(disease_pdf, annotated_posters, source_lookup)
    build_technical_pdf(technical_pdf, prompt_text, source_lookup, [motivation_pdf.name, disease_pdf.name, technical_pdf.name])

    manifest = {
        "source_dir": str(source_dir),
        "output_dir": str(output_dir),
        "source_files": sorted(source_lookup.keys()),
        "outputs": [str(motivation_pdf), str(disease_pdf), str(technical_pdf)],
        "poster_count": len(annotated_posters),
        "disease_named_count": sum(1 for item in annotated_posters if item["diseases"]),
        "category_counts": Counter(item["category"] for item in annotated_posters),
    }
    (output_dir / "analysis_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
