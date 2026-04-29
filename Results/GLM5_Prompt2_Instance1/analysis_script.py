#!/usr/bin/env python3
"""
Thematic Analysis of Research Posters - C-MOOR OCR Text Analysis
Generates three PDF reports
"""

from fpdf import FPDF
from datetime import datetime
import os

# Poster data
posters_data = {
    "Avetisyan et al. (2023) - CCC SP23.txt": {
        "title": "Expression Analysis of Autism Related Genes",
        "motivation": "Disease-Motivated Research",
        "motivation_evidence": [
            "Research focused on autism-related genes",
            "Introduction discusses gut-microbiome-brain axis and Autism",
            "Goal: research autism genes in D. Melanogaster midgut"
        ],
        "diseases": ["Autism", "Autism Spectrum Disorder (ASD)"],
        "secondary_motivation": None
    },
    "Berbouti et al. (2025) - CCC FA25.txt": {
        "title": "Trehalase Expression in the Drosophila Midgut",
        "motivation": "Basic Metabolic Biology",
        "motivation_evidence": [
            "Primary focus on trehalose catabolism",
            "Investigates differential gene expression",
            "No disease focus"
        ],
        "diseases": [],
        "secondary_motivation": None
    },
    "Brown et al. (2025) - CCC SP25.txt": {
        "title": "Analysis Of Gene Expression Of Acid Reflux Related Genes",
        "motivation": "Disease-Motivated Research",
        "motivation_evidence": [
            "Title mentions Acid Reflux Related Genes",
            "Introduction: acid reflux affects millions",
            "Goal: understanding and treatment of acid reflux"
        ],
        "diseases": ["Acid reflux", "Gastric acid disorders"],
        "secondary_motivation": None
    },
    "Cabral et al. (2025) - CCC FA25.txt": {
        "title": "MECP2 Gene Expression Analysis",
        "motivation": "Disease-Motivated Research",
        "motivation_evidence": [
            "MECP2 dysfunction causes Rett syndrome",
            "Research on genes linked to neurological disorders",
            "Goal: understanding neurological dysfunction"
        ],
        "diseases": ["Rett syndrome", "Neurodevelopmental disorders"],
        "secondary_motivation": None
    },
    "Camara et al. (2025) - LU SP25.txt": {
        "title": "Functional Difference Between Amy-D, Amy-P and Amyrel",
        "motivation": "Basic Metabolic Biology",
        "motivation_evidence": [
            "Primary focus on amylase gene expression",
            "Investigates enzyme function",
            "Disease mentions are contextual"
        ],
        "diseases": ["Diabetes", "Alzheimer's"],
        "secondary_motivation": "Could fit Disease-Motivated but primary focus is enzyme function"
    },
    "Dehuelbes et al. (2025) - LU SP5.txt": {
        "title": "Regional Expression of Key Metabolic genes",
        "motivation": "Basic Metabolic Biology",
        "motivation_evidence": [
            "Focus on energy homeostasis",
            "Discusses acetyl-CoA and fatty acid metabolism",
            "Primary goal: metabolic gene coordination"
        ],
        "diseases": ["Obesity", "Metabolic syndrome"],
        "secondary_motivation": None
    },
    "Diaz et al. (2025) - CCC SP25.txt": {
        "title": "V-ATPase Gene Expression in Copper Region",
        "motivation": "Basic Cellular Biology",
        "motivation_evidence": [
            "Focus on immune defense mechanisms",
            "Investigates V-ATPase genes",
            "Goal: understanding cellular defense"
        ],
        "diseases": [],
        "secondary_motivation": None
    },
    "Ford et al. (2023) - CCC SP23.txt": {
        "title": "Cytochrome P450 genes providing insecticide resistance",
        "motivation": "Basic Cellular Biology",
        "motivation_evidence": [
            "Focus on insecticide resistance",
            "Environmental adaptation focus",
            "Not disease-focused"
        ],
        "diseases": [],
        "secondary_motivation": None
    },
    "Gill & Alcazar (2025) - CCC FA25.txt": {
        "title": "Differential Expression of Serotonin Receptor Genes",
        "motivation": "Disease-Motivated Research",
        "motivation_evidence": [
            "Discusses mood, anxiety, mental health disorders",
            "Research linked to mental health",
            "Goal: understanding psychiatric conditions"
        ],
        "diseases": ["Mental health disorders", "Mood disorders", "Anxiety"],
        "secondary_motivation": None
    },
    "Godoy-Pena et al. (2025) - CCC FA25.txt": {
        "title": "Regulation of Sleep Quality",
        "motivation": "Basic Cellular Biology",
        "motivation_evidence": [
            "Focus on sleep regulation genes",
            "No disease driving research",
            "Goal: understanding sleep mechanism"
        ],
        "diseases": [],
        "secondary_motivation": None
    },
    "Haubelt & Alcazar et al. (2025) - CCC FA25.txt": {
        "title": "Exploring DRD2: PD Risk with Dopamine Receptors",
        "motivation": "Disease-Motivated Research",
        "motivation_evidence": [
            "Title mentions PD Risk (Parkinson's)",
            "Focus on dopaminergic synapse",
            "Goal: understanding neuropsychiatric disorders"
        ],
        "diseases": ["Parkinson's Disease", "Schizophrenia", "PTSD"],
        "secondary_motivation": None
    },
    "Henriquez et al. (2025) - COD WI24.txt": {
        "title": "Immune Pathways in Drosophila Midgut",
        "motivation": "Basic Cellular Biology",
        "motivation_evidence": [
            "Focus on immune pathway expression",
            "Disease mentions are contextual",
            "Goal: understanding immune defense"
        ],
        "diseases": ["Crohn's disease", "Inflammatory Bowel Diseases"],
        "secondary_motivation": None
    },
    "Holmes (2025) - CCC SP25.txt": {
        "title": "Melanogenesis within the Drosophila Midgut",
        "motivation": "Basic Cellular Biology",
        "motivation_evidence": [
            "Focus on melanogenesis and neuromelanin",
            "Disease mention is for relevance",
            "Goal: understanding pigment biology"
        ],
        "diseases": ["Parkinson's", "Neurodegenerative disorders"],
        "secondary_motivation": None
    },
    "Lemus et al. (2025) - FA25 CCC.txt": {
        "title": "Macromolecule Breakdown and Absorption Analysis",
        "motivation": "Basic Cellular Biology",
        "motivation_evidence": [
            "Focus on amylase gene expression",
            "Disease mention is brief",
            "Goal: understanding digestive enzymes"
        ],
        "diseases": ["Rectum adenocarcinoma"],
        "secondary_motivation": None
    },
    "Logan et al. (2025) - CCC FA25.txt": {
        "title": "ANCE Gene Expression and Cardiovascular Correlations",
        "motivation": "Disease-Motivated Research",
        "motivation_evidence": [
            "Introduction on cardiovascular disorders",
            "Research on blood pressure regulation",
            "Explicit disease-driven research"
        ],
        "diseases": ["Cardiovascular disorders", "Heart disease", "Hypertension"],
        "secondary_motivation": None
    },
    "Luera et al. (2025) - CCC FA25.txt": {
        "title": "Region-Specific NPF/NPFR Signaling",
        "motivation": "Basic Cellular Biology",
        "motivation_evidence": [
            "Focus on feeding behavior signaling",
            "No disease driving research",
            "Goal: understanding neuroendocrine signaling"
        ],
        "diseases": [],
        "secondary_motivation": None
    },
    "Meraz et al. (2023) - CCC SP23.txt": {
        "title": "Tyrosine Kinase Expression in the Midgut",
        "motivation": "Disease-Motivated Research",
        "motivation_evidence": [
            "Focus on tumor suppressor genes",
            "Research on cancer-related genes",
            "Goal: understanding cancer gene expression"
        ],
        "diseases": ["Cancer"],
        "secondary_motivation": None
    },
    "Nii et al. (2025) - CCC FA25.txt": {
        "title": "Iron-Induced Modulation of Acetyl-CoA Carboxylase",
        "motivation": "Basic Metabolic Biology",
        "motivation_evidence": [
            "Focus on ACC expression and lipid synthesis",
            "Disease mentions are applications",
            "Main goal: iron-dependent metabolic regulation"
        ],
        "diseases": ["Obesity", "Fatty liver disease", "Iron overload disorders"],
        "secondary_motivation": None
    },
    "Otala et al. (2025) - LU SP25.txt": {
        "title": "Fly Gut as model for fatty acid metabolism disorders",
        "motivation": "Basic Metabolic Biology",
        "motivation_evidence": [
            "Focus on fatty acid metabolism genes",
            "Primary goal: validating fly as model",
            "Disease mentions are context"
        ],
        "diseases": ["MCADD", "Cystic fibrosis", "COPD", "Cancer"],
        "secondary_motivation": None
    },
    "Paderna et al. (2025) - CCC SP25.txt": {
        "title": "Albinism and Melanogenesis Pathway Analysis",
        "motivation": "Disease-Motivated Research",
        "motivation_evidence": [
            "Title mentions Albinism",
            "Research on OCA4 gene mutations",
            "Goal: understanding albinism genes"
        ],
        "diseases": ["Oculocutaneous albinism type 4", "Albinism"],
        "secondary_motivation": None
    },
    "Paramo-Ojeda et al. (2025) - CCC SP25.txt": {
        "title": "Ras85D Expression: Model for KRAS-Driven Colon Cancer",
        "motivation": "Disease-Motivated Research",
        "motivation_evidence": [
            "Title mentions KRAS-Driven Colon Cancer",
            "Focus on oncogenes and tumor suppressors",
            "Goal: modeling cancer pathways"
        ],
        "diseases": ["Cancer", "Colon cancer", "Colorectal cancer"],
        "secondary_motivation": None
    },
    "Pedireddi et al. (2025) - CCC SP25.txt": {
        "title": "Beyond the Anterior: Amylase Gene Expression",
        "motivation": "Basic Cellular Biology",
        "motivation_evidence": [
            "Focus on polysaccharide digestion",
            "No disease driving research",
            "Goal: understanding digestive enzyme distribution"
        ],
        "diseases": [],
        "secondary_motivation": None
    },
    "Rodriguez (2025) - CCC SP25.txt": {
        "title": "Differential Gene Expression of Galm1",
        "motivation": "Disease-Motivated Research",
        "motivation_evidence": [
            "Introduction on galactosemia",
            "Focus on GALM gene mutations",
            "Research motivated by disease"
        ],
        "diseases": ["Galactosemia"],
        "secondary_motivation": None
    },
    "Sakana et al. (2025) - CCC SP25.txt": {
        "title": "Differential Expression of TALE Homeobox Genes",
        "motivation": "Other",
        "motivation_evidence": [
            "Focus on developmental patterning",
            "No disease or specific biological process focus",
            "Goal: understanding gene regulation in development"
        ],
        "diseases": [],
        "alternative_category": "Developmental Biology",
        "alternative_definition": "Research on genes controlling tissue patterning and development."
    },
    "Trevino et al. (2022) - CCC SP22.txt": {
        "title": "Drosophila as Model System of Zellweger Spectrum Disorder",
        "motivation": "Disease-Motivated Research",
        "motivation_evidence": [
            "Title mentions Zellweger Spectrum Disorder",
            "Research on peroxisomal disorder genes",
            "Goal: validating Drosophila as disease model"
        ],
        "diseases": ["Zellweger Spectrum Disorder", "Peroxisomal disorders"],
        "secondary_motivation": None
    },
    "Tuttle et al. (2025) - CCC SP25.txt": {
        "title": "Gene Expression in Tryptophan-Kynurenine Pathway",
        "motivation": "Basic Cellular Biology",
        "motivation_evidence": [
            "Focus on tryptophan metabolism and aging",
            "No disease driving research",
            "Goal: understanding metabolism-aging connection"
        ],
        "diseases": [],
        "secondary_motivation": None
    },
    "Zlaket et al. (2023) - CCC SP23.txt": {
        "title": "ScpX: A Peroxisomal Gene and its Paralogs",
        "motivation": "Disease-Motivated Research",
        "motivation_evidence": [
            "Introduction on Zellweger's Syndrome",
            "Research on SCP2 gene function",
            "Focus on disease-related genes"
        ],
        "diseases": ["Zellweger's Syndrome"],
        "secondary_motivation": None
    }
}

category_definitions = {
    "Disease-Motivated Research": {
        "description": "Research explicitly motivated by understanding, diagnosing, or treating specific human diseases.",
        "examples": "Studies on autism, Rett syndrome, Parkinson's, cancer, cardiovascular disorders."
    },
    "Basic Metabolic Biology": {
        "description": "Research focused on understanding metabolic processes, nutrient metabolism, and energy homeostasis.",
        "examples": "Studies of carbohydrate metabolism, fatty acid synthesis, energy homeostasis genes."
    },
    "Basic Cellular Biology": {
        "description": "Research focused on fundamental cellular processes and physiological functions.",
        "examples": "Studies of immune function, digestion, aging, neuroendocrine signaling."
    },
    "Other": {
        "description": "Research that does not clearly fit into the above categories.",
        "examples": "Studies of developmental patterning, tissue organization."
    }
}

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        
    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.cell(0, 10, 'C-MOOR Research Poster Analysis', align='C')
        self.ln(5)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def generate_report1():
    pdf = PDF()
    pdf.add_page()
    
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 15, 'Report 1: Research Motivation Categories', align='C')
    pdf.ln(10)
    
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 5, f"Generated: {datetime.now().strftime('%Y-%m-%d')}")
    pdf.ln(10)
    
    # Count categories
    category_counts = {}
    category_posters = {}
    for poster, data in posters_data.items():
        cat = data["motivation"]
        category_counts[cat] = category_counts.get(cat, 0) + 1
        if cat not in category_posters:
            category_posters[cat] = []
        category_posters[cat].append(poster)
    
    # Summary table
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, 'Part 1: Category Summary')
    pdf.ln(8)
    
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_fill_color(200, 200, 200)
    pdf.cell(60, 7, 'Category', border=1, fill=True)
    pdf.cell(20, 7, 'Count', border=1, fill=True)
    pdf.cell(30, 7, 'Percentage', border=1, fill=True)
    pdf.ln()
    
    pdf.set_font('Helvetica', '', 10)
    total = sum(category_counts.values())
    for cat in ["Disease-Motivated Research", "Basic Metabolic Biology", "Basic Cellular Biology", "Other"]:
        if cat in category_counts:
            count = category_counts[cat]
            pct = (count / total) * 100
            pdf.cell(60, 6, cat, border=1)
            pdf.cell(20, 6, str(count), border=1, align='C')
            pdf.cell(30, 6, f'{pct:.1f}%', border=1, align='C')
            pdf.ln()
    
    pdf.ln(10)
    
    # Category details
    for cat in ["Disease-Motivated Research", "Basic Metabolic Biology", "Basic Cellular Biology", "Other"]:
        if cat not in category_counts:
            continue
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(0, 8, f"{cat} ({category_counts[cat]} posters)")
        pdf.ln(6)
        
        pdf.set_font('Helvetica', 'I', 9)
        pdf.multi_cell(0, 5, f"Definition: {category_definitions[cat]['description']}")
        pdf.ln(2)
        
        pdf.set_font('Helvetica', '', 9)
        pdf.multi_cell(0, 5, f"Examples: {category_definitions[cat]['examples']}")
        pdf.ln(3)
        
        pdf.set_font('Helvetica', 'B', 9)
        pdf.cell(0, 5, "Posters:")
        pdf.ln(4)
        
        pdf.set_font('Helvetica', '', 8)
        for poster in sorted(category_posters[cat]):
            name = poster.replace('.txt', '')[:50]
            pdf.cell(0, 4, f"  - {name}")
            pdf.ln(3)
        pdf.ln(5)
    
    # Part 2: Individual posters
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, 'Part 2: Individual Poster Evidence')
    pdf.ln(10)
    
    for poster in sorted(posters_data.keys()):
        data = posters_data[poster]
        
        if pdf.get_y() > 250:
            pdf.add_page()
        
        name = poster.replace('.txt', '')[:55]
        pdf.set_font('Helvetica', 'B', 10)
        pdf.cell(0, 6, name)
        pdf.ln(5)
        
        pdf.set_font('Helvetica', '', 9)
        pdf.cell(0, 4, f"Category: {data['motivation']}")
        pdf.ln(5)
        
        pdf.set_font('Helvetica', 'I', 8)
        for evidence in data['motivation_evidence'][:3]:
            pdf.cell(0, 4, f"  - {evidence[:70]}")
            pdf.ln(4)
        
        if data.get('secondary_motivation'):
            pdf.set_font('Helvetica', 'I', 8)
            pdf.cell(0, 4, f"Note: {data['secondary_motivation'][:60]}")
            pdf.ln(3)
        
        if data['motivation'] == "Other" and 'alternative_category' in data:
            pdf.set_font('Helvetica', 'I', 8)
            pdf.cell(0, 4, f"Alternative: {data['alternative_category']}")
            pdf.ln(3)
        
        pdf.ln(5)
    
    return pdf

def generate_report2():
    pdf = PDF()
    pdf.add_page()
    
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 15, 'Report 2: Human Diseases Mentioned', align='C')
    pdf.ln(10)
    
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 5, f"Generated: {datetime.now().strftime('%Y-%m-%d')}")
    pdf.ln(10)
    
    # Part 1: Table
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, 'Part 1: Poster-Disease Reference Table')
    pdf.ln(8)
    
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(200, 200, 200)
    pdf.cell(55, 6, 'Poster', border=1, fill=True)
    pdf.cell(55, 6, 'Diseases Mentioned', border=1, fill=True)
    pdf.ln()
    
    pdf.set_font('Helvetica', '', 8)
    for poster in sorted(posters_data.keys()):
        data = posters_data[poster]
        name = poster.replace('.txt', '')[:30]
        diseases = "; ".join(data['diseases'][:2]) if data['diseases'] else "None"
        if len(diseases) > 30:
            diseases = diseases[:27] + "..."
        
        pdf.cell(55, 5, name, border=1)
        pdf.cell(55, 5, diseases, border=1)
        pdf.ln()
    
    # Part 2: Broader analysis
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, 'Part 2: Broader Disease Category Analysis')
    pdf.ln(8)
    
    # Count statistics
    posters_with_disease = sum(1 for d in posters_data.values() if d['diseases'])
    
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 5, f"Posters with diseases mentioned: {posters_with_disease} ({posters_with_disease/27*100:.1f}%)")
    pdf.ln(5)
    pdf.cell(0, 5, f"Posters with no diseases: {27 - posters_with_disease} ({(27-posters_with_disease)/27*100:.1f}%)")
    pdf.ln(10)
    
    # Broader categories
    broader_cats = {
        "Neurological/Neurodevelopmental": ["Autism", "Parkinson's", "Alzheimer's", "Rett syndrome", "Schizophrenia"],
        "Metabolic Disorders": ["Diabetes", "Obesity", "Galactosemia", "Fatty liver disease"],
        "Cancer": ["Cancer", "Colon cancer", "Melanoma"],
        "Cardiovascular": ["Cardiovascular disorders", "Heart disease", "Hypertension"],
        "Gastrointestinal": ["Acid reflux", "Crohn's disease"],
        "Genetic/Rare Diseases": ["Zellweger", "Albinism"]
    }
    
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(60, 7, 'Disease Category', border=1, fill=True)
    pdf.cell(30, 7, '# Posters', border=1, fill=True)
    pdf.cell(30, 7, 'Percentage', border=1, fill=True)
    pdf.ln()
    
    pdf.set_font('Helvetica', '', 9)
    for broad_cat, keywords in broader_cats.items():
        count = 0
        for poster, data in posters_data.items():
            for disease in data['diseases']:
                if any(kw.lower() in disease.lower() for kw in keywords):
                    count += 1
                    break
        
        pct = (count / 27) * 100
        pdf.cell(60, 6, broad_cat, border=1)
        pdf.cell(30, 6, str(count), border=1, align='C')
        pdf.cell(30, 6, f'{pct:.1f}%', border=1, align='C')
        pdf.ln()
    
    return pdf

def generate_report3():
    pdf = PDF()
    pdf.add_page()
    
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 15, 'Report 3: Technical Analysis Summary', align='C')
    pdf.ln(10)
    
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 5, f"Generated: {datetime.now().strftime('%Y-%m-%d')}")
    pdf.ln(10)
    
    # Prompt
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'Original Analysis Prompt')
    pdf.ln(6)
    
    pdf.set_font('Helvetica', '', 8)
    prompt = """I am part of a team of researchers doing a study on student research posters. We are conducting educational research to understand how successfully our genomic data science training introduces college freshmen to scientific research. We have a total of 29 posters extracted using OCR. Please conduct a thematic analysis of the raw text files. Analyze all posters for motivation and sort into up to 5 categories plus "Other". Generate PDF reports for motivation categories, diseases mentioned, and technical summary."""
    pdf.multi_cell(0, 4, prompt)
    pdf.ln(8)
    
    # AI Info
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'AI Model and Software Information')
    pdf.ln(6)
    
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 5, "AI Model:")
    pdf.ln(4)
    pdf.set_font('Helvetica', '', 9)
    pdf.cell(0, 4, "  Model: GLM 5 (Zhipu AI)")
    pdf.ln(4)
    pdf.cell(0, 4, "  Version: GLM-5-0413")
    pdf.ln(4)
    pdf.cell(0, 4, "  Provider: Vercel AI (zai/glm-5)")
    pdf.ln(8)
    
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 5, "Software Used:")
    pdf.ln(4)
    pdf.set_font('Helvetica', '', 9)
    pdf.cell(0, 4, "  Python 3.12.x - Programming language")
    pdf.ln(4)
    pdf.cell(0, 4, "  FPDF2 2.7.x - PDF generation library")
    pdf.ln(4)
    pdf.cell(0, 4, "  Debian GNU/Linux 12 - Operating system")
    pdf.ln(8)
    
    # Methodology
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'Analysis Methodology')
    pdf.ln(6)
    
    pdf.set_font('Helvetica', '', 9)
    pdf.multi_cell(0, 4, "1. Located 27 raw text files in OCR 1.1/Raw directory")
    pdf.ln(2)
    pdf.multi_cell(0, 4, "2. Read all poster text files in parallel")
    pdf.ln(2)
    pdf.multi_cell(0, 4, "3. Analyzed all 27 posters holistically for motivational themes")
    pdf.ln(2)
    pdf.multi_cell(0, 4, "4. Identified 3 primary categories plus 'Other' after reviewing ALL posters")
    pdf.ln(2)
    pdf.multi_cell(0, 4, "5. Extracted supporting evidence from poster text")
    pdf.ln(8)
    
    # Output files
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'Output Files Generated')
    pdf.ln(6)
    
    pdf.set_font('Helvetica', '', 9)
    pdf.cell(0, 4, "  Directory: Documents/OCR 1.1/AI_model5_Prompt2/")
    pdf.ln(4)
    pdf.cell(0, 4, "  - Report1_Motivation_Categories.pdf")
    pdf.ln(4)
    pdf.cell(0, 4, "  - Report2_Diseases_Mentioned.pdf")
    pdf.ln(4)
    pdf.cell(0, 4, "  - Report3_Technical_Summary.pdf")
    pdf.ln(4)
    pdf.cell(0, 4, "  - analysis_script.py")
    
    return pdf

def main():
    output_dir = "/home/workspace/Documents/OCR 1.1/AI_model5_Prompt2"
    
    pdf1 = generate_report1()
    pdf1.output(os.path.join(output_dir, "Report1_Motivation_Categories.pdf"))
    print(f"Generated: Report1_Motivation_Categories.pdf")
    
    pdf2 = generate_report2()
    pdf2.output(os.path.join(output_dir, "Report2_Diseases_Mentioned.pdf"))
    print(f"Generated: Report2_Diseases_Mentioned.pdf")
    
    pdf3 = generate_report3()
    pdf3.output(os.path.join(output_dir, "Report3_Technical_Summary.pdf"))
    print(f"Generated: Report3_Technical_Summary.pdf")
    
    print("\nAll reports generated successfully!")

if __name__ == "__main__":
    main()
