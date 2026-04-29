import json
from collections import Counter
from pathlib import Path

def match_terms(text: str, mapping: dict[str, list[str]]) -> set[str]:
    text_low = text.lower()
    return {label for label, terms in mapping.items() if any(term in text_low for term in terms)}

motivation_terms = {
    'Disease mechanism': ['disease', 'disorder', 'cancer', 'syndrome', 'infection', 'pathway', 'regulation', 'homeostasis'],
    'Technology demonstration': ['method', 'tool', 'pipeline', 'platform', 'visualization', 'analysis method', 'modeling'],
    'Model organism validation': ['model organism', 'drosophila', 'fruit fly', 'mouse', 'zebrafish'],
    'Human health application': ['human', 'clinical', 'patient', 'therapy', 'treatment', 'diagnosis', 'medical'],
    'Environmental/Population context': ['population', 'environment', 'ecology', 'community'],
}

category_keywords = {
    'Neurological / Neurodevelopmental': ['autism', 'nerve', 'brain', 'neuro', 'dementia', 'cognitive'],
    'Metabolic / Endocrine': ['metabolic', 'diabetes', 'obesity', 'thyroid', 'insulin', 'gastro', 'cholesterol'],
    'Cancer / Growth control': ['cancer', 'tumor', 'oncology', 'proliferation', 'apoptosis'],
    'Infectious / Immune': ['virus', 'infection', 'immune', 'pathogen', 'bacteria'],
    'Cardiovascular / Circulatory': ['heart', 'cardiac', 'vascular', 'blood', 'blood vessel'],
}

diseases = {
    'Autism spectrum disorder': ['autism', 'asd'],
    'Acid reflux / GERD': ['acid reflux', 'gerd'],
    'Diabetes / metabolic syndrome': ['diabetes', 'metabolic', 'insulin', 'obesity'],
    'Cancer': ['cancer', 'tumor', 'oncology'],
    'Thyroid disorders': ['thyroid'],
    'Infectious disease': ['virus', 'infection', 'bacteria', 'pathogen'],
    'Cardiovascular disease': ['cardiac', 'heart', 'vascular'],
}

script_dir = Path(__file__).resolve().parent
root = script_dir.parent
clean_dir = root / 'Cleaned'
files = sorted(clean_dir.glob('*_cleaned.txt'))
poster_summary = []
motivation_counts = Counter()
category_counts = Counter()
disease_counts = Counter()
for path in files:
    text = path.read_text(encoding='utf-8', errors='ignore')
    motivations = match_terms(text, motivation_terms)
    categories = match_terms(text, category_keywords)
    disease_matches = match_terms(text, diseases)
    poster_summary.append({
        'poster': path.name,
        'motivations': sorted(motivations),
        'categories': sorted(categories),
        'diseases': sorted(disease_matches),
    })
    motivation_counts.update(motivations)
    category_counts.update(categories)
    disease_counts.update(disease_matches)

analysis_dir = script_dir / 'analysis'
analysis_dir.mkdir(exist_ok=True)
with open(analysis_dir / 'poster_summary.json', 'w') as fh:
    json.dump(poster_summary, fh, indent=2)
with open(analysis_dir / 'counts.json', 'w') as fh:
    json.dump({
        'motivations': motivation_counts,
        'categories': category_counts,
        'diseases': disease_counts,
    }, fh, ensure_ascii=False, indent=2)

with open(analysis_dir / 'poster_summary.csv', 'w') as fh:
    fh.write('poster,motivations,categories,diseases\n')
    for entry in poster_summary:
        fh.write(','.join([
            entry['poster'],
            '|'.join(entry['motivations']) or 'none',
            '|'.join(entry['categories']) or 'none',
            '|'.join(entry['diseases']) or 'none',
        ]) + '\n')

print('Saved poster_summary.csv and counts.json inside analysis/')
print(f'{len(poster_summary)} posters processed')
print('Top motivations:', motivation_counts.most_common())
print('Top categories:', category_counts.most_common())
print('Top diseases:', disease_counts.most_common())
