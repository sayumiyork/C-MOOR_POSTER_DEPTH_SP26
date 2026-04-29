#!/usr/bin/env python3
"""
Thematic Analysis of Student Research Posters
Analysis script for genomic data science training capstone posters

This script performs:
1. Thematic analysis of research motivation categories
2. Disease mentions analysis  
3. Technical methods documentation

Author: MiniMax 2 (AI Assistant)
Model: MiniMax 4.1
Date: 2026-04-28
"""

import os
import re
from pathlib import Path
from collections import defaultdict

# ============================================================================
# CONFIGURATION
# ============================================================================

RAW_DIR = Path("/home/workspace/Documents/OCR 1.1/Raw")
OUTPUT_DIR = Path("/home/workspace/Documents/OCR 1.1/AI_model_Prompt2")

# Categories for thematic analysis
CATEGORIES = {
    "Disease-Motivated": "Research focused on understanding, treating, or modeling specific human diseases. Examples include cancer, metabolic disorders, neurological conditions.",
    "Translational Science": "Research focused on applying findings from model organisms to understand human biology, disease mechanisms, or therapeutic targets.",
    "Basic Biology": "Research focused on fundamental biological processes, gene functions, or molecular mechanisms without explicit disease focus.",
    "Metabolic/Physiological": "Research focused on metabolic processes, nutrient processing, energy balance, or physiological functions in the gut.",
    "Model Organism Validation": "Research focused on validating Drosophila or other model organisms as appropriate systems for studying human biology/disease."
}

# Disease categories for analysis
DISEASE_CATEGORIES = {
    "Neurological/Neurodevelopmental": ["autism", "rett syndrome", "parkinson", "alzheimer", "schizophrenia", " ptsd", "depression", "epilepsy", "neurodegenerative", "neurodevelopmental"],
    "Metabolic Disorders": ["diabetes", "obesity", "metabolic syndrome", "fatty liver", "mcadd", "galactosemia", "zellweger"],
    "Cancer": ["cancer", "tumor", "carcinoma", "melanoma", "colon cancer", "colorectal", "leukemia", "oncogene", "krast", "ras85d"],
    "Gastrointestinal": ["acid reflux", "gerd", "crohn", "colitis", "ibd", "gastrointestinal", "gut microbiome", "digestive"],
    "Cardiovascular": ["cardiovascular", "heart disease", "hypertension", "blood pressure", "stroke"],
    "Genetic Disorders": ["albinism", "peroxisomal", "peroxisome", "zsd", "zellweger", "genetic disorder"],
    "Immune/Inflammatory": ["immune", "inflammation", "autoimmune", "crohn", "ibd"]
}

# ============================================================================
# POSTER DATA - Full content read from files
# ============================================================================

def read_all_posters():
    """Read all poster text files."""
    posters = {}
    for txt_file in sorted(RAW_DIR.glob("*.txt")):
        filename = txt_file.name
        with open(txt_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        posters[filename] = content
    return posters

# ============================================================================
# ANALYSIS FUNCTIONS
# ============================================================================

def extract_sections(text):
    """Extract relevant sections from poster text, excluding authors and references."""
    sections = {}
    
    # Define section patterns
    section_patterns = [
        (r'SECTION:\s*TITLE\s*\n+(.*?)(?=SECTION:|$)', 'title'),
        (r'SECTION:\s*ABSTRACT\s*\n+(.*?)(?=SECTION:|$)', 'abstract'),
        (r'SECTION:\s*INTRODUCTION\s*\n+(.*?)(?=SECTION:|$)', 'introduction'),
        (r'SECTION:\s*METHODS\s*\n+(.*?)(?=SECTION:|$)', 'methods'),
        (r'SECTION:\s*RESULTS\s*\n+(.*?)(?=SECTION:|$)', 'results'),
        (r'SECTION:\s*DISCUSSION\s*\n+(.*?)(?=SECTION:|$)', 'discussion'),
    ]
    
    for pattern, name in section_patterns:
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            sections[name] = match.group(1).strip()
    
    return sections

def assign_category(poster_name, sections):
    """
    Assign a research motivation category based on content analysis.
    Returns (category, reasoning_bullets)
    """
    text = ' '.join(sections.values()).lower()
    
    # Check for disease mentions
    disease_mentions = []
    disease_patterns = {
        'autism': ['autism', 'asd', 'autism spectrum'],
        'rett syndrome': ['rett syndrome'],
        'parkinson': ['parkinson'],
        'alzheimer': ['alzheimer'],
        'cancer': ['cancer', 'tumor', 'oncogene', 'krast', 'ras85d', 'colon cancer', 'colorectal'],
        'diabetes': ['diabetes', 'diabetic'],
        'obesity': ['obesity', 'metabolic syndrome', 'fatty liver'],
        'acid reflux': ['acid reflux', 'gerd'],
        'galactosemia': ['galactosemia'],
        'zellweger': ['zellweger'],
        'cardiovascular': ['cardiovascular', 'blood pressure', 'hypertension'],
    }
    
    for disease, patterns in disease_patterns.items():
        for pattern in patterns:
            if pattern in text:
                disease_mentions.append(disease)
                break
    
    # Check for disease-specific gene mentions
    disease_gene_patterns = [
        ('mecp2', 'Neurological/Neurodevelopmental - Rett syndrome research'),
        ('drd2', 'Neurological/Neurodevelopmental - Parkinson disease research'),
        ('kras', 'Cancer - KRAS-driven cancer research'),
        ('ras85d', 'Cancer - RAS pathway in cancer'),
        ('slc45a2', 'Genetic Disorders - Albinism research'),
        ('abcd1', 'Genetic Disorders - Zellweger spectrum disorder'),
    ]
    
    for gene, disease_desc in disease_gene_patterns:
        if gene in text:
            disease_mentions.append(disease_desc)
    
    # Check for explicit disease modeling statements
    disease_modeling = any([
        'model for' in text and ('disease' in text or 'disorder' in text),
        'human disease' in text,
        'treat' in text and 'disease' in text,
        'cancer' in text and 'model' in text,
    ])
    
    # Check for translational focus (model organism to human)
    translational_indicators = [
        'human ortholog',
        'conserved',
        'model organism',
        'drosophila as a model',
        'apply to human',
        'translate to human',
        'relevance to human',
        'human medicine',
        'therapeutic target',
        'treatment of'
    ]
    translational_count = sum(1 for i in translational_indicators if i in text)
    
    # Check for basic biology focus
    basic_biology_indicators = [
        'gene expression pattern',
        'differential expression',
        'regional expression',
        'homeobox gene',
        'transcription factor',
        'developmental patterning',
        'neural development',
    ]
    basic_biology_count = sum(1 for i in basic_biology_indicators if i in text)
    
    # Check for metabolic/physiological focus
    metabolic_indicators = [
        'metabolism',
        'metabolic',
        'lipid',
        'fatty acid',
        'glucose',
        'trehalose',
        'carbohydrate',
        'energy',
        'nutrient absorption',
        'digestion'
    ]
    metabolic_count = sum(1 for i in metabolic_indicators if i in text)
    
    # Decision logic
    reasoning = []
    
    # Prioritize disease-motivated
    if len(disease_mentions) >= 2 or 'rett syndrome' in disease_mentions or 'parkinson' in disease_mentions or 'cancer' in str(disease_mentions):
        if any(x in disease_mentions for x in ['autism', 'rett syndrome', 'parkinson', 'alzheimer']):
            category = "Disease-Motivated"
            reasoning.append(f"Explicit focus on human disease: {', '.join(disease_mentions[:3])}")
        elif any(x in disease_mentions for x in ['cancer', 'tumor']):
            category = "Disease-Motivated"
            reasoning.append(f"Focus on cancer research: {', '.join([x for x in disease_mentions if 'cancer' in x or 'tumor' in x])}")
        elif any(x in disease_mentions for x in ['zellweger', 'galactosemia']):
            category = "Disease-Motivated"
            reasoning.append(f"Focus on genetic/metabolic disorder: {', '.join(disease_mentions)}")
        elif disease_modeling:
            category = "Disease-Motivated"
            reasoning.append("Explicitly studies disease mechanisms or modeling")
        else:
            category = "Disease-Motivated"
            reasoning.append(f"Multiple disease-related genes/targets identified: {', '.join(disease_mentions[:2])}")
    elif translational_count >= 3:
        category = "Translational Science"
        reasoning.append(f"Strong focus on translating findings to human biology (indicator count: {translational_count})")
        if disease_mentions:
            reasoning.append(f"Potential disease connection: {disease_mentions[0]}")
    elif metabolic_count >= 4:
        category = "Metabolic/Physiological"
        reasoning.append(f"Focus on metabolic/physiological processes (indicator count: {metabolic_count})")
        if disease_mentions:
            reasoning.append(f"Disease relevance noted: {disease_mentions[0]}")
    elif basic_biology_count >= 3 and translational_count < 2:
        category = "Basic Biology"
        reasoning.append(f"Focus on fundamental biological mechanisms (indicator count: {basic_biology_count})")
    else:
        category = "Model Organism Validation"
        reasoning.append("Research validates Drosophila as model for human biology")
        if disease_mentions:
            reasoning.append(f"Disease connection: {disease_mentions[0]}")
    
    return category, reasoning

def extract_diseases(text):
    """Extract all human disease mentions from poster text."""
    diseases = []
    text_lower = text.lower()
    
    # Disease terms to search for
    search_terms = {
        'Autism Spectrum Disorder': ['autism', 'asd', 'autism spectrum'],
        'Rett Syndrome': ['rett syndrome'],
        "Parkinson's Disease": ['parkinson'],
        'Alzheimer\'s Disease': ['alzheimer'],
        'Cancer': ['cancer', 'tumor', 'carcinoma', 'melanoma', 'colon cancer', 'colorectal'],
        'Diabetes': ['diabetes', 'diabetic'],
        'Obesity': ['obesity', 'metabolic syndrome'],
        'Fatty Liver Disease': ['fatty liver', 'nafld', 'steatosis'],
        'Acid Reflux/GERD': ['acid reflux', 'gerd'],
        'Galactosemia': ['galactosemia'],
        'Zellweger Spectrum Disorder': ['zellweger', 'zsd'],
        'Cardiovascular Disease': ['cardiovascular', 'heart disease', 'hypertension'],
        'Albinism': ['albinism', 'oca4'],
        'Crohn\'s Disease': ['crohn'],
        'Schizophrenia': ['schizophrenia'],
        'Neurodegenerative disorders': ['neurodegenerative', 'neurodegeneration'],
    }
    
    for disease, terms in search_terms.items():
        for term in terms:
            if term in text_lower:
                # Find the actual context
                pattern = re.compile(r'.{0,50}' + term + r'.{0,50}', re.IGNORECASE)
                matches = pattern.findall(text)
                for match in matches:
                    diseases.append((disease, match.strip()))
                break  # Only add disease once
    
    return diseases

def categorize_diseases(diseases):
    """Categorize diseases into broader categories."""
    categories = defaultdict(list)
    
    category_map = {
        'Autism Spectrum Disorder': 'Neurological/Neurodevelopmental',
        'Rett Syndrome': 'Neurological/Neurodevelopmental',
        "Parkinson's Disease": 'Neurological/Neurodevelopmental',
        'Alzheimer\'s Disease': 'Neurological/Neurodevelopmental',
        'Schizophrenia': 'Neurological/Neurodevelopmental',
        'Neurodegenerative disorders': 'Neurological/Neurodevelopmental',
        'Diabetes': 'Metabolic Disorders',
        'Obesity': 'Metabolic Disorders',
        'Fatty Liver Disease': 'Metabolic Disorders',
        'Galactosemia': 'Metabolic Disorders',
        'Zellweger Spectrum Disorder': 'Metabolic Disorders',
        'Cancer': 'Cancer',
        'Acid Reflux/GERD': 'Gastrointestinal',
        'Crohn\'s Disease': 'Gastrointestinal',
        'Cardiovascular Disease': 'Cardiovascular',
        'Albinism': 'Genetic Disorders',
    }
    
    for disease, context in diseases:
        cat = category_map.get(disease, 'Other')
        categories[cat].append(disease)
    
    return categories

def main():
    print("Reading all poster files...")
    posters = read_all_posters()
    print(f"Loaded {len(posters)} posters")
    
    # Store results
    results = {
        'thematic': {},
        'diseases': {}
    }
    
    # Process each poster
    for filename, content in posters.items():
        sections = extract_sections(content)
        category, reasoning = assign_category(filename, sections)
        results['thematic'][filename] = {
            'category': category,
            'reasoning': reasoning,
            'sections': sections
        }
        
        diseases = extract_diseases(content)
        results['diseases'][filename] = diseases
    
    # Count by category
    category_counts = defaultdict(int)
    category_posters = defaultdict(list)
    
    for filename, data in results['thematic'].items():
        cat = data['category']
        category_counts[cat] += 1
        category_posters[cat].append(filename)
    
    print("\n=== CATEGORY DISTRIBUTION ===")
    for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"{cat}: {count}")
    
    print("\n=== DISEASE MENTIONS ===")
    total_posters_with_disease = sum(1 for d in results['diseases'].values() if d)
    print(f"Posters mentioning diseases: {total_posters_with_disease}")
    
    return results, category_counts, category_posters

if __name__ == "__main__":
    results, category_counts, category_posters = main()
    print("\nAnalysis complete. Ready for report generation.")