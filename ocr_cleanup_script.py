#!/usr/bin/env python3
"""
OCR Text Cleanup Script

This script cleans up OCR text from research posters by:
1. Removing section headers (except the first occurrence)
2. Removing headers/footers from pages
3. Fixing common OCR errors
4. Fixing line breaks in the middle of thoughts
5. Fixing common typos

Usage: python3 ocr_cleanup_script.py <input_file> [output_file]
If no output file is specified, saves as input_file_cleaned.txt
"""

import sys
import re

def clean_ocr_text(text):
    """Clean up OCR text with various fixes."""
    if not text or len(text) == 0:
        return text
    
    cleaned = text
    
    # 1. Remove soft hyphens at line breaks
    cleaned = re.sub(r'-\n', '', cleaned)
    
    # 2. Fix common OCR character swaps
    cleaned = re.sub(r'\|', 'I', cleaned)  # Pipe to letter I
    cleaned = re.sub(r'\\midgut', 'midgut', cleaned)  # Fix \midgut
    cleaned = re.sub(r'\\alpha', 'alpha', cleaned)
    cleaned = re.sub(r'\\beta', 'beta', cleaned)
    cleaned = re.sub(r'\\gamma', 'gamma', cleaned)
    
    # 3. Fix common gene name errors
    cleaned = re.sub(r'\bDESeq\d*\b', 'DESeq2', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\bCluster\s*Profiler\b', 'ClusterProfiler', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\bClustr\s*Profiler\b', 'ClusterProfiler', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\bFlyBase\b', 'FlyBase', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\bDrosophila\b', 'Drosophila', cleaned, flags=re.IGNORECASE)
    
    # 4. Fix word splits at line breaks
    cleaned = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', cleaned)
    
    # 5. Normalize whitespace
    cleaned = re.sub(r'[ \t]+', ' ', cleaned)  # Multiple spaces to single
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)  # Multiple newlines to double
    
    # 6. Remove reference numbers like [1], (1), 1. at start of lines in references
    cleaned = re.sub(r'\n\s*\[\d+\]\s*', '\n', cleaned)
    cleaned = re.sub(r'\n\s*\(\d+\)\s*', '\n', cleaned)
    cleaned = re.sub(r'\n\s*\d+\.\s*', '\n', cleaned)
    
    # 7. Fix common OCR typos
    common_typos = {
        r'\bfatty\s*acid\b': 'fatty acid',
        r'\bmid\s*gut\b': 'midgut',
        r'\bDrosophiia\b': 'Drosophila',
        r'\bmelanogoster\b': 'melanogaster',
        r'\bprote in\b': 'protein',
        r'\bexpre ssion\b': 'expression',
        r'\bgene\s*ration\b': 'generation',
        r'\benzyme\b': 'enzyme',
        r'\bmetabol ism\b': 'metabolism',
    }
    for pattern, replacement in common_typos.items():
        cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)
    
    return cleaned.strip()

def group_panels_by_section(results_text):
    """
    Group OCR results by section, combining multiple panels of the same section
    under a single header. Panels are assumed to be in order.
    
    Expected format:
        RESEARCH POSTER OCR RESULTS
        ================================================================================
        
        ================================================================================
        SECTION: INTRODUCTION
        ================================================================================
        
        [intro text panel 1]
        
        [intro text panel 2 if exists]
        
        ================================================================================
        SECTION: METHODS
        ================================================================================
        
        [methods text panel 1]
        
        ...
    """
    lines = results_text.split('\n')
    output_lines = []
    current_section = None
    section_order = []
    section_content = {}
    in_results = False
    
    header_pattern = re.compile(r'^=+$')
    section_pattern = re.compile(r'^SECTION:\s*(.+)$', re.IGNORECASE)
    results_header = 'RESEARCH POSTER OCR RESULTS'
    
    for i, line in enumerate(lines):
        # Keep the header
        if results_header in line:
            in_results = True
            continue
        
        if header_pattern.match(line):
            # Skip separator lines
            continue
        
        section_match = section_pattern.match(line.strip())
        if section_match:
            section_name = section_match.group(1).strip().upper()
            if section_name not in section_content:
                section_order.append(section_name)
                section_content[section_name] = []
            current_section = section_name
            continue
        
        # Content line
        if current_section and line.strip():
            section_content[current_section].append(line)
    
    # Build output with single header per section
    output_lines.append(results_header)
    output_lines.append('=' * 80)
    output_lines.append('')
    
    for section in section_order:
        output_lines.append('=' * 80)
        output_lines.append(f'SECTION: {section}')
        output_lines.append('=' * 80)
        output_lines.append('')
        # Join all content for this section
        if section_content[section]:
            output_lines.append('\n'.join(section_content[section]))
        output_lines.append('')
    
    return '\n'.join(output_lines).strip()

def process_file(input_file, output_file=None):
    """Process a single OCR text file."""
    if output_file is None:
        # Create output filename from input
        if input_file.endswith('.txt'):
            output_file = input_file.replace('.txt', '_cleaned.txt')
        else:
            output_file = input_file + '_cleaned'
    
    # Read input
    with open(input_file, 'r', encoding='utf-8', errors='replace') as f:
        original_text = f.read()
    
    print(f"Processing: {input_file}")
    print(f"Original length: {len(original_text)} characters")
    
    # Step 1: Clean the text
    cleaned_text = clean_ocr_text(original_text)
    print(f"After basic cleaning: {len(cleaned_text)} characters")
    
    # Step 2: Group panels by section (remove duplicate headers)
    grouped_text = group_panels_by_section(cleaned_text)
    print(f"After grouping: {len(grouped_text)} characters")
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(grouped_text)
    
    print(f"Saved to: {output_file}")
    return output_file

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nUsage: python3 ocr_cleanup_script.py <input_file> [output_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        process_file(input_file, output_file)
    except FileNotFoundError:
        print(f"Error: File not found: {input_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()