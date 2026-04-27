#!/usr/bin/env python3
"""
OCR Text Cleaner v2 for Scientific Research Posters

Improvements:
1. Fix numbers with spaced digits (2 0 2 4 -> 2024)
2. Better garbled text removal
3. Better sentence reconstruction
4. Better handling of figure/table labels

Usage:
    python ocr_cleanup_v2.py <input_file> [output_file]
"""

import sys
import re
from pathlib import Path


def fix_spaced_numbers(text):
    """Fix numbers that have spaces between digits (common OCR error)."""
    # Pattern: digit space digit -> digit
    # Keep doing this until no more changes
    result = text
    while True:
        # Match: digit followed by optional spaces, then more digits
        new_result = re.sub(r'(\d)\s+(\d)', r'\1\2', result)
        if new_result == result:
            break
        result = new_result
    return result


def fix_spaced_numbers_aggressive(text):
    """More aggressive version that handles years like "2 0 2 4"."""
    # First handle the spaced digit pattern
    result = re.sub(r'(\d)\s+(\d)\s+(\d)\s+(\d)', r'\1\2\3\4', text)
    result = re.sub(r'(\d)\s+(\d)\s+(\d)', r'\1\2\3', result)
    result = re.sub(r'(\d)\s+(\d)', r'\1\2', result)
    return result


def remove_figure_labels(text):
    """Remove common figure labels and axis labels from results."""
    patterns = [
        # Axis labels and data labels
        r'\b(AL|A1|a1|p1|p2|p3|Cu|Cu1|Cu2|PL|R1|R2|R3)\b',
        # Common figure caption patterns
        r'Fig\s*\d+[a-z]?.*?(?=\n|$)',
        r'Figure\s*\d+.*?(?=\n|$)',
        r'Supplementary.*?(?=\n|$)',
        # Statistical labels
        r'p\s*[<>=]\s*\d+\.?\d*',
        r'adj\s*p.*?(?=\n|$)',
        r'FDR.*?(?=\n|$)',
        # Numeric patterns that look like axis ticks or data points
        r'^\d+\.?\d*\s*$',
        # Specific gene names followed by garbled text
        r'(Acox3|Muc68E|Mdh1)\s+[a-z]\s*[a-z]\s*[a-z]',
    ]
    
    result = text
    for pattern in patterns:
        result = re.sub(pattern, '', result, flags=re.IGNORECASE)
    
    return result


def is_garbled_line(line):
    """Check if a line is garbled beyond repair."""
    if not line or len(line.strip()) < 3:
        return True
        
    # Count letters vs other characters
    letters = sum(1 for c in line if c.isalpha())
    total = len(line.strip())
    
    if total == 0:
        return True
    
    # If less than 30% are letters, likely garbled
    if letters / total < 0.3:
        return True
    
    # Check for common garbled patterns
    garbled_patterns = [
        r'^[a-z]\s+[a-z]\s+[a-z]\s*$',  # single letters separated by spaces
        r'^[^a-zA-Z]*$',  # no letters at all
        r'^\s*[A-Z]\s*[A-Z]\s*[A-Z]\s*$',  # multiple single capitals
    ]
    
    for pattern in garbled_patterns:
        if re.match(pattern, line):
            return True
    
    return False


def should_join_lines(current, next_line):
    """Determine if two lines should be joined."""
    if not current or not next_line:
        return False
    
    current = current.strip()
    next_line = next_line.strip()
    
    if not current or not next_line:
        return False
    
    # If current ends with lowercase and next starts lowercase, join
    if current[-1].isalpha() and current[-1].islower() and next_line[0].isalpha() and next_line[0].islower():
        return True
    
    # If current ends with continuation punctuation, join
    if current[-1] in ',;:(' and next_line[0].islower():
        return True
    
    # If next line is short and starts lowercase, likely continuation
    if len(next_line) < 60 and next_line[0].islower() and len(current) < 100:
        return True
    
    return False


def fix_line_breaks_v2(text):
    """Improved line break fixing."""
    lines = text.split('\n')
    fixed = []
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines
        if not line:
            fixed.append('')
            i += 1
            continue
        
        # Check if should join with next line(s)
        while i + 1 < len(lines) and should_join_lines(line, lines[i + 1]):
            next_line = lines[i + 1].strip()
            line = line + ' ' + next_line
            i += 1
        
        fixed.append(line)
        i += 1
    
    return '\n'.join(fixed)


def remove_short_garbled_lines(text):
    """Remove lines that are likely garbled but preserve meaningful short lines."""
    lines = text.split('\n')
    cleaned = []
    
    for line in lines:
        line = line.strip()
        
        # Skip completely empty
        if not line:
            cleaned.append('')
            continue
        
        # Skip if too short and likely garbled (but preserve bullet points)
        if len(line) < 4 and not line.startswith('+') and not line.startswith('-') and not line.startswith('*'):
            # Check if it's meaningful
            if not any(c.isalpha() for c in line):
                continue
        
        # Skip lines that are just noise
        if is_garbled_line(line):
            continue
            
        cleaned.append(line)
    
    return '\n'.join(cleaned)


def apply_fixes(text):
    """Apply all OCR corrections."""
    result = text
    
    # Fix spaced numbers first (year-like patterns)
    result = fix_spaced_numbers_aggressive(result)
    
    # Fix common typos
    fixes = [
        (r'\bFemandez\b', 'Fernandez'),
        (r'\bMuc683\b', 'Muc68E'),
        (r'\bMuc68E3\b', 'Muc68E'),
        (r'\bClustrProfiler\b', 'ClusterProfiler'),
        (r'\bclustrprofiler\b', 'ClusterProfiler'),
        (r'\bDESeq2\?\b', 'DESeq2'),
        (r'\bDESeq\?', 'DESeq2'),
        (r'\bdeseq\b', 'DESeq2'),
        (r'\bFlyBase\b', 'FlyBase'),
        (r'\bFly Base\b', 'FlyBase'),
        (r'\bprota\b', 'protein'),
        (r'\bprot\b', 'protein'),
        (r'\bosterior\b', 'posterior'),
        (r'\banterior\b', 'anterior'),
        (r'\bcentral\b', 'central'),
        (r'\bsorption\b', 'absorption'),
        (r'\blipids\b', 'lipids'),
        (r'\bencode?s?\b', 'encodes'),
        (r'\bmucin\b', 'mucin'),
        (r'\bepithelial\b', 'epithelial'),
        (r'\bmetabolism\b', 'metabolism'),
        (r'\bmetabol(?:ism|ic)\b', 'metabolism'),
        (r'\bcritical\b', 'critical'),
        (r'\btissues?\b', 'tissues'),
        (r'\blevels?\b', 'levels'),
        (r'\bdifferent\b', 'different'),
        (r'\bregions?\b', 'regions'),
        (r'\bcells?\b', 'cells'),
        (r'\bmore\b', 'more'),
        (r'\btheir\b', 'their'),
        (r'\bwhich\b', 'which'),
        (r'\bthese\b', 'these'),
        (r'\bshows?\b', 'shows'),
        # Fix hyphenation artifacts
        (r'(\w+)-\s*\n\s*(\w+)', r'\1\2'),
        (r'(\w+)\s+-\s+(\w+)', r'\1-\2'),
        # Fix sentence fragments
        (r'\bfly gut\b', 'fly gut'),
        (r'\bhuman body\b', 'human body'),
        (r'\bdisease mechanisms\b', 'disease mechanisms'),
        (r'\btherapeutic strategies\b', 'therapeutic strategies'),
    ]
    
    for pattern, replacement in fixes:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    
    return result


def fix_discussion_section(text):
    """Special handling for discussion section that got fragmented."""
    # If discussion content is fragmented, try to reconstruct
    lines = text.split('\n')
    fixed_lines = []
    in_discussion = False
    
    for line in lines:
        line = line.strip()
        
        # Skip the header
        if line.upper().startswith('DISCUSSION'):
            in_discussion = True
            fixed_lines.append('Discussion')
            continue
        
        if not line:
            fixed_lines.append('')
            continue
        
        # Join fragmented sentences
        if in_discussion and line and not line.startswith('+') and not line.startswith('-'):
            if fixed_lines and fixed_lines[-1] and fixed_lines[-1][-1].islower():
                fixed_lines[-1] = fixed_lines[-1] + ' ' + line
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)


def process_section(section_name, content):
    """Process a single section."""
    if not content or content == '[Not detected]':
        return f'\n{"="*70}\nSECTION: {section_name}\n{"="*70}\n\n[Not detected]\n'
    
    # Apply fixes
    result = content
    
    # Remove figure labels if Results section
    if section_name == 'RESULTS':
        result = remove_figure_labels(result)
    
    # Remove garbled lines
    result = remove_short_garbled_lines(result)
    
    # Fix line breaks
    result = fix_line_breaks_v2(result)
    
    # Apply OCR fixes
    result = apply_fixes(result)
    
    # Clean up extra whitespace
    result = re.sub(r'\n{3,}', '\n\n', result)
    result = re.sub(r' +', ' ', result)
    
    # Fix discussion specifically
    if section_name == 'DISCUSSION':
        result = fix_discussion_section(result)
    
    return f'\n{"="*70}\nSECTION: {section_name}\n{"="*70}\n\n{result.strip()}\n'


def cleanup_ocr_text_v2(input_file, output_file=None):
    """Main cleanup function v2."""
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Parse sections
    sections = {}
    current_section = 'HEADER'
    current_content = []
    
    for line in text.split('\n'):
        line_upper = line.strip().upper()
        
        if 'SECTION: INTRODUCTION' in line_upper:
            sections[current_section] = '\n'.join(current_content)
            current_section = 'INTRODUCTION'
            current_content = []
        elif 'SECTION: METHODS' in line_upper:
            sections[current_section] = '\n'.join(current_content)
            current_section = 'METHODS'
            current_content = []
        elif 'SECTION: RESULTS' in line_upper:
            sections[current_section] = '\n'.join(current_content)
            current_section = 'RESULTS'
            current_content = []
        elif 'SECTION: DISCUSSION' in line_upper:
            sections[current_section] = '\n'.join(current_content)
            current_section = 'DISCUSSION'
            current_content = []
        else:
            current_content.append(line)
    
    sections[current_section] = '\n'.join(current_content)
    
    # Process each section
    output = f'RESEARCH POSTER OCR RESULTS\n{"="*70}\n\n'
    
    for section in ['INTRODUCTION', 'METHODS', 'RESULTS', 'DISCUSSION']:
        if section in sections:
            output += process_section(section, sections[section])
    
    # Write output
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Cleaned text saved to: {output_file}")
    else:
        print(output)
    
    return output


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python ocr_cleanup_v2.py <input_file> [output_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    cleanup_ocr_text_v2(input_file, output_file)