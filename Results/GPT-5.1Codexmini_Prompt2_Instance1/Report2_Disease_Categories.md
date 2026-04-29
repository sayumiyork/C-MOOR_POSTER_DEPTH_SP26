# Poster Disease and Domain Focus

## Summary
- Used keyword matching to flag disease mentions in all 27 cleaned posters (entire corpus scanned before locking categories). Keyword groups were derived from the research prompt (e.g., metabolic disorders, endocrine conditions, infection, cancer, cardiovascular) so that labels correspond to real study topics.
- Each poster could hit multiple disease tags; counts therefore reflect mentions, not unique posters, and two categories (cardiovascular and infectious) appeared less frequently.

## Disease mentions
| Disease grouping | Poster mentions |
| --- | --- |
| Diabetes / metabolic syndrome | 13 |
| Cancer | 6 |
| Infectious disease | 4 |
| Cardiovascular disease | 2 |
| Autism spectrum disorder | 1 |

*Interpretation:* Metabolic conditions dominate the dataset (half the series mention diabetes or related metabolic dysregulation), while autism and cardiovascular disease appear rarely. Cancer and infectious disease have moderate representation, suggesting the training program pushes students toward metabolism-first narratives.

## Domain overlap
- Many of the disease-focused posters also fall under the Neurological / Metabolic thematic categories (Report 1), which reflects the dual focus on human disease relevance and fly midgut biology.
- The counts help orient future training: e.g., additional modules on cardiovascular biology or infection could balance the current metabolic-heavy emphasis.

## Next steps
1. Use the `poster_summary.csv` to map disease counts back to genes/databases already extracted.
2. Consider manual review of the 13 diabetes/metabolic posters to check for subthemes (obesity vs. lipid metabolism) and refine the keyword taxonomy.
