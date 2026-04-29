#!/usr/bin/env python3
"""
Thematic Analysis of Student Research Posters
Extracts sections, performs thematic categorization, identifies disease mentions.
"""

import os
import re
import json
from collections import defaultdict

RAW_DIR = "/home/workspace/Documents/OCR 1.1/Raw"
OUTPUT_DIR = "/home/workspace/Documents/OCR 1.1/AI_model#_Prompt2"

POSTER_FILES = [
    "Avetisyan et al. (2023) - CCC SP23.txt",
    "Berbouti et al. (2025) - CCC FA25.txt",
    "Brown et al. (2025) - CCC SP25.txt",
    "Cabral et al. (2025) - CCC FA25.txt",
    "Camara et al. (2025) - LU SP25.txt",
    "Dehuelbes et al. (2025) - LU SP5.txt",
    "Diaz et al. (2025) - CCC SP25.txt",
    "Ford et al. (2023) - CCC SP23.txt",
    "Gill & Alcazar (2025) - CCC FA25.txt",
    "Godoy-Pena et al. (2025) - CCC FA25.txt",
    "Haubelt & Alcazar et al. (2025) - CCC FA25.txt",
    "Henriquez et al. (2025) - COD WI24.txt",
    "Holmes (2025) - CCC SP25.txt",
    "Lemus et al. (2025) - FA25 CCC.txt",
    "Logan et al. (2025) - CCC FA25.txt",
    "Luera et al. (2025) - CCC FA25.txt",
    "Meraz et al. (2023) - CCC SP23.txt",
    "Nii et al. (2025) - CCC FA25.txt",
    "Otala et al. (2025) - LU SP25.txt",
    "Paderna et al. (2025) - CCC SP25.txt",
    "Paramo-Ojeda et al. (2025) - CCC SP25.txt",
    "Pedireddi et al. (2025) - CCC SP25.txt",
    "Rodriguez (2025) - CCC SP25.txt",
    "Sakana et al. (2025) - CCC SP25.txt",
    "Trevino et al. (2022) - CCC SP22.txt",
    "Tuttle et al. (2025) - CCC SP25.txt",
    "Zlaket et al. (2023) - CCC SP23.txt",
]


def extract_sections(filepath):
    """Parse a poster file and return dict of section -> content."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        raw = f.read()

    sections = {}
    # Split on SECTION: headers
    pattern = re.compile(r'^={20,}\s*\nSECTION:\s*(\w+)\s*\n={20,}\s*\n', re.MULTILINE)
    parts = pattern.split(raw)

    # parts[0] is before first header (garbage), then [section_name, content, section_name, content, ...]
    if len(parts) > 1:
        for i in range(1, len(parts), 2):
            if i+1 < len(parts):
                sec_name = parts[i].strip().upper()
                sec_content = parts[i+1].strip()
                sections[sec_name] = sec_content
    return sections


def get_analysis_text(sections):
    """Combine sections relevant for thematic analysis (excluding AUTHORS and REFERENCES)."""
    relevant = ['TITLE', 'ABSTRACT', 'INTRODUCTION', 'METHODS', 'RESULTS', 'DISCUSSION', 'OTHER']
    texts = []
    for sec in relevant:
        if sec in sections:
            texts.append(sections[sec])
    return '\n\n'.join(texts)


def get_disease_text(sections):
    """Combine all text for disease search."""
    exclude = ['AUTHORS', 'REFERENCES']
    texts = []
    for sec, content in sections.items():
        if sec not in exclude:
            texts.append(content)
    return '\n\n'.join(texts)


def load_all_posters():
    """Load all poster files and return a dict of filename -> sections."""
    posters = {}
    for fname in POSTER_FILES:
        fpath = os.path.join(RAW_DIR, fname)
        if os.path.exists(fpath):
            sections = extract_sections(fpath)
            posters[fname] = sections
        else:
            print(f"WARNING: File not found: {fpath}")
    return posters


if __name__ == "__main__":
    posters = load_all_posters()
    print(f"Loaded {len(posters)} posters")
    for fname, sections in posters.items():
        print(f"  {fname}: sections = {list(sections.keys())}")
