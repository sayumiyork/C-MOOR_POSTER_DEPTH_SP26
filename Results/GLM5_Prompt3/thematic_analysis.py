#!/usr/bin/env python3
"""
Thematic Analysis of Research Poster Motivations
GLM5_Prompt3 Analysis Script
"""

import os
from collections import defaultdict
from fpdf import FPDF

def clean_text(text):
    """Clean text to remove special characters that cause encoding issues."""
    replacements = {
        '\u2014': '-',  # em-dash
        '\u2013': '-',  # en-dash
        '\u2018': "'",  # left single quote
        '\u2019': "'",  # right single quote
        '\u201c': '"',  # left double quote
        '\u201d': '"',  # right double quote
        '\u2026': '...',  # ellipsis
        '\u00b0': ' degrees',  # degree symbol
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    # Remove any remaining non-latin-1 characters
    return text.encode('latin-1', errors='replace').decode('latin-1')

# Define the categories and their descriptions
CATEGORIES = {
    "Basic biology (Neurology)": "Posters centered on nervous-system signaling, sleep, feeding behavior, gut-brain communication, or related signaling pathways without a named disease being the main motivating factor.",
    "Basic biology (Metabolism)": "Posters focused on sugar, lipid, or amino-acid metabolism; digestion; absorption; or energy balance without a named disease being the main motivating factor.",
    "Basic biology (Other)": "Research focused on understanding fundamental biological mechanisms - such as gene expression patterns, regional tissue specialization, signaling pathways, gene function, patterning, pigmentation, transcriptional control, developmental processes, or cell biology - without explicitly targeting a specific human disease.",
    "Disease research (Neurology)": "Research motivated by understanding the molecular basis of brain or nervous system disorders. These posters investigate genes and pathways linked to cognitive, behavioral, or neuropsychiatric conditions in humans.",
    "Disease research (Metabolism)": "Research motivated by understanding metabolic or digestive disorders, including conditions affecting the liver, gut, or nutrient processing.",
    "Disease research (Other)": "Posters where a named human disease, disorder, or direct health model is the main reason for the work, but the poster does not fit into disease research (neurology) or disease research (metabolism).",
    "Other": "Posters that do not fit into the categories above."
}

# Poster categorizations with supporting evidence
POSTER_ANALYSIS = {
    "Avetisyan et al. (2023) - CCC SP23.txt": {
        "category": "Disease research (Neurology)",
        "evidence": [
            "Title explicitly states: 'Expression Analysis of Autism Related Genes'",
            "Abstract states: 'These genes, which play a role in the upkeep of the gut-microbiome-brain axis, have been identified as autism related.'",
            "Introduction states: 'This connection has linked disorders such as Autism (ASD) to genes expressed within the midgut.'",
            "Abstract states: 'Genes such as these are being studied to further research autism, and how treatment of the midgut can affect autism management.'",
            "The primary motivation is understanding autism spectrum disorder (ASD), a neurological condition."
        ],
        "notes": "This poster has a clear disease motivation (autism) which is a neurological/developmental disorder."
    },
    
    "Berbouti et al. (2025) - CCC FA25.txt": {
        "category": "Basic biology (Metabolism)",
        "evidence": [
            "Title: 'Trehalase Expression in the Drosophila Midgut: Differential Expression across Anterior and Posterior regions'",
            "Abstract: 'Trehalose is a critical sugar in Drosophila melanogaster, in which its breakdown by trehalase provides glucose for energy metabolism.'",
            "Abstract: 'This study provides insight into the regulation of carbohydrate metabolism in flies and parallel sugar processing in humans.'",
            "Introduction: 'The knowledge gap is the relationship between TREH expression and transport genes linked to trehalose and glucose movement.'",
            "No named disease is mentioned as the primary motivation for the research."
        ],
        "notes": "Focus is on carbohydrate metabolism and sugar processing without a disease driver."
    },
    
    "Brown et al. (2025) - CCC SP25.txt": {
        "category": "Disease research (Metabolism)",
        "evidence": [
            "Title: 'Analysis Of Gene Expression Of Acids Reflux Related Genes Across The Midgut'",
            "Abstract: 'These findings highlight conserved biological mechanisms that may provide clarification into human gastric acid disorders such as acid reflux.'",
            "Introduction: 'Acid reflux is a condition shown in millions of people in the world and results in pain in the esophagus due to the backflow of stomach acid.'",
            "Introduction: 'Our research focus is to apply the unknown in the current discussion and lay the foundations for future studies that could eventually lead to more understanding and treatment of acid reflux.'",
            "The primary motivation is acid reflux, a digestive disorder."
        ],
        "notes": "Clear disease motivation (acid reflux) which is a digestive/metabolic condition."
    },
    
    "Cabral et al. (2025) - CCC FA25.txt": {
        "category": "Disease research (Neurology)",
        "evidence": [
            "Abstract: 'Mutations in MECP2 are linked to Rett syndrome and related neurodevelopmental disorders'",
            "Introduction: 'MECP2 dysfunction is known to cause Rett syndrome and contribute to a range of neurological impairments, demonstrating its essential role in normal brain function.'",
            "The research investigates MECP2 expression in relation to Rett syndrome and neurodevelopmental disorders.",
            "Rett syndrome is a neurological disorder affecting brain development."
        ],
        "notes": "Primary motivation is Rett syndrome, a neurological/developmental disorder."
    },
    
    "Camara et al. (2025) - LU SP25.txt": {
        "category": "Basic biology (Metabolism)",
        "evidence": [
            "Title: 'Functional Difference Between Amy-D, Amy-P and Amyrel in Drosophila Midgut'",
            "Introduction: 'We studied expression of three fly amylase genes: Amy-d, Amy-p, and Amyrel.'",
            "Introduction: 'We hypothesized differential expression of these genes across the midgut.'",
            "Introduction mentions diabetes and Alzheimer's as potential relations, but this is secondary context.",
            "Discussion: 'Our findings suggest a specialization of enzyme function along the midgut.'",
            "The main research question is about amylase gene expression patterns, not disease mechanisms."
        ],
        "notes": "While diabetes and Alzheimer's are mentioned, they are noted as potential connections rather than the primary research motivation."
    },
    
    "Dehuelbes et al. (2025) - LU SP5.txt": {
        "category": "Basic biology (Metabolism)",
        "evidence": [
            "Title: 'Regional Expression of Key Metabolic genes in Drosophila Midgut: CRAT, MANF, NPY and their relation to each other'",
            "Introduction: 'Acetyl-CoA links carbohydrate, fat, & protein metabolism'",
            "Introduction: 'Carnitine O-Acetyltransferase (CRAT) is a mitochondrial enzyme involved in fatty acid metabolism'",
            "Discussion mentions potential therapeutic applications but the main focus is on understanding metabolic gene expression patterns.",
            "The poster explores basic metabolic gene functions without a specific disease as the primary driver."
        ],
        "notes": "Focus on metabolic gene expression and energy homeostasis. Disease applications are mentioned as future directions."
    },
    
    "Diaz et al. (2025) - CCC SP25.txt": {
        "category": "Basic biology (Other)",
        "evidence": [
            "Title: 'V-ATPase Gene Expression Reveals Cellular Defense Zones in the Copper Region of the Drosophila Midgut'",
            "Abstract: 'To explore how different regions of the Drosophila melanogaster midgut contribute to immune defense'",
            "Introduction: 'Phagosomes are part of the cell's internal defense and cleanup system, essential for immunity, tissue remodelling, and maintaining cellular health.'",
            "The focus is on understanding basic immune defense mechanisms and cellular cleanup systems.",
            "No named disease is the primary motivation for this research."
        ],
        "notes": "Focus on immune defense and cellular mechanisms (phagocytosis) without a specific disease motivation."
    },
    
    "Ford et al. (2023) - CCC SP23.txt": {
        "category": "Basic biology (Other)",
        "evidence": [
            "Title: 'Cytochrome P450 genes providing insecticide resistance found in al, p1 and p2_4 midgut regions of Drosophila'",
            "Abstract: 'Some Cytochrome P450 genes play an important role in the development of insecticide resistance in Drosophila Melanogaster.'",
            "Introduction: 'Since it is known that some Cytochrome P450 genes have been shown to play a role in insecticide resistance, especially to DDT'",
            "Focus is on insecticide resistance mechanisms in Drosophila - this is not a human disease focus.",
            "Discussion mentions potential human relevance but the main focus is fly biology."
        ],
        "notes": "The research is about insecticide resistance in flies, not a human disease."
    },
    
    "Gill & Alcazar (2025) - CCC FA25.txt": {
        "category": "Basic biology (Neurology)",
        "evidence": [
            "Title: 'Differential Expression of Serotonin Receptor Genes Htrla and Htr2a in the Prefrontal Cortex and Striatum'",
            "Abstract: 'The purpose of this study was to test if serotonin receptor signaling is higher in the PFC compared to the STR as hypothesized.'",
            "Introduction: 'Serotonin is one of the major chemical messengers in the brain that through receptors genes.'",
            "While mental health disorders are mentioned as context, the primary research question is about serotonin receptor expression patterns between brain regions.",
            "No specific named disease is the main motivation for the research."
        ],
        "notes": "The focus is on serotonin receptor signaling in different brain regions. Mental health disorders are mentioned as background context."
    },
    
    "Godoy-Pena et al. (2025) - CCC FA25.txt": {
        "category": "Basic biology (Neurology)",
        "evidence": [
            "Title: 'Regulation of Sleep Quality: Analysis of Gene Expression Using Bulk RNA-seq Data'",
            "Abstract: 'The main purpose of this study was to determine what genes dictate the kind of sleep drosophila flies get, and connect it to a gut-brain region.'",
            "Introduction: 'Sleep and diet play crucial roles in human health, affecting energy levels, cognitive function, and overall well-being.'",
            "Focus is on sleep regulation mechanisms and gut-brain communication.",
            "No named disease is the primary motivation."
        ],
        "notes": "Focus on sleep quality and sleep regulation through gut-brain axis. Sleep is a biological process, not a specific disease."
    },
    
    "Haubelt & Alcazar et al. (2025) - CCC FA25.txt": {
        "category": "Disease research (Neurology)",
        "evidence": [
            "Title: 'Exploring DRD2: The Association of PD Risk with Dopamine Receptors in the Dopaminergic Synapse' (PD = Parkinson's Disease)",
            "Abstract: 'I was interested in the genes, pathways, and mechanisms related to the neuropsychiatric disorder Parkinson's Disease'",
            "Introduction: 'Many neuropsychiatric disorders including Parkinson's Disease, Schizophrenia, and Post-traumatic Stress Disorder are seen to have direct correlation to dopamine receptor D2'",
            "The primary motivation is clearly Parkinson's Disease, a neurological disorder."
        ],
        "notes": "Clear disease motivation - Parkinson's Disease is the main focus of the research."
    },
    
    "Henriquez et al. (2025) - COD WI24.txt": {
        "category": "Basic biology (Other)",
        "evidence": [
            "Title: '6 Immune Pathways Exhibit Similar Patterns of Gene Expressions in Drosophila melanogaster Midgut'",
            "Abstract: 'Measurement of gene expression in six immune pathways... suggests similar levels of immune pathway protein expression in the 10 midgut regions'",
            "Introduction: 'Using RNAseq techniques to characterize expression levels of genes related to specific immune responses may help further uncover their functions'",
            "Introduction mentions Crohn's disease as a potential application, but not the main motivation.",
            "The primary focus is on understanding immune pathway expression patterns."
        ],
        "notes": "While Crohn's disease and IBD are mentioned as potential applications, the main research question is about immune pathway gene expression patterns."
    },
    
    "Holmes (2025) - CCC SP25.txt": {
        "category": "Basic biology (Other)",
        "evidence": [
            "Title: 'Melanogenesis within the Drosophila Midgut: Neuromelanin and Dopamine'",
            "Abstract: 'This research was focused in genes connected to melanogenesis (synthesis of melanin) and its antioxidant uses.'",
            "Methods: 'There is an intricate relationship to melanin expression and dopamine in most organisms.'",
            "Discussion mentions Parkinson's as a potential connection, but this is an implication, not the main motivation.",
            "The primary research focus is on melanogenesis and pigment synthesis mechanisms."
        ],
        "notes": "Parkinson's is mentioned in the discussion as a potential connection, but the main motivation is understanding melanogenesis."
    },
    
    "Lemus et al. (2025) - FA25 CCC.txt": {
        "category": "Basic biology (Metabolism)",
        "evidence": [
            "Title: 'Macromolecule Breakdown and Absorption: Analysis of Differential Expression Using Single Cell and Bulk RNA-seq Data'",
            "Abstract: 'Understanding differential gene expression in particular regions can uncover processes relevant to human digestion as well as metabolic disorders.'",
            "The abstract mentions metabolic disorders as potential relevance, but the main focus is on understanding macromolecule breakdown and absorption.",
            "Discussion: 'These results reveal functional diversity within the amylase-family'",
            "Primary focus is on digestive enzyme function and carbohydrate processing."
        ],
        "notes": "The main motivation is understanding macromolecule breakdown and absorption mechanisms."
    },
    
    "Logan et al. (2025) - CCC FA25.txt": {
        "category": "Disease research (Other)",
        "evidence": [
            "Abstract: 'Our results suggest that studying ANCE gene expression and functional studies may offer insights into cardiovascular-related pathways'",
            "Introduction: 'Cardiovascular disorders are a prominent and widespread disease... This sparked an interest to research the ANCE gene within Drosophila melanogaster to find a correlation between the ACE gene and cardiovascular disorders.'",
            "Discussion: 'Our research highlights how studies in fruit flies can offer insights into gene families related to human health, including... cardiovascular function.'",
            "The primary motivation is cardiovascular disorders, which do not fit into neurology or metabolism categories."
        ],
        "notes": "Clear disease motivation - cardiovascular disorders. This does not fit neurology or metabolism disease categories."
    },
    
    "Luera et al. (2025) - CCC FA25.txt": {
        "category": "Basic biology (Neurology)",
        "evidence": [
            "Title: 'Region-Specific NPF/NPFR Signaling in the Drosophila Midgut'",
            "Abstract: 'We analyzed Neuropeptide F (NPF) and its receptor NPFR in Drosophila melanogaster to explore their role in gut-mediated feeding behavior'",
            "Introduction: 'Neuropeptide F (NPF) is a conserved neuropeptide that regulates feeding, stress, and sleep behaviors in Drosophila melanogaster'",
            "Focus is on feeding behavior regulation through neuropeptide signaling.",
            "No named disease is the primary motivation."
        ],
        "notes": "Focus on feeding behavior and neuropeptide signaling (gut-brain axis) without a specific disease motivation."
    },
    
    "Meraz et al. (2023) - CCC SP23.txt": {
        "category": "Basic biology (Other)",
        "evidence": [
            "Title: 'Tyrosine Kinase Expression in the Midgut Suggests a Role in the Copper Region'",
            "Abstract: 'Tyrosine kinases are enzymes related to cell growth and development.'",
            "Introduction mentions disease-related genes as context but the main research question is about gene expression patterns.",
            "Discussion: 'Our hypothesis proposed that a gene that functions as a tumor suppressor would be expressed relatively equally among all regions'",
            "While tumor suppression is discussed, the main focus is on understanding tyrosine kinase gene expression patterns."
        ],
        "notes": "The focus is on understanding gene expression patterns of tyrosine kinases."
    },
    
    "Nii et al. (2025) - CCC FA25.txt": {
        "category": "Basic biology (Metabolism)",
        "evidence": [
            "Title: 'Iron-Induced Modulation of Acetyl-CoA Carboxylase (ACC) in Drosophila Melanogaster: Impacts on Lipid Metabolism and Energy Storage'",
            "Abstract: 'This project investigates how elevated iron influences ACC and ATPCL expression and lipid storage in Drosophila.'",
            "Introduction: 'Iron is an essential micronutrient involved in redox chemistry, mitochondrial function, and cellular metabolism.'",
            "Introduction mentions human metabolic diseases as potential applications.",
            "The main research focus is on understanding iron's effects on lipid metabolism."
        ],
        "notes": "The primary motivation is understanding how iron influences lipid metabolism. Human diseases are mentioned as potential applications."
    },
    
    "Otala et al. (2025) - LU SP25.txt": {
        "category": "Disease research (Metabolism)",
        "evidence": [
            "Title: 'Fly Gut is a good model for fatty acid metabolism disorders'",
            "Introduction: 'Fatty acid metabolism is essential for energy production... Related disorders and symptoms include: MCADD and Carnitine transporter deficiency, hypoglycemia, liver dysfunction, and muscle weakness.'",
            "Introduction: 'We studied the gene expression of Acox3, Muc68e and Mdh1 across the Drosophila midgut to gain a better understanding of how their functions in the fly gut relate to the human body.'",
            "Discussion: 'Based on our results, we can conclude that the fly gut is a good model for fatty acid metabolism.'",
            "The title and introduction make fatty acid metabolism disorders the primary motivation."
        ],
        "notes": "The title explicitly states the focus is on fatty acid metabolism disorders."
    },
    
    "Paderna et al. (2025) - CCC SP25.txt": {
        "category": "Disease research (Other)",
        "evidence": [
            "Title: 'Albinism and Melanogenesis Pathway: Analysis of Differential Gene Expression'",
            "Abstract: 'In humans, the gene SLC45A2 is associated with oculocutaneous albinism type 4, a condition that affects the skin, eyes, and hair'",
            "Introduction: 'In humans, oculocutaneous albinism type 4 (OCA4) manifests as reduced pigment in the skin, eyes, and hair.'",
            "The primary motivation is understanding albinism, a genetic condition affecting pigmentation."
        ],
        "notes": "Albinism is a genetic condition but not a neurological or metabolic disorder."
    },
    
    "Paramo-Ojeda et al. (2025) - CCC SP25.txt": {
        "category": "Disease research (Other)",
        "evidence": [
            "Title: 'Ras85D Expression in Drosophila Midgut Highlights a Model for KRAS-Driven Colon Cancer'",
            "Abstract: 'KRAS mutations drive many human cancers by promoting uncontrolled cell growth.'",
            "Introduction: 'Cancer is a complex disease driven by mutations in genes that regulate cell growth, survival, and DNA repair. One of the most frequently mutated oncogenes in human cancers is KRAS...'",
            "The primary motivation is colon cancer and KRAS-driven oncogenesis."
        ],
        "notes": "Clear disease motivation - colon cancer. Cancer does not fit into neurology or metabolism disease categories."
    },
    
    "Pedireddi et al. (2025) - CCC SP25.txt": {
        "category": "Basic biology (Metabolism)",
        "evidence": [
            "Title: 'Beyond the Anterior: Amylase Gene Expression Suggests Widespread Polysaccharide Digestion in the Drosophila Midgut'",
            "Abstract: 'We were interested in genes involved in sugar metabolism since Drosophila melanogaster lives on a high sugar diet.'",
            "Introduction: 'Our group was interested in looking at how Drosophila Melanogaster digested polysaccharides and the genes that were involved in this process.'",
            "Focus is on polysaccharide digestion and sugar metabolism.",
            "No named disease is the primary motivation."
        ],
        "notes": "Focus on polysaccharide digestion and carbohydrate metabolism without a disease driver."
    },
    
    "Rodriguez (2025) - CCC SP25.txt": {
        "category": "Disease research (Metabolism)",
        "evidence": [
            "Title: 'Differential Gene Expression of Galm1 in the Drosophila Midgut'",
            "Abstract: 'Mutations in the protein galactose mutarotase, or GALM, are associated with the disease galactosemia, which prevents the body from properly metabolising the sugar galactose.'",
            "Introduction: 'Galactosemia is a rare metabolic disorder that results from deficiencies in the GALM gene.'",
            "The primary motivation is understanding galactosemia, a metabolic disorder."
        ],
        "notes": "Galactosemia is a metabolic disorder affecting sugar metabolism, fitting Disease research (Metabolism)."
    },
    
    "Sakana et al. (2025) - CCC SP25.txt": {
        "category": "Basic biology (Other)",
        "evidence": [
            "Title: 'Differential Expression of the TALE Homeobox Genes in Drosophila Midgut patterning'",
            "Abstract: 'The Three Amino acid Loop Extension (TALE) group of homeobox genes regulate cell and tissue-specific gene expression... Our results may help shed light on possible roles and hierarchy of how the TALE genes control patterning in the midgut.'",
            "Introduction: 'Gene expression patterns that control development and differentiation are often orchestrated by transcription factors.'",
            "Focus is on developmental patterning and transcription factor gene expression.",
            "No named disease is the primary motivation."
        ],
        "notes": "Focus on gene expression patterns, developmental processes, and tissue patterning - fundamental biological mechanisms."
    },
    
    "Trevino et al. (2022) - CCC SP22.txt": {
        "category": "Disease research (Metabolism)",
        "evidence": [
            "Title: 'Drosophila Melanogaster a Good Model System of Zellweger Spectrum Disorder'",
            "Abstract: 'Zellweger Spectrum Disorder (ZSD) is a genetic disorder that is caused by the mutation of 1 out of 13 different genes involved in the formation and function of peroxisomes.'",
            "Introduction: 'ZSD is a rare inherited disorder characterized by the absence/reduction of functional peroxisomes in cells, which are essential for beta-oxidation of very-long-chain fatty acids.'",
            "The primary motivation is understanding Zellweger Spectrum Disorder, a peroxisomal disorder affecting metabolism."
        ],
        "notes": "ZSD is a peroxisomal disorder that affects fatty acid metabolism, fitting Disease research (Metabolism)."
    },
    
    "Tuttle et al. (2025) - CCC SP25.txt": {
        "category": "Basic biology (Metabolism)",
        "evidence": [
            "Title: 'Gene Expression Patterns in the Tryptophan-Kynurenine Pathway in Drosophila Melanogaster'",
            "Abstract: 'This study investigates the differential expression of genes regulating Tryptophan and its metabolism pathways in Drosophila Melanogaster.'",
            "Introduction: 'In Drosophila melanogaster, tryptophan is metabolized through the kynurenine pathway, this process has been linked to aging not just in Drosophila, but in all organisms.'",
            "Focus is on tryptophan metabolism and amino acid metabolism.",
            "Aging is mentioned but it's a biological process, not a specific disease."
        ],
        "notes": "Focus on amino acid (tryptophan) metabolism. Aging is mentioned as a related process but not as a specific disease motivation."
    },
    
    "Zlaket et al. (2023) - CCC SP23.txt": {
        "category": "Basic biology (Other)",
        "evidence": [
            "Title: 'ScpX: A Peroxisomal Gene and its Distinctive Paralogs'",
            "Abstract: 'For this research project, we researched the ScpX gene and its paralogs, which are homologous genes arisen from duplication events in the genome and produce proteins with different functions.'",
            "Introduction mentions Zellweger's Syndrome as context, but the main research questions are about paralog expression patterns.",
            "The primary focus is on comparing paralog expression patterns and functions.",
            "While Zellweger's is mentioned as context, the main motivation is understanding gene paralog function."
        ],
        "notes": "Zellweger's Syndrome is mentioned as context for the human gene, but the main research focus is on comparing paralog expression patterns."
    }
}


def generate_report():
    """Generate the PDF report with analysis results."""
    
    # Count posters per category
    category_counts = defaultdict(list)
    for poster, data in POSTER_ANALYSIS.items():
        category_counts[data["category"]].append(poster)
    
    # Create PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Title page
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 20, clean_text("Thematic Analysis of Research Poster Motivations"), new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font("Helvetica", "", 14)
    pdf.cell(0, 10, "GLM5_Prompt3 Analysis Report", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.cell(0, 10, "Date: April 29, 2026", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(10)
    
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, clean_text(
        "This report presents a thematic analysis of 27 research posters examining the motivation behind each study. "
        "Posters were categorized based on whether the primary motivation was basic biology research or disease-oriented research, "
        "with subcategories for neurology, metabolism, and other topics."))
    pdf.ln(5)
    
    # Part 1: Summary Table
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Part 1: Summary Table", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    # Table header
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(200, 200, 200)
    col_widths = [60, 20, 110]
    pdf.cell(col_widths[0], 8, "Category", border=1, fill=True)
    pdf.cell(col_widths[1], 8, "Count", border=1, align="C", fill=True)
    pdf.cell(col_widths[2], 8, "Posters", border=1, fill=True)
    pdf.ln()
    
    # Table rows
    pdf.set_font("Helvetica", "", 9)
    for category in CATEGORIES.keys():
        posters = category_counts.get(category, [])
        count = len(posters)
        poster_names = ", ".join([p.replace(".txt", "") for p in posters])
        
        pdf.cell(col_widths[0], 8, clean_text(category), border=1)
        pdf.cell(col_widths[1], 8, str(count), border=1, align="C")
        
        # Handle long poster lists
        if len(poster_names) > 55:
            # Split into multiple lines
            words = poster_names.split(", ")
            lines = []
            current_line = ""
            for word in words:
                if len(current_line + word) < 55:
                    current_line += word + ", "
                else:
                    lines.append(current_line.strip(", "))
                    current_line = word + ", "
            lines.append(current_line.strip(", "))
            
            for i, line in enumerate(lines):
                if i == 0:
                    pdf.cell(col_widths[2], 8, clean_text(line), border=1)
                else:
                    pdf.cell(col_widths[0], 8, "", border=0)
                    pdf.cell(col_widths[1], 8, "", border=0)
                    pdf.cell(col_widths[2], 8, clean_text(line), border="LR")
                pdf.ln()
            # Add bottom border
            pdf.cell(col_widths[0], 0, "", border=0)
            pdf.cell(col_widths[1], 0, "", border=0)
            pdf.cell(col_widths[2], 0, "", border="LRB")
            pdf.ln()
        else:
            pdf.cell(col_widths[2], 8, clean_text(poster_names), border=1)
            pdf.ln()
    
    # Part 2: Detailed Evidence
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Part 2: Supporting Evidence by Poster", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    # Sort posters by category
    sorted_posters = sorted(POSTER_ANALYSIS.items(), key=lambda x: (x[1]["category"], x[0]))
    
    current_category = None
    for poster, data in sorted_posters:
        category = data["category"]
        
        # Add category header if new category
        if category != current_category:
            if current_category is not None:
                pdf.ln(5)
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_fill_color(230, 230, 230)
            pdf.cell(0, 8, clean_text(category), fill=True, new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", "I", 9)
            pdf.multi_cell(0, 5, clean_text(CATEGORIES[category]))
            pdf.ln(3)
            current_category = category
        
        # Poster name
        pdf.set_font("Helvetica", "B", 10)
        poster_name = poster.replace(".txt", "")
        pdf.cell(0, 7, clean_text(poster_name), new_x="LMARGIN", new_y="NEXT")
        
        # Evidence
        pdf.set_font("Helvetica", "", 9)
        for evidence in data["evidence"]:
            clean_evidence = evidence.replace("\n", " ").strip()
            pdf.set_x(15)
            pdf.multi_cell(0, 5, "- " + clean_text(clean_evidence))
        
        # Notes
        if "notes" in data and data["notes"]:
            pdf.set_font("Helvetica", "I", 8)
            pdf.set_x(15)
            pdf.multi_cell(0, 4, "Note: " + clean_text(data["notes"]))
        
        pdf.ln(3)
        
        # Check if we need a new page
        if pdf.get_y() > 250:
            pdf.add_page()
    
    # Part 3: Category Definitions
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Part 3: Category Definitions", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    pdf.set_font("Helvetica", "", 10)
    for category, description in CATEGORIES.items():
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 7, clean_text(category), new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 9)
        pdf.multi_cell(0, 5, clean_text(description))
        pdf.ln(3)
    
    # Save PDF
    output_path = "/home/workspace/Documents/OCR 1.1/GLM5_Prompt3/Thematic_Analysis_Report.pdf"
    pdf.output(output_path)
    print(f"Report saved to: {output_path}")
    
    # Also save a summary text file
    summary_path = "/home/workspace/Documents/OCR 1.1/GLM5_Prompt3/analysis_summary.txt"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("THEMATIC ANALYSIS OF RESEARCH POSTER MOTIVATIONS\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("SUMMARY TABLE\n")
        f.write("-" * 60 + "\n")
        for category in CATEGORIES.keys():
            posters = category_counts.get(category, [])
            count = len(posters)
            f.write(f"\n{category}: {count} posters\n")
            for p in posters:
                f.write(f"  - {p.replace('.txt', '')}\n")
        
        f.write("\n\n" + "=" * 60 + "\n")
        f.write("DETAILED ANALYSIS BY POSTER\n")
        f.write("=" * 60 + "\n")
        
        for poster, data in sorted_posters:
            f.write(f"\n{poster.replace('.txt', '')}\n")
            f.write(f"Category: {data['category']}\n")
            f.write("Supporting Evidence:\n")
            for evidence in data["evidence"]:
                f.write(f"  - {evidence}\n")
            if "notes" in data and data["notes"]:
                f.write(f"Note: {data['notes']}\n")
            f.write("-" * 40 + "\n")
    
    print(f"Summary saved to: {summary_path}")
    
    return category_counts


if __name__ == "__main__":
    generate_report()
