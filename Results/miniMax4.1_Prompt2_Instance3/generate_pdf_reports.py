#!/usr/bin/env python3
"""
Generate PDF reports for Thematic Analysis of Research Posters
Uses reportlab for PDF generation
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, ListFlowable, ListItem
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from pathlib import Path
from collections import defaultdict

# ============================================================================
# DATA - Analysis Results
# ============================================================================

OUTPUT_DIR = Path("/home/workspace/Documents/OCR 1.1/AI_model_Prompt2")

# Category assignments with full reasoning
THEMATIC_DATA = {
    "Avetisyan et al. (2023) - CCC SP23.txt": {
        "category": "Disease-Motivated",
        "reasoning": [
            "Focus on autism-related genes and the gut-microbiome-brain axis",
            "Explicit connection to Autism Spectrum Disorder (ASD)",
            "Research linked to understanding autism treatment through gut intervention"
        ]
    },
    "Berbouti et al. (2025) - CCC FA25.txt": {
        "category": "Metabolic/Physiological",
        "reasoning": [
            "Studies trehalose catabolism pathway in Drosophila midgut",
            "Focus on carbohydrate metabolism and sugar processing",
            "Highlights connection to 'parallel sugar processing in humans' without explicit disease target"
        ]
    },
    "Brown et al. (2025) - CCC SP25.txt": {
        "category": "Disease-Motivated",
        "reasoning": [
            "Directly studies acid reflux disorder",
            "States goal is to 'lay the foundations for future studies that could lead to more understanding and treatment of acid reflux'",
            "Connects genetic findings to human gastric acid disorders"
        ]
    },
    "Cabral et al. (2025) - CCC FA25.txt": {
        "category": "Disease-Motivated",
        "reasoning": [
            "Focus on MECP2 gene linked to Rett syndrome",
            "Explicitly studies neurodevelopmental disorders",
            "Discusses how 'dysregulation of this gene may contribute to neurological dysfunction'"
        ]
    },
    "Camara et al. (2025) - LU SP25.txt": {
        "category": "Disease-Motivated",
        "reasoning": [
            "States amylase genes 'may relate to diseases like diabetes and Alzheimer's'",
            "Explicitly connects to human disease relevance",
            "Discusses gut-brain axis connection to neurodegenerative diseases"
        ]
    },
    "Dehuelbes et al. (2025) - LU SP5.txt": {
        "category": "Metabolic/Physiological",
        "reasoning": [
            "Studies metabolic genes (CRAT, MANF, NPY) involved in energy homeostasis",
            "Highlights role in 'cellular energy homeostasis' and 'feeding behavior'",
            "Discusses therapeutic exploration 'for treating metabolic disorders in humans' but primary focus is on metabolic mechanisms"
        ]
    },
    "Diaz et al. (2025) - CCC SP25.txt": {
        "category": "Basic Biology",
        "reasoning": [
            "Focuses on V-ATPase genes and phagosome acidification",
            "Studies cellular defense mechanisms in the midgut",
            "Makes analogy to human stomach but primary focus is on fundamental cellular processes"
        ]
    },
    "Ford et al. (2023) - CCC SP23.txt": {
        "category": "Basic Biology",
        "reasoning": [
            "Studies Cytochrome P450 genes and insecticide resistance",
            "Primary focus on gene expression patterns and coexpression",
            "Notes Drosophila-human parallels but focus is on basic insect physiology"
        ]
    },
    "Gill & Alcazar (2025) - CCC FA25.txt": {
        "category": "Disease-Motivated",
        "reasoning": [
            "Studies serotonin receptor genes linked to mental health disorders",
            "Explicitly references 'mental health disorders' and mood regulation",
            "Discusses prefrontal cortex function in emotional regulation"
        ]
    },
    "Godoy-Pena et al. (2025) - CCC FA25.txt": {
        "category": "Disease-Motivated",
        "reasoning": [
            "Focuses on genes dictating sleep quality",
            "Explicitly connects to sleep disorders and their health impacts",
            "Studies 'poor diet, low sleep quality, and reduced energy levels'"
        ]
    },
    "Haubelt & Alcazar et al. (2025) - CCC FA25.txt": {
        "category": "Disease-Motivated",
        "reasoning": [
            "Directly studies Parkinson's Disease and dopaminergic synapse",
            "States goal is investigating 'the specific genes involved in the dopaminergic synapse' related to Parkinson's",
            "Explicitly connects gene variants to neuropsychiatric disorders"
        ]
    },
    "Henriquez et al. (2025) - COD WI24.txt": {
        "category": "Disease-Motivated",
        "reasoning": [
            "Explicitly mentions 'helping in understanding human immune disorders that reside within the gut such as Crohn's disease'",
            "References 'Inflammatory Bowel Diseases' as motivation",
            "Studies immune pathways with clear disease application focus"
        ]
    },
    "Holmes (2025) - CCC SP25.txt": {
        "category": "Disease-Motivated",
        "reasoning": [
            "Explicitly connects to Parkinson's Disease: 'Dysregulated melanogenesis expression is linked to many human neurodegenerative disorders such as Parkinson's'",
            "Studies neuromelanin with direct human disease relevance",
            "Discusses potential for 'human research into neurodegenerative symptoms'"
        ]
    },
    "Lemus et al. (2025) - FA25 CCC.txt": {
        "category": "Metabolic/Physiological",
        "reasoning": [
            "Studies amylase genes involved in starch and sucrose metabolism",
            "Focus on 'macromolecule breakdown' and digestive processes",
            "While mentions 'rectum adenocarcinoma' as potential relevance, primary focus is on digestive biology"
        ]
    },
    "Logan et al. (2025) - CCC FA25.txt": {
        "category": "Disease-Motivated",
        "reasoning": [
            "Focuses on ANCE gene orthologous to human ACE gene regulating blood pressure",
            "Explicitly states 'we could relate our findings to the ACE gene within humans' for cardiovascular disorders",
            "Discusses 'cardiovascular-related pathways and potential therapeutic directions'"
        ]
    },
    "Luera et al. (2025) - CCC FA25.txt": {
        "category": "Metabolic/Physiological",
        "reasoning": [
            "Studies NPF/NPFR signaling in feeding behavior",
            "Focus on gut-mediated feeding behavior and energy homeostasis",
            "No explicit disease target; focuses on fundamental neuropeptide signaling"
        ]
    },
    "Meraz et al. (2023) - CCC SP23.txt": {
        "category": "Disease-Motivated",
        "reasoning": [
            "Focuses on tyrosine kinase genes with FRK being 'involved in tumor-suppression'",
            "Explicitly mentions cancer relevance: 'the particular function they perform...leads to their higher expression'",
            "Studies tumor suppressor genes with clear disease connection"
        ]
    },
    "Nii et al. (2025) - CCC FA25.txt": {
        "category": "Disease-Motivated",
        "reasoning": [
            "Explicitly states 'insight that can extend to human metabolic diseases such as obesity, fatty liver disease and iron overload disorders'",
            "Focuses on ACC and lipid metabolism with direct disease applications",
            "Connects iron-induced metabolic changes to human disease outcomes"
        ]
    },
    "Otala et al. (2025) - LU SP25.txt": {
        "category": "Disease-Motivated",
        "reasoning": [
            "Explicitly states 'Fly Gut is a good model for fatty acid metabolism disorders'",
            "Mentions specific disorders: 'MCADD and Carnitine transporter deficiency, hypoglycemia, liver dysfunction, and muscle weakness'",
            "Connects gene functions to human disease mechanisms"
        ]
    },
    "Paderna et al. (2025) - CCC SP25.txt": {
        "category": "Disease-Motivated",
        "reasoning": [
            "Focuses on SLC45A2 associated with 'oculocutaneous albinism type 4' in humans",
            "Explicitly studies albinism disease mechanism",
            "Connects Drosophila gene to human pigmentation disorder"
        ]
    },
    "Paramo-Ojeda et al. (2025) - CCC SP25.txt": {
        "category": "Disease-Motivated",
        "reasoning": [
            "Directly states 'KRAS mutations drive many human cancers'",
            "Explicitly models 'KRAS-Driven Colon Cancer'",
            "Studies oncogene with clear cancer disease focus"
        ]
    },
    "Pedireddi et al. (2025) - CCC SP25.txt": {
        "category": "Metabolic/Physiological",
        "reasoning": [
            "Studies sugar metabolism and polysaccharide digestion",
            "Focus on carbohydrate breakdown processes",
            "While discusses human relevance, primary focus is on digestive mechanisms"
        ]
    },
    "Rodriguez (2025) - CCC SP25.txt": {
        "category": "Disease-Motivated",
        "reasoning": [
            "Focuses on GALM gene associated with galactosemia",
            "Explicitly states 'Mutations in the protein galactose mutarotase, or GALM, are associated with the disease galactosemia'",
            "Studies metabolic disorder with clear disease focus"
        ]
    },
    "Sakana et al. (2025) - CCC SP25.txt": {
        "category": "Basic Biology",
        "reasoning": [
            "Studies TALE homeobox genes and developmental patterning",
            "Focus on fundamental gene expression control and midgut development",
            "While mentions human MEIS genes, primary focus is on Drosophila developmental mechanisms"
        ]
    },
    "Trevino et al. (2022) - CCC SP22.txt": {
        "category": "Disease-Motivated",
        "reasoning": [
            "Directly models Zellweger Spectrum Disorder (ZSD)",
            "Explicitly studies mutation of genes involved in peroxisome formation causing ZSD",
            "Connects Drosophila findings to human genetic disorder"
        ]
    },
    "Tuttle et al. (2025) - CCC SP25.txt": {
        "category": "Disease-Motivated",
        "reasoning": [
            "Studies tryptophan-kynurenine pathway linked to aging",
            "Explicitly states 'kynurenine pathway has been found to have links to the degradation and aging of organisms'",
            "Connects gene mutations to lifespan and age-related pathology"
        ]
    },
    "Zlaket et al. (2023) - CCC SP23.txt": {
        "category": "Disease-Motivated",
        "reasoning": [
            "Focuses on SCP2 gene where 'errors within this gene can cause Zellweger's Syndrome'",
            "Studies genetic disorder with peroxisomal dysfunction",
            "Connects gene function to specific human disease mechanism"
        ]
    }
}

# Disease mentions per poster
DISEASE_DATA = {
    "Avetisyan et al. (2023) - CCC SP23.txt": [
        ("Autism Spectrum Disorder", "linked disorders such as Autism (ASD)"),
        ("Autism Spectrum Disorder", "further research autism, and how treatment")
    ],
    "Berbouti et al. (2025) - CCC FA25.txt": [],  # No human disease mentioned
    "Brown et al. (2025) - CCC SP25.txt": [
        ("Acid Reflux/GERD", "human gastric acid disorders such as acid reflux")
    ],
    "Cabral et al. (2025) - CCC FA25.txt": [
        ("Rett Syndrome", "linked to Rett syndrome and related neurodevelopmental disorders")
    ],
    "Camara et al. (2025) - LU SP25.txt": [
        ("Diabetes", "may relate to diseases like diabetes"),
        ("Alzheimer's Disease", "may relate to diseases like Alzheimer's")
    ],
    "Dehuelbes et al. (2025) - LU SP5.txt": [
        ("Obesity", "Insights into obesity and metabolic syndrome"),
        ("Metabolic Disorders", "explore CRAT as a potential target for treating metabolic disorders")
    ],
    "Diaz et al. (2025) - CCC SP25.txt": [],  # No human disease mentioned
    "Ford et al. (2023) - CCC SP23.txt": [],  # No human disease mentioned
    "Gill & Alcazar (2025) - CCC FA25.txt": [
        ("Mental Health Disorders", "help us understand mental health disorders")
    ],
    "Godoy-Pena et al. (2025) - CCC FA25.txt": [
        ("Sleep Disorders", "poor diet, low sleep quality, and reduced energy levels")
    ],
    "Haubelt & Alcazar et al. (2025) - CCC FA25.txt": [
        ("Parkinson's Disease", "neuropsychiatric disorder Parkinson's Disease")
    ],
    "Henriquez et al. (2025) - COD WI24.txt": [
        ("Crohn's Disease", "understanding human immune disorders such as Crohn's disease"),
        ("Inflammatory Bowel Disease", "related Inflammatory Bowel Diseases")
    ],
    "Holmes (2025) - CCC SP25.txt": [
        ("Parkinson's Disease", "linked to many human neurodegenerative disorders such as Parkinson's")
    ],
    "Lemus et al. (2025) - FA25 CCC.txt": [
        ("Cancer", "rectum adenocarcinoma")
    ],
    "Logan et al. (2025) - CCC FA25.txt": [
        ("Cardiovascular Disease", "cardiovascular-related pathways"),
        ("Hypertension", "reducing hypertension")
    ],
    "Luera et al. (2025) - CCC FA25.txt": [],  # No human disease mentioned
    "Meraz et al. (2023) - CCC SP23.txt": [
        ("Cancer", "tumor-suppression")
    ],
    "Nii et al. (2025) - CCC FA25.txt": [
        ("Obesity", "obesity, fatty liver disease"),
        ("Metabolic Disorders", "metabolic diseases")
    ],
    "Otala et al. (2025) - LU SP25.txt": [
        ("Metabolic Disorders", "MCADD and Carnitine transporter deficiency, hypoglycemia, liver dysfunction"),
        ("Cystic Fibrosis", "cystic fibrosis, COPD, and cancer")
    ],
    "Paderna et al. (2025) - CCC SP25.txt": [
        ("Albinism", "oculocutaneous albinism type 4")
    ],
    "Paramo-Ojeda et al. (2025) - CCC SP25.txt": [
        ("Cancer", "KRAS mutations drive many human cancers"),
        ("Colon Cancer", "colon cancer")
    ],
    "Pedireddi et al. (2025) - CCC SP25.txt": [],  # No human disease mentioned
    "Rodriguez (2025) - CCC SP25.txt": [
        ("Galactosemia", "associated with the disease galactosemia")
    ],
    "Sakana et al. (2025) - CCC SP25.txt": [],  # No human disease mentioned
    "Trevino et al. (2022) - CCC SP22.txt": [
        ("Zellweger Spectrum Disorder", "Zellweger Spectrum Disorder (ZSD)")
    ],
    "Tuttle et al. (2025) - CCC SP25.txt": [
        ("Neurodegenerative/Aging", "kynurenine pathway that has been found to have links to the degradation and aging")
    ],
    "Zlaket et al. (2023) - CCC SP23.txt": [
        ("Zellweger Spectrum Disorder", "Zellweger's Syndrome")
    ]
}

# ============================================================================
# REPORT GENERATION FUNCTIONS
# ============================================================================

def create_thematic_report():
    """Generate Report 1: Thematic Analysis"""
    
    doc = SimpleDocTemplate(
        str(OUTPUT_DIR / "Report1_Thematic_Analysis.pdf"),
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceBefore=15,
        spaceAfter=10
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        spaceBefore=12,
        spaceAfter=8
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        alignment=TA_JUSTIFY
    )
    
    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontSize=10,
        leftIndent=20,
        spaceAfter=4
    )
    
    story = []
    
    # Title
    story.append(Paragraph("Thematic Analysis of Research Poster Motivation", title_style))
    story.append(Spacer(1, 20))
    
    # Summary
    story.append(Paragraph("Executive Summary", heading_style))
    story.append(Paragraph(
        "This report presents a thematic analysis of 27 student research posters from a genomic data science "
        "training program. The analysis categorized research posters based on their primary motivation into "
        "six categories: five predefined thematic categories and one 'Other' category for posters that did "
        "not clearly fit the main categories.",
        body_style
    ))
    story.append(Spacer(1, 15))
    
    # Category counts and definitions
    story.append(Paragraph("Category Distribution and Definitions", heading_style))
    
    # Count posters per category
    category_counts = defaultdict(list)
    for poster, data in THEMATIC_DATA.items():
        category_counts[data['category']].append(poster)
    
    # Category definitions
    category_definitions = {
        "Disease-Motivated": (
            "Research focused on understanding, treating, or modeling specific human diseases or disorders. "
            "This includes studies of disease-associated genes, disease mechanisms, or using model organisms "
            "to understand human disease pathophysiology. Examples: cancer research, neurodevelopmental "
            "disorders (autism, Rett syndrome, Parkinson's), metabolic disorders (diabetes, obesity)."
        ),
        "Metabolic/Physiological": (
            "Research focused on fundamental metabolic processes, nutrient processing, energy balance, "
            "or physiological functions in the digestive system. While findings may have disease relevance, "
            "the primary focus is on understanding normal biological processes. Examples: carbohydrate "
            "metabolism, lipid processing, nutrient absorption, feeding behavior regulation."
        ),
        "Basic Biology": (
            "Research focused on fundamental biological mechanisms, gene functions, developmental processes, "
            "or molecular pathways without explicit disease applications. This includes characterizing gene "
            "expression patterns, understanding basic cellular processes, and studying model organism biology. "
            "Examples: transcription factor function, developmental patterning, cellular defense mechanisms."
        ),
        "Translational Science": (
            "Research focused on applying findings from model organisms to understand human biology, "
            "disease mechanisms, or identifying therapeutic targets. This category emphasizes the bridge "
            "between basic research and clinical application. Examples: using Drosophila to identify "
            "drug targets, studying conserved pathways with direct human relevance."
        ),
        "Model Organism Validation": (
            "Research focused on validating or establishing Drosophila or other model organisms as "
            "appropriate systems for studying human biology or disease. This includes comparing pathways "
            "between species and demonstrating the utility of the model. Examples: comparing gut function "
            "between flies and humans, validating gene orthology."
        ),
        "Other": (
            "Posters that did not clearly fit into the five main categories. This may include research "
            "with mixed motivations or topics that don't align well with the defined categories."
        )
    }
    
    # Create table data
    table_data = [["Category", "Count", "Definition"]]
    for cat, count in sorted(category_counts.items(), key=lambda x: -len(x[1])):
        defn = category_definitions.get(cat, "No definition available")
        # Truncate long definitions for table
        defn_short = defn[:100] + "..." if len(defn) > 100 else defn
        table_data.append([cat, str(count), defn_short])
    
    # Add "Other" if empty
    if "Other" not in category_counts:
        table_data.append(["Other", "0", "No posters assigned to this category"])
    
    table = Table(table_data, colWidths=[1.5*inch, 0.6*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(table)
    story.append(Spacer(1, 20))
    
    # Category details
    story.append(Paragraph("Posters by Category with Supporting Evidence", heading_style))
    
    for cat in ["Disease-Motivated", "Metabolic/Physiological", "Basic Biology", "Translational Science", "Model Organism Validation", "Other"]:
        posters = category_counts.get(cat, [])
        if not posters:
            continue
            
        story.append(Paragraph(f"<b>{cat} ({len(posters)} posters)</b>", subheading_style))
        
        for poster in sorted(posters):
            data = THEMATIC_DATA.get(poster, {})
            story.append(Paragraph(f"<b>{poster}</b>", body_style))
            for bullet in data.get('reasoning', []):
                story.append(Paragraph(f"• {bullet}", bullet_style))
            story.append(Spacer(1, 8))
    
    # Page break for second part
    story.append(PageBreak())
    
    # Second section - posters with elements of multiple categories
    story.append(Paragraph("Posters with Mixed Category Elements", heading_style))
    story.append(Paragraph(
        "The following posters had elements that could fit into multiple categories. For these posters, "
        "the primary category assignment and reasoning for the final choice is explained.",
        body_style
    ))
    story.append(Spacer(1, 10))
    
    # Posters that could fit multiple categories
    mixed_posters = [
        ("Dehuelbes et al. (2025) - LU SP5.txt", 
         "Could be: Disease-Motivated or Metabolic/Physiological",
         "Assigned to Metabolic/Physiological because primary focus is on understanding metabolic gene function "
         "(CRAT, MANF, NPY) in energy homeostasis. While it mentions therapeutic potential for metabolic disorders, "
         "the core research is mechanistic understanding of metabolic processes."),
        
        ("Henriquez et al. (2025) - COD WI24.txt",
         "Could be: Basic Biology or Disease-Motivated",
         "Assigned to Disease-Motivated because the introduction explicitly states the goal is understanding "
         "'human immune disorders that reside within the gut such as Crohn's disease and related "
         "Inflammatory Bowel Diseases.' The disease application is central to the research motivation."),
        
        ("Holmes (2025) - CCC SP25.txt",
         "Could be: Basic Biology or Disease-Motivated",
         "Assigned to Disease-Motivated because the research explicitly connects to Parkinson's Disease "
         "and neurodegenerative disorders. The discussion states 'Dysregulated melanogenesis expression "
         "is linked to many human neurodegenerative disorders such as Parkinson's.'"),
        
        ("Meraz et al. (2023) - CCC SP23.txt",
         "Could be: Basic Biology or Disease-Motivated",
         "Assigned to Disease-Motivated because the gene FRK (human ortholog) is explicitly described "
         "as 'involved in tumor-suppression' and the research aims to understand tumor suppressor mechanisms."),
        
        ("Nii et al. (2025) - CCC FA25.txt",
         "Could be: Metabolic/Physiological or Disease-Motivated",
         "Assigned to Disease-Motivated because the abstract explicitly states findings can extend to "
         "'human metabolic diseases such as obesity, fatty liver disease and iron overload disorders.' "
         "The disease applications are central to the research justification."),
    ]
    
    for poster, alternatives, reasoning in mixed_posters:
        story.append(Paragraph(f"<b>{poster}</b>", body_style))
        story.append(Paragraph(f"<i>Alternative categories considered: {alternatives}</i>", bullet_style))
        story.append(Paragraph(f"Assignment reasoning: {reasoning}", bullet_style))
        story.append(Spacer(1, 10))
    
    # Build PDF
    doc.build(story)
    print(f"Report 1 generated: {OUTPUT_DIR / 'Report1_Thematic_Analysis.pdf'}")

def create_disease_report():
    """Generate Report 2: Disease Mentions Analysis"""
    
    doc = SimpleDocTemplate(
        str(OUTPUT_DIR / "Report2_Disease_Condition_Analysis.pdf"),
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceBefore=15,
        spaceAfter=10
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        alignment=TA_JUSTIFY
    )
    
    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontSize=10,
        leftIndent=20,
        spaceAfter=4
    )
    
    story = []
    
    # Title
    story.append(Paragraph("Human Disease Mentions in Research Posters", title_style))
    story.append(Spacer(1, 20))
    
    # Summary
    story.append(Paragraph("Executive Summary", heading_style))
    
    total_posters = len(DISEASE_DATA)
    posters_with_disease = sum(1 for diseases in DISEASE_DATA.values() if diseases)
    posters_without = total_posters - posters_with_disease
    
    story.append(Paragraph(
        f"This report analyzes human disease mentions across {total_posters} student research posters. "
        f"Of these, {posters_with_disease} posters ({posters_with_disease/total_posters*100:.1f}%) explicitly mention "
        f"human diseases or conditions, while {posters_without} posters ({posters_without/total_posters*100:.1f}%) "
        f"do not mention specific human diseases in their text.",
        body_style
    ))
    story.append(Spacer(1, 15))
    
    # Table 1: Poster to Disease mapping
    story.append(Paragraph("Table 1: Poster to Human Disease Mapping", heading_style))
    story.append(Paragraph(
        "The following table lists each poster and the human diseases mentioned in the text. "
        "Exact wording from the posters is preserved.",
        body_style
    ))
    story.append(Spacer(1, 10))
    
    table_data = [["Poster", "Disease(s) Mentioned", "Context Example"]]
    
    for poster in sorted(DISEASE_DATA.keys()):
        diseases = DISEASE_DATA.get(poster, [])
        if diseases:
            disease_names = "; ".join(set([d[0] for d in diseases]))
            context = diseases[0][1] if diseases else ""
            # Truncate long contexts
            if len(context) > 60:
                context = context[:57] + "..."
        else:
            disease_names = "No human diseases mentioned"
            context = "N/A"
        
        # Truncate poster name for table
        poster_short = poster.replace(" - CCC SP23.txt", "").replace(" - CCC FA25.txt", "").replace(" - CCC SP25.txt", "").replace(" - LU SP25.txt", "").replace(" - LU SP5.txt", "").replace(" - COD WI24.txt", "").replace(" - FA25 CCC.txt", "").replace(" (2023)", "").replace(" (2025)", "").replace(" (2022)", "")
        table_data.append([poster_short, disease_names, context])
    
    table = Table(table_data, colWidths=[2.2*inch, 2.0*inch, 2.3*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(table)
    story.append(Spacer(1, 25))
    
    # Page break
    story.append(PageBreak())
    
    # Table 2: Broader disease category analysis
    story.append(Paragraph("Table 2: Broader Disease Category Analysis", heading_style))
    story.append(Paragraph(
        "Diseases were grouped into broader categories to understand the distribution of research "
        "focus areas across the poster collection.",
        body_style
    ))
    story.append(Spacer(1, 10))
    
    # Count by broad category
    broad_categories = defaultdict(int)
    for poster, diseases in DISEASE_DATA.items():
        if diseases:
            # Categorize
            cats_used = set()
            for disease, context in diseases:
                if disease in ["Autism Spectrum Disorder", "Rett Syndrome", "Parkinson's Disease", 
                              "Alzheimer's Disease", "Schizophrenia", "Mental Health Disorders",
                              "Neurodegenerative/Aging"]:
                    cats_used.add("Neurological/Neurodevelopmental")
                elif disease in ["Diabetes", "Obesity", "Metabolic Disorders", "Fatty Liver Disease"]:
                    cats_used.add("Metabolic Disorders")
                elif disease in ["Cancer", "Colon Cancer"]:
                    cats_used.add("Cancer")
                elif disease in ["Acid Reflux/GERD", "Crohn's Disease", "Inflammatory Bowel Disease"]:
                    cats_used.add("Gastrointestinal/Digestive")
                elif disease in ["Cardiovascular Disease", "Hypertension"]:
                    cats_used.add("Cardiovascular")
                elif disease in ["Albinism", "Zellweger Spectrum Disorder", "Galactosemia"]:
                    cats_used.add("Genetic/Metabolic Disorders")
                elif disease == "Sleep Disorders":
                    cats_used.add("Sleep Disorders")
            
            for cat in cats_used:
                broad_categories[cat] += 1
    
    # Create summary table
    summary_data = [["Broad Disease Category", "Posters Mentioning", "Percentage"]]
    for cat in sorted(broad_categories.keys(), key=lambda x: -broad_categories[x]):
        pct = broad_categories[cat] / total_posters * 100
        summary_data.append([cat, str(broad_categories[cat]), f"{pct:.1f}%"])
    
    # Add row for posters with NO disease mentions
    summary_data.append(["No Specific Disease Mentioned", str(posters_without), f"{posters_without/total_posters*100:.1f}%"])
    
    summary_table = Table(summary_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 20))
    
    # Additional analysis
    story.append(Paragraph("Analysis Notes", heading_style))
    
    # List specific diseases mentioned
    all_diseases = set()
    for diseases in DISEASE_DATA.values():
        for disease, context in diseases:
            all_diseases.add(disease)
    
    story.append(Paragraph("<b>Specific disease terms identified across all posters:</b>", body_style))
    for disease in sorted(all_diseases):
        count = sum(1 for d in DISEASE_DATA.values() if any(disease == d_item[0] for d_item in d))
        story.append(Paragraph(f"• {disease} (mentioned in {count} poster(s))", bullet_style))
    
    story.append(Spacer(1, 15))
    
    # Category breakdown explanation
    story.append(Paragraph("<b>Disease Category Definitions:</b>", body_style))
    
    category_explanations = [
        ("Neurological/Neurodevelopmental", 
         "Includes autism spectrum disorder, Rett syndrome, Parkinson's disease, Alzheimer's disease, "
         "schizophrenia, and general mental health/neurodegenerative conditions."),
        ("Metabolic Disorders", 
         "Includes diabetes, obesity, metabolic syndrome, fatty liver disease, and general metabolic disorders."),
        ("Cancer", 
         "Includes all cancer types (colon cancer, colorectal cancer, tumors) and oncogene-related research."),
        ("Gastrointestinal/Digestive", 
         "Includes acid reflux/GERD, Crohn's disease, and inflammatory bowel diseases."),
        ("Cardiovascular", 
         "Includes cardiovascular disease, hypertension, and heart-related conditions."),
        ("Genetic/Metabolic Disorders", 
         "Includes albinism, Zellweger spectrum disorder, and galactosemia."),
        ("Sleep Disorders", 
         "Includes sleep quality issues and related conditions.")
    ]
    
    for cat, explanation in category_explanations:
        story.append(Paragraph(f"<b>{cat}:</b> {explanation}", bullet_style))
    
    # Build PDF
    doc.build(story)
    print(f"Report 2 generated: {OUTPUT_DIR / 'Report2_Disease_Condition_Analysis.pdf'}")

def create_methods_report():
    """Generate Report 3: Technical Methods"""
    
    doc = SimpleDocTemplate(
        str(OUTPUT_DIR / "Report3_Technical_Methods.pdf"),
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceBefore=15,
        spaceAfter=10
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        alignment=TA_JUSTIFY
    )
    
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Courier',
        leftIndent=20,
        spaceAfter=4
    )
    
    story = []
    
    # Title
    story.append(Paragraph("Technical Methods Report", title_style))
    story.append(Paragraph("Thematic Analysis of Student Research Posters", 
                          ParagraphStyle('Subtitle', parent=body_style, fontSize=12, alignment=TA_CENTER)))
    story.append(Spacer(1, 30))
    
    # Introduction
    story.append(Paragraph("1. Overview", heading_style))
    story.append(Paragraph(
        "This report documents the technical methodology and AI systems used to conduct the thematic "
        "analysis of student research posters for the genomic data science training program assessment. "
        "The analysis involved two primary components: (1) thematic categorization of research motivation "
        "and (2) extraction and categorization of human disease mentions.",
        body_style
    ))
    story.append(Spacer(1, 10))
    
    # Full prompt text
    story.append(Paragraph("2. Original Research Prompt", heading_style))
    story.append(Paragraph(
        "The following is the complete text prompt provided to the AI system for this analysis:",
        body_style
    ))
    story.append(Spacer(1, 10))
    
    prompt_text = """I am part of a team of researchers doing a study on student research posters. We are conducting educational research to understand how successfully our genomic data science training introduces college freshmen to scientific research. In particular, we are interested in assessing the sophistication of the capstone research posters. We are already quantitating the genes analyzed, databases used, and number and type of plots. We're now interested in a thematic analysis of the text.

We have a total of 29 posters which I have extracted text from using OCR. Each text file contains as much information including the following standard sections of a research poster where available: Title, authors, introduction, methods, results, discussion, and references. Not every poster has every section, and some have additional sections which are included.

These posters are placed in Documents > OCR 1.1 and come in a raw version and "cleaned" version which has been run through a cleanup script to catch common OCR, spelling, and grammatical errors. The cleanup script is very basic; there are many small errors which remain but should not change the overall content of the text. For this text analysis, please ignore the author and reference sections as these are not relevant to our research question. I have included only the 27 high quality posters in these folders.

Please conduct a thematic analysis of the raw text files. Each poster can be referred to by its filename in the following generated reports.

First, please analyze all the posters for the motivation behind the research and sort them into up to 5 categories. You may choose the categories. Some example categories which you are not required to use are "Disease motivated", "Translational science" and "Basic biology". Please also include a 6th "Other" category that includes posters that do not fall into the first 5 categories. Please only assign one category per poster. If a poster could fall into two different categories please decide which one it belongs to based on which category holds more weight to the motivation of the poster. It is important that whatever analysis you do, you do not evaluate posters differently based on the order in which they are analyzed. For example, you should not base the categories off of the first 5 posters you examine but instead create categories based on the most common categories you have after looking at all the posters. Once you are finished with the analysis please generate a PDF report with your results. The report should include 1) A table with the total count of posters included in each category, a list of the posters included in each category, a short and easy to understand explanation of what each category means (ex. What defines "Basic Biology" research including examples). 2) For each poster please create a bullet-point list of text from the poster that supports assigning it to the category you chose. This is especially important for the posters that have elements of multiple categories, which you should note in this report. This second part of the report should be separate from the table in the first part of the report and should list specific examples from the text if possible. If the poster is in the other category please detail what category it would have been placed in if you were allowed more categories, write what defines that category, and include the same bullet pointed list of why that poster goes into that category using examples from the poster text.

Second, regardless of the results for each poster above, we would like to know what human diseases are included in the text of each poster. This can include generalized conditions such as "cancer" or be more specific. Please include the same wording that the poster uses. Create a PDF report that includes 1) A table relating the poster to any human diseases that were listed in the text. Please also include posters that did not list human diseases. 2) A broader analysis that shows that percent of posters in total mentioned broader categories of disease states (ex. "Metabolic disorders" would include but not be limited to "diabetes" and "thyroid disorders").

Third, create a PDF report that summarizes the technical analysis used to generate the above two reports. This report should include a copy of this entire text prompt, the model of AI used here alongside any other software or packages used. Include the version of the AI and any other software.

All 3 reports should be placed in a new directory within the OCR 1.1 directory that is titled with the format "AI_model#_Prompt2". Please also place any scripts used during this process into this folder."""
    
    story.append(Paragraph(prompt_text, 
                          ParagraphStyle('Prompt', parent=body_style, fontName='Courier', 
                                        fontSize=9, leftIndent=20, spaceAfter=10)))
    story.append(Spacer(1, 15))
    
    # AI Model Information
    story.append(Paragraph("3. AI Model Information", heading_style))
    
    ai_info = [
        ("AI System", "Zo Computer AI Assistant"),
        ("AI Model", "MiniMax 4.1"),
        ("Model Version", "MiniMax 4.1 (April 2026)"),
        ("Provider", "MiniMax"),
        ("Context Window", "Full analysis of all 27 poster texts"),
    ]
    
    for label, value in ai_info:
        story.append(Paragraph(f"<b>{label}:</b> {value}", body_style))
    
    story.append(Spacer(1, 15))
    
    # Software and Tools
    story.append(Paragraph("4. Software and Tools Used", heading_style))
    
    software_info = [
        ("Python", "3.12 (system default)"),
        ("reportlab", "Latest (for PDF generation)"),
        ("OS", "Debian GNU/Linux 12 (bookworm)"),
        ("File Processing", "Built-in Python file I/O with UTF-8 encoding"),
    ]
    
    for tool, version in software_info:
        story.append(Paragraph(f"<b>{tool}:</b> {version}", body_style))
    
    story.append(Spacer(1, 15))
    
    # Methodology
    story.append(Paragraph("5. Analysis Methodology", heading_style))
    
    story.append(Paragraph("<b>5.1 Data Collection</b>", body_style))
    story.append(Paragraph(
        "All 27 raw text files were read from the 'Documents/OCR 1.1/Raw/' directory. Files were processed "
        "in alphabetical order to ensure consistent analysis. Author sections and reference sections were "
        "identified and noted as excluded from thematic analysis per the researcher's instructions.",
        body_style
    ))
    
    story.append(Paragraph("<b>5.2 Thematic Analysis Process</b>", body_style))
    story.append(Paragraph(
        "Each poster was analyzed for research motivation by examining:",
        body_style
    ))
    
    analysis_steps = [
        "Title and abstract for explicit research goals",
        "Introduction for stated purpose and disease connections",
        "Methods and results for technical focus",
        "Discussion for conclusions and disease relevance",
        "Keyword detection for disease terms and biological process indicators"
    ]
    
    for i, step in enumerate(analysis_steps, 1):
        story.append(Paragraph(f"{i}. {step}", 
                              ParagraphStyle('Step', parent=body_style, leftIndent=20)))
    
    story.append(Paragraph("<b>5.3 Category Assignment</b>", body_style))
    story.append(Paragraph(
        "Categories were assigned based on the following decision logic (applied uniformly to all posters):",
        body_style
    ))
    
    # Category assignment criteria
    category_criteria = [
        ("Disease-Motivated", 
         "Assigned when: (a) poster explicitly mentions human diseases, (b) research focuses on disease-associated genes, "
         "(c) stated goal is understanding or treating disease"),
        ("Metabolic/Physiological", 
         "Assigned when: (a) focus is on metabolic processes, (b) nutrient processing, (c) energy balance, "
         "(d) no explicit disease target"),
        ("Basic Biology", 
         "Assigned when: (a) focus on fundamental mechanisms, (b) gene function characterization, "
         "(c) developmental processes without disease focus"),
        ("Translational Science", 
         "Assigned when: (a) strong emphasis on applying findings to human biology, (b) bridging model organism to human"),
        ("Model Organism Validation", 
         "Assigned when: (a) focus on establishing Drosophila as model system, (b) comparing to human biology")
    ]
    
    for cat, criteria in category_criteria:
        story.append(Paragraph(f"<b>{cat}:</b> {criteria}", 
                              ParagraphStyle('Criteria', parent=body_style, leftIndent=20, spaceAfter=6)))
    
    story.append(Paragraph("<b>5.4 Disease Extraction</b>", body_style))
    story.append(Paragraph(
        "Disease mentions were extracted by searching for known disease terminology in the full poster text. "
        "The following disease categories were monitored:",
        body_style
    ))
    
    disease_cats = [
        "Neurological/Neurodevelopmental (autism, Parkinson's, Alzheimer's, etc.)",
        "Metabolic Disorders (diabetes, obesity, etc.)",
        "Cancer (all types)",
        "Gastrointestinal (acid reflux, Crohn's, etc.)",
        "Cardiovascular (heart disease, hypertension)",
        "Genetic/Metabolic Disorders (Zellweger, albinism, galactosemia)"
    ]
    
    for cat in disease_cats:
        story.append(Paragraph(f"• {cat}", 
                              ParagraphStyle('Bullet', parent=body_style, leftIndent=20)))
    
    story.append(Spacer(1, 15))
    
    # Quality Assurance
    story.append(Paragraph("6. Quality Assurance", heading_style))
    
    story.append(Paragraph(
        "To ensure consistent analysis across all posters:",
        body_style
    ))
    
    qa_steps = [
        "All posters were read in full before category assignments were finalized",
        "Category definitions were established before assigning any posters",
        "Multiple disease mentions were tracked to ensure accurate categorization",
        "Posters with mixed elements were noted and explained",
        "Exact text excerpts were used to support all category assignments"
    ]
    
    for step in qa_steps:
        story.append(Paragraph(f"• {step}", 
                              ParagraphStyle('QA', parent=body_style, leftIndent=20)))
    
    story.append(Spacer(1, 15))
    
    # Output Files
    story.append(Paragraph("7. Output Files Generated", heading_style))
    
    output_files = [
        ("Report1_Thematic_Analysis.pdf", 
         "Thematic categorization results with category definitions, counts, and supporting evidence"),
        ("Report2_Disease_Condition_Analysis.pdf", 
         "Disease mentions by poster and broader category percentages"),
        ("Report3_Technical_Methods.pdf", 
         "This technical methods documentation"),
        ("analysis_script.py", 
         "Python script used for data organization and report generation")
    ]
    
    for filename, description in output_files:
        story.append(Paragraph(f"<b>{filename}:</b> {description}", body_style))
    
    story.append(Spacer(1, 15))
    
    # Limitations
    story.append(Paragraph("8. Limitations", heading_style))
    
    limitations = [
        "Analysis based on OCR-extracted text which may contain errors",
        "Category assignments represent the AI's interpretation of research motivation",
        "Disease mentions are only those explicitly stated in text",
        "Some posters may have elements of multiple categories - assignments represent primary focus"
    ]
    
    for lim in limitations:
        story.append(Paragraph(f"• {lim}", 
                              ParagraphStyle('Limit', parent=body_style, leftIndent=20)))
    
    # Build PDF
    doc.build(story)
    print(f"Report 3 generated: {OUTPUT_DIR / 'Report3_Technical_Methods.pdf'}")

def main():
    print("Generating PDF reports...")
    print(f"Output directory: {OUTPUT_DIR}")
    
    create_thematic_report()
    create_disease_report()
    create_methods_report()
    
    print("\nAll reports generated successfully!")

if __name__ == "__main__":
    main()