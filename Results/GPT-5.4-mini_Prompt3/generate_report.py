from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
from textwrap import fill
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUT_DIR = Path(__file__).resolve().parent
MD_PATH = OUT_DIR / "thematic_analysis_report.md"
PDF_PATH = OUT_DIR / "thematic_analysis_report.pdf"

CATEGORIES = [
    "Basic biology (Neurology)",
    "Basic biology (Metabolism)",
    "Basic biology (Other)",
    "Disease research (Neurology)",
    "Disease research (Metabolism)",
    "Disease research (Other)",
    "Other",
]

POSTERS = [
    {
        "file": "Avetisyan et al. (2023) - CCC SP23.txt",
        "category": "Disease research (Neurology)",
        "note": "Named autism-related genes and a gut-brain-axis framing make the disease motivation dominant.",
        "evidence": [
            "Abstract: 'Genes such as dve, KCNQ, Ssadh, Hem, ebi, and glo ... have been identified as autism related.'",
            "Introduction: 'The Gut-microbiome-brain axis (GUMBA)... has linked disorders such as Autism (ASD) to genes expressed within the midgut.'",
            "Introduction: 'When communication between the midgut and the brain is disrupted, there is a higher probability of autism.'",
            "Discussion: the poster links the results to 'genes, expressed in both the central nervous system and midgut'.",
        ],
    },
    {
        "file": "Berbouti et al. (2025) - CCC FA25.txt",
        "category": "Basic biology (Metabolism)",
        "note": "A digestion/energy-metabolism poster about trehalose breakdown and region-specific expression.",
        "evidence": [
            "Title: 'Trehalase Expression in the Drosophila Midgut'.",
            "Abstract: 'Trehalose is a critical sugar... in which its breakdown by trehalase provides glucose for energy metabolism.'",
            "Introduction: 'Trehalose is a major sugar in insects. TREH breaks trehalose into glucose in the Drosophila midgut.'",
            "Discussion: 'local metabolic or metal handling functions' and 'glucose transporter ... enriched in the far posterior digestive regions'.",
        ],
    },
    {
        "file": "Brown et al. (2025) - CCC SP25.txt",
        "category": "Disease research (Metabolism)",
        "note": "The poster is driven by acid reflux, a digestive disorder, even though it also uses gut-brain signaling language.",
        "evidence": [
            "Title: 'Analysis Of Gene Expression Of Acids Reflux Related Genes Across The Midgut'.",
            "Introduction: 'Acid reflux is a condition shown in millions of people in the world'.",
            "Introduction: 'To better comprehend the molecular mechanisms behind this condition'.",
            "Discussion: 'effects of acid reflux are influenced by genetic factors' and the work focuses on 'human-relevant genes associated with this condition'.",
        ],
    },
    {
        "file": "Cabral et al. (2025) - CCC FA25.txt",
        "category": "Disease research (Neurology)",
        "note": "MECP2, Rett syndrome, and neurodevelopmental dysfunction make this clearly disease-driven.",
        "evidence": [
            "Abstract: 'The methyl-CpG binding protein 2 (MECP2) gene is essential for neuronal nervous system.'",
            "Abstract: 'Mutations in MECP2 are linked to Rett syndrome and related neurodevelopmental disorders'.",
            "Introduction: 'MECP2 dysfunction is known to cause Rett syndrome and contribute to a range of neurological impairments'.",
            "Discussion: 'Because MECP2 is expressed across the brain, its loss disrupts activity'.",
        ],
    },
    {
        "file": "Camara et al. (2025) - LU SP25.txt",
        "category": "Basic biology (Metabolism)",
        "note": "The central question is how amylase genes support digestion across gut regions; disease references are secondary.",
        "evidence": [
            "Title: 'Functional Difference Between Amy-D, Amy-P and Amyrel in Drosophila Midgut'.",
            "Introduction: 'The Drosophila midgut has distinct regions and pH zones that may affect enzyme activity.'",
            "Introduction: the genes 'are orthologs to human amylases' and are tied only secondarily to 'diseases like diabetes and Alzheimer’s'.",
            "Discussion: 'specialization of enzyme function along the midgut' and 'overlapping roles in digestion'.",
        ],
    },
    {
        "file": "Dehuelbes et al. (2025) - LU SP5.txt",
        "category": "Basic biology (Metabolism)",
        "note": "Energy homeostasis, fatty-acid metabolism, and feeding behavior dominate; no named disease is the main driver.",
        "evidence": [
            "Title: 'Regional Expression of Key Metabolic genes in Drosophila Midgut'.",
            "Introduction: 'Acetyl-CoA links carbohydrate, fat, & protein metabolism'.",
            "Introduction: 'CRAT is a mitochondrial enzyme involved in fatty acid metabolism' and 'may influence feeding behavior'.",
            "Discussion: 'Explore CRAT as a potential target for treating metabolic disorders in humans' is framed as a downstream implication rather than the core motivation.",
        ],
    },
    {
        "file": "Diaz et al. (2025) - CCC SP25.txt",
        "category": "Basic biology (Other)",
        "note": "This is about immune-defense biology and phagosome acidification, not a named disease model.",
        "evidence": [
            "Title: 'V-ATPase Gene Expression Reveals Cellular Defense Zones'.",
            "Abstract: 'To explore how different regions ... contribute to immune defense'.",
            "Introduction: 'Phagosomes are part of the cell’s internal defense and cleanup system'.",
            "Discussion: the Cu region 'contributes to immune defense by nurturing an acidic environment'.",
        ],
    },
    {
        "file": "Ford et al. (2023) - CCC SP23.txt",
        "category": "Basic biology (Other)",
        "note": "An environmental-response / xenobiotic-metabolism poster rather than a disease poster.",
        "evidence": [
            "Title: 'Cytochrome P450 genes providing insecticide resistance'.",
            "Abstract: 'Some Cytochrome P450 genes play an important role in the development of insecticide resistance'.",
            "Introduction: 'the Drosophila melanogaster midgut is used as a model system for studying human gut function'.",
            "Discussion: 'genes involved in insecticide resistance ... are most highly expressed'.",
        ],
    },
    {
        "file": "Gill & Alcazar (2025) - CCC FA25.txt",
        "category": "Disease research (Neurology)",
        "note": "The explicit disease framing is Parkinson’s and broader neuropsychiatric disorders.",
        "evidence": [
            "Title: 'Differential Expression of Serotonin Receptor Genes Htrla and Htr2a in the Prefrontal Cortex and Striatum'.",
            "Abstract: 'related to the neuropsychiatric disorder Parkinson's Disease'.",
            "Introduction: 'Many neuropsychiatric disorders including Parkinson's Disease, Schizophrenia, and Post-traumatic Stress Disorder'.",
            "Discussion: 'stronger serotonergic signaling in the PFC circuits which are involved in cognition and emotional regulation'.",
        ],
    },
    {
        "file": "Godoy-Pena et al. (2025) - CCC FA25.txt",
        "category": "Basic biology (Neurology)",
        "note": "Sleep/circadian behavior and gut-brain signaling are the main focus, not a named disorder.",
        "evidence": [
            "Title: 'Regulation of Sleep Quality: Analysis of Gene Expression'.",
            "Abstract: 'determine what genes dictate the kind of sleep drosophila flies get'.",
            "Abstract: 'genes known to influence the drosophila fly's circadian rhythm'.",
            "Introduction: 'Sleep and diet play crucial roles in human health' and the study is aimed at sleep-quality genetics.",
        ],
    },
    {
        "file": "Haubelt & Alcazar et al. (2025) - CCC FA25.txt",
        "category": "Disease research (Neurology)",
        "note": "Parkinson’s disease is named directly and drives the whole analysis of the dopaminergic synapse.",
        "evidence": [
            "Title: 'Exploring DRD2: The Association of PD Risk with Dopamine Receptors'.",
            "Abstract: 'related to the neuropsychiatric disorder Parkinson's Disease'.",
            "Introduction: 'Many neuropsychiatric disorders including Parkinson's Disease... are seen to have direct correlation to dopamine receptor D2'.",
            "Discussion: the poster links striatal dopamine pathways to Parkinson's symptoms such as tremor and rigidity."
        ],
    },
    {
        "file": "Henriquez et al. (2025) - COD WI24.txt",
        "category": "Basic biology (Other)",
        "note": "A core physiology / immune-pathway expression study; disease relevance is only secondary.",
        "evidence": [
            "Title: '6 Immune Pathways Exhibit Similar Patterns of Gene Expressions in Drosophila melanogaster Midgut'.",
            "Abstract: 'Measurement of gene expression in six immune pathways... suggests similar levels of immune pathway protein expression'.",
            "Introduction: 'The specific functions that each region performs have not been thoroughly characterized'.",
            "Introduction: disease references such as Crohn's disease are presented as possible broader relevance, not the main motivation.",
        ],
    },
    {
        "file": "Holmes (2025) - CCC SP25.txt",
        "category": "Basic biology (Other)",
        "note": "A melanogenesis/pigmentation project that only later connects to Parkinson’s and neurodegeneration.",
        "evidence": [
            "Title: 'Melanogenesis within the Drosophila Midgut: Neuromelanin and Dopamine'.",
            "Abstract: 'focused in genes connected to melanogenesis (synthesis of melanin) and its antioxidant uses'.",
            "Abstract: the yellow gene is discussed for pigmentation and mating behavior, not a disease model.",
            "Discussion: Parkinson's appears as a downstream implication of dysregulated neuromelanin rather than the main research driver.",
        ],
    },
    {
        "file": "Lemus et al. (2025) - FA25 CCC.txt",
        "category": "Basic biology (Metabolism)",
        "note": "This is a carbohydrate digestion / absorption study with human digestive relevance.",
        "evidence": [
            "Title: 'Macromolecule Breakdown and Absorption'.",
            "Abstract: 'Understanding differential gene expression... can uncover processes relevant to human digestion as well as metabolic disorders'.",
            "Introduction: the anterior region is 'tasked with macromolecule breakdown' and the posterior region 'controls molecule absorption'.",
            "Discussion: the work examines 'starch and sucrose' digestion and regional nutrient absorption.",
        ],
    },
    {
        "file": "Logan et al. (2025) - CCC FA25.txt",
        "category": "Disease research (Other)",
        "note": "The project is explicitly about cardiovascular disease and ACE-related human pathology, not neurology or metabolism.",
        "evidence": [
            "Abstract: 'cardiovascular-related pathways and potential therapeutic directions'.",
            "Introduction: 'Cardiovascular disorders are a prominent and widespread disease'.",
            "Introduction: the human ACE gene is 'a critical regulator of blood pressure and fluid balance'.",
            "Discussion: the poster frames the work as insight into 'human cardiovascular disease'.",
        ],
    },
    {
        "file": "Luera et al. (2025) - CCC FA25.txt",
        "category": "Basic biology (Neurology)",
        "note": "This is fundamentally a neuropeptide / feeding-behavior poster about the gut-brain axis.",
        "evidence": [
            "Title: 'Region-Specific NPF/NPFR Signaling in the Drosophila Midgut'.",
            "Abstract: 'explore their role in gut-mediated feeding behavior'.",
            "Introduction: 'Neuropeptide F (NPF) is a conserved neuropeptide that regulates feeding, stress, and sleep behaviors'.",
            "Discussion: 'local paracrine signaling' and 'feeding regulation' dominate the motivation.",
        ],
    },
    {
        "file": "Meraz et al. (2023) - CCC SP23.txt",
        "category": "Basic biology (Other)",
        "note": "This is a gene-function / tissue-patterning poster built around tyrosine kinase expression and cell growth.",
        "evidence": [
            "Title: 'Tyrosine Kinase Expression in the Midgut Suggests a Role in the Copper Region'.",
            "Abstract: 'Tyrosine kinases are enzymes related to cell growth and development'.",
            "Introduction: the midgut expression pattern is used to infer gene function across subregions.",
            "Discussion: the poster concludes that the genes 'have high specificity to the Cu region of the midgut'.",
        ],
    },
    {
        "file": "Nii et al. (2025) - CCC FA25.txt",
        "category": "Basic biology (Metabolism)",
        "note": "The center of gravity is iron-dependent regulation of fatty-acid synthesis and energy storage.",
        "evidence": [
            "Title: 'Iron-Induced Modulation of Acetyl-CoA Carboxylase (ACC)... Impacts on Lipid Metabolism and Energy Storage'.",
            "Abstract: 'ACC is the rate limiting enzyme that converts acetyl-CoA to malonyl-CoA, committing cells to fatty acid synthesis'.",
            "Introduction: 'Iron is an essential micronutrient... [that] can disrupt oxidative balance and alter key metabolic pathways'.",
            "Discussion: 'ACC expression is strongly enriched in the Fe region... associated with iron absorption and metal handling'.",
        ],
    },
    {
        "file": "Otala et al. (2025) - LU SP25.txt",
        "category": "Disease research (Metabolism)",
        "note": "The title and introduction explicitly make this a model for fatty-acid metabolism disorders.",
        "evidence": [
            "Title: 'Fly Gut is a good model for fatty acid metabolism disorders'.",
            "Introduction: 'Related disorders and symptoms include: MCADD and Carnitine transporter deficiency, hypoglycemia, liver dysfunction, and muscle weakness'.",
            "Introduction: 'ACOX3 breaks down very long-chain fatty acids... dysfunction may lead to fat accumulation, liver disease, and inflammation'.",
            "Discussion: links Acox3 to 'nutrient absorption and waste management' in the context of metabolic disorders.",
        ],
    },
    {
        "file": "Paderna et al. (2025) - CCC SP25.txt",
        "category": "Disease research (Other)",
        "note": "The poster is driven by albinism / melanogenesis, which is a named disorder but not a neurology or metabolism category.",
        "evidence": [
            "Title: 'Albinism and Melanogenesis Pathway'.",
            "Abstract: 'In humans, the gene SLC45A2 is associated with oculocutaneous albinism type 4'.",
            "Introduction: 'OCA4 can result from mutations in the gene SLC45A2'.",
            "Discussion: the poster keeps returning to 'melanin synthesis' and albinism-linked human genetics.",
        ],
    },
    {
        "file": "Paramo-Ojeda et al. (2025) - CCC SP25.txt",
        "category": "Disease research (Other)",
        "note": "This is a classic cancer-motivation poster centered on KRAS-driven colon cancer.",
        "evidence": [
            "Title: 'Ras85D Expression in Drosophila Midgut Highlights a Model for KRAS-Driven Colon Cancer'.",
            "Abstract: 'KRAS mutations drive many human cancers by promoting uncontrolled cell growth'.",
            "Introduction: 'Cancer is a complex disease driven by mutations in genes that regulate cell growth, survival, and DNA repair'.",
            "Discussion: the work frames Ras85D as a model for 'tumor initiation'.",
        ],
    },
    {
        "file": "Pedireddi et al. (2025) - CCC SP25.txt",
        "category": "Basic biology (Metabolism)",
        "note": "This is a carbohydrate-digestion poster, not a disease poster.",
        "evidence": [
            "Title: 'Beyond the Anterior: Amylase Gene Expression Suggests Widespread Polysaccharide Digestion'.",
            "Abstract: 'interested in genes involved in sugar metabolism'.",
            "Introduction: the project studies 'how Drosophila melanogaster digested polysaccharides'.",
            "Discussion: 'breakdown of polysaccharides' and 'nutrient absorption' are the central themes.",
        ],
    },
    {
        "file": "Rodriguez (2025) - CCC SP25.txt",
        "category": "Disease research (Metabolism)",
        "note": "Galactosemia is a named metabolic disorder and is the direct motivation for the work.",
        "evidence": [
            "Title: 'Differential Gene Expression of Galm1 in the Drosophila Midgut'.",
            "Abstract: 'Mutations in... GALM, are associated with the disease galactosemia'.",
            "Introduction: 'Galactosemia is a rare metabolic disorder'.",
            "Discussion: 'areas such as the p2_4 region in Drosophila and the kidneys in humans, are at a greater risk for damaging mutations'.",
        ],
    },
    {
        "file": "Sakana et al. (2025) - CCC SP25.txt",
        "category": "Basic biology (Other)",
        "note": "Developmental patterning and transcription-factor control are the core themes.",
        "evidence": [
            "Title: 'Differential Expression of the TALE Homeobox Genes in Drosophila Midgut patterning'.",
            "Abstract: 'TALE group of homeobox genes regulate cell and tissue-specific gene expression'.",
            "Introduction: 'homothorax ... known for its role in tissue patterning, stem cell maintenance, and organ development'.",
            "Discussion: 'Genes coding for homeodomain transcription factors play a key role in gene expression control'.",
        ],
    },
    {
        "file": "Trevino et al. (2022) - CCC SP22.txt",
        "category": "Disease research (Metabolism)",
        "note": "Zellweger Spectrum Disorder is a named metabolic/peroxisomal disorder and remains the main motivation.",
        "evidence": [
            "Title: 'Drosophila Melanogaster a Good Model System of Zellweger Spectrum Disorder'.",
            "Abstract: 'Zellweger Spectrum Disorder (ZSD) is a genetic disorder'.",
            "Introduction: 'ZSD is a rare inherited disorder characterized by the absence/reduction of functional peroxisomes'.",
            "Introduction: 'essential for beta-oxidation of very-long-chain fatty acids' and 'metabolic abnormalities'.",
        ],
    },
    {
        "file": "Tuttle et al. (2025) - CCC SP25.txt",
        "category": "Basic biology (Metabolism)",
        "note": "A metabolism / aging / pigmentation pathway study, not a disease model.",
        "evidence": [
            "Title: 'Gene Expression Patterns in the Tryptophan-Kynurenine Pathway'.",
            "Abstract: 'genes regulating Tryptophan and its metabolism pathways'.",
            "Introduction: 'tryptophan is metabolized through the kynurenine pathway'.",
            "Discussion: the project emphasizes 'regional specialization in TRY processing' and links to aging and energy metabolism.",
        ],
    },
    {
        "file": "Zlaket et al. (2023) - CCC SP23.txt",
        "category": "Disease research (Metabolism)",
        "note": "A peroxisomal / lipid-metabolism disease framing anchored by Zellweger syndrome.",
        "evidence": [
            "Title: 'ScpX: A Peroxisomal Gene and its Distinctive Paralogs'.",
            "Introduction: 'Errors within this gene can cause Zellweger's Syndrome'.",
            "Introduction: the gene functions in 'oxidation of fatty acid chains within peroxisomes' and cholesterol transport."
            ,"Discussion: the research links ScpX/paralogs to 'peroxisomal function' and lipid/sterol pathways.",
        ],
    },
]


def md_escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def build_markdown() -> str:
    counts = Counter(item["category"] for item in POSTERS)
    grouped = defaultdict(list)
    for item in POSTERS:
        grouped[item["category"]].append(item["file"])

    lines: list[str] = []
    lines.append("# Thematic analysis of 27 OCR posters")
    lines.append("")
    lines.append("Raw text files were analyzed. Author and reference sections were ignored.")
    lines.append("")
    lines.append("## Category summary")
    lines.append("")
    lines.append("| Category | Count | Posters |")
    lines.append("| --- | ---: | --- |")
    for cat in CATEGORIES:
        posters = grouped.get(cat, [])
        poster_text = "; ".join(md_escape(x) for x in posters) if posters else "—"
        lines.append(f"| {cat} | {counts.get(cat, 0)} | {poster_text} |")
    lines.append("")
    lines.append("## Poster-by-poster evidence")
    lines.append("")
    for item in POSTERS:
        lines.append(f"### {item['file']}")
        lines.append("")
        lines.append(f"**Category:** {item['category']}")
        if item.get("note"):
            lines.append("")
            lines.append(f"**Note:** {item['note']}")
        lines.append("")
        lines.append("**Evidence from the poster:**")
        for bullet in item["evidence"]:
            lines.append(f"- {bullet}")
        lines.append("")
    lines.append("## Summary note")
    lines.append("")
    lines.append("No poster was assigned to the catch-all **Other** category; all 27 fit one of the six substantive categories above.")
    lines.append("")
    return "\n".join(lines)


def make_pdf(md: str) -> None:
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="TitleCenter", parent=styles["Title"], alignment=TA_CENTER, fontSize=18, leading=22, spaceAfter=12))
    styles.add(ParagraphStyle(name="BodySmall", parent=styles["BodyText"], fontSize=8.5, leading=11, spaceAfter=4))
    styles.add(ParagraphStyle(name="Section", parent=styles["Heading2"], fontSize=13, leading=16, spaceBefore=10, spaceAfter=6))
    styles.add(ParagraphStyle(name="PosterTitle", parent=styles["Heading3"], fontSize=11, leading=13, spaceBefore=8, spaceAfter=4))
    styles.add(ParagraphStyle(name="PosterMeta", parent=styles["BodyText"], fontSize=8.5, leading=10.5, leftIndent=6, spaceAfter=2))

    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=LETTER,
        rightMargin=0.55 * inch,
        leftMargin=0.55 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.55 * inch,
    )

    story = []
    story.append(Paragraph("Thematic analysis of 27 OCR posters", styles["TitleCenter"]))
    story.append(Paragraph("Raw text files were analyzed. Author and reference sections were ignored.", styles["BodySmall"]))
    story.append(Spacer(1, 8))

    counts = Counter(item["category"] for item in POSTERS)
    grouped = defaultdict(list)
    for item in POSTERS:
        grouped[item["category"]].append(item["file"])

    story.append(Paragraph("Category summary", styles["Section"]))
    table_data = [[Paragraph("Category", styles["BodySmall"]), Paragraph("Count", styles["BodySmall"]), Paragraph("Posters", styles["BodySmall"] )]]
    for cat in CATEGORIES:
        posters = grouped.get(cat, [])
        poster_text = "; ".join(escape(x) for x in posters) if posters else "—"
        table_data.append([
            Paragraph(escape(cat), styles["BodySmall"]),
            Paragraph(str(counts.get(cat, 0)), styles["BodySmall"]),
            Paragraph(poster_text, styles["BodySmall"]),
        ])
    tbl = Table(table_data, colWidths=[1.9 * inch, 0.5 * inch, 4.95 * inch], repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e5e7eb")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#cbd5e1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.2),
        ("LEADING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Poster-by-poster evidence", styles["Section"]))
    for item in POSTERS:
        story.append(Paragraph(escape(item["file"]), styles["PosterTitle"]))
        story.append(Paragraph(f"<b>Category:</b> {escape(item['category'])}", styles["PosterMeta"]))
        if item.get("note"):
            story.append(Paragraph(f"<b>Note:</b> {escape(item['note'])}", styles["PosterMeta"]))
        bullets = [ListItem(Paragraph(escape(b), styles["PosterMeta"])) for b in item["evidence"]]
        story.append(ListFlowable(bullets, bulletType="bullet", start="bullet", leftIndent=14))

    story.append(Spacer(1, 8))
    story.append(Paragraph("No poster was assigned to the catch-all Other category; all 27 fit one of the six substantive categories above.", styles["BodySmall"]))

    doc.build(story)


def main() -> None:
    md = build_markdown()
    MD_PATH.write_text(md)
    make_pdf(md)
    print(MD_PATH)
    print(PDF_PATH)


if __name__ == "__main__":
    main()
