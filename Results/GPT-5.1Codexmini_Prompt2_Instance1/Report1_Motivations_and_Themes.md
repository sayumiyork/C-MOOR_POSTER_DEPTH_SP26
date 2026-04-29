# Poster Motivation and Thematic Categories

## Dataset
- 27 OCR-cleaned posters stored in `Documents/OCR 1.1/Cleaned`.
- Text parsed programmatically via `theme_analysis.py` to extract category keywords across the full corpus (no incremental bias).

## Method
1. Keywords mapped to five motivation buckets (e.g., Disease mechanism, Human health application, Technology demonstration, Model organism validation, Environmental/Population context), ensuring each poster could contribute to multiple motivations.
2. Another set of domain-specific keywords produced five broad thematic categories (Neurological / Neurodevelopmental, Metabolic / Endocrine, Cancer / Growth control, Infectious / Immune, Cardiovascular / Circulatory).
3. All posters were scanned before finalizing categories so counts reflect the entire corpus.

## Findings
| Theme | Count of posters citing the theme |
| --- | --- |
| Model organism validation | 27 |
| Technology demonstration | 26 |
| Disease mechanism | 26 |
| Human health application | 25 |
| Environmental/Population context | 6 |

| Clinical domain | Poster count |
| --- | --- |
| Neurological / Neurodevelopmental | 18 |
| Metabolic / Endocrine | 15 |
| Infectious / Immune | 9 |
| Cancer / Growth control | 7 |
| Cardiovascular / Circulatory | 5 |

*Interpretation:* Every project referenced the value of Drosophila as a model organism and framed work as both a technology demonstration and disease investigation. Neurological/neurodevelopmental and metabolic topics dominate, with fewer posters focusing on cardiovascular or cancer topics.

## Notes
- Each poster was tagged with every keyword it matched, so counts total more than 27 when posters touched multiple themes.
- Next steps could include refining keywords (e.g., splitting metabolic into endocrine vs. digestive) and linking to the genes/databases already cataloged.
