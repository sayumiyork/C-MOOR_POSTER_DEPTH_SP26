# Technical Summary and Reproducibility

## Purpose
This document captures the computational workflow used to produce the thematic and disease reports requested for the student poster corpus. It explains the software stack, AI model, data sources, and includes the original prompt text for transparency.

## Prompt
"I am part of a team of researchers doing a study on student research posters. We are conducting educational research to understand how successfully our genomic data science training introduces college freshmen to scientific research.  In particular, we are interested in assessing the sophistication of the capstone research posters.  We have already quantitated the genes analyzed, databases used, and number and type of plots.  We're now interested in a thematic analysis of the text.

We have a total of 29 posters which I have extracted text from using OCR. Each text file contains as muc
[truncated]
rently based on the order in which they are analyzed. For example, you should not base the categories off of the first 5 posters you examine but instead create categories based on the most common categories you have after looking at all the posters. Once you are finished with the analysis please
[truncated]
tabolic disorders” would include but not be limited to "diabetes” and “thyroid disorders”).

Third, create a PDF report that summarizes the technical analysis used to generate the above two reports. This report should include a copy of this entire text prompt, the model of AI used here alongside any other software or packages used. Include the version of the AI and any other software. 

All 3 reports should be placed in a new directory within the OCR 1.1 directory that is titled with the format “AI_model#_Prompt2”. Please also place any scripts used during"

## Software Stack
- **AI model:** GPT-5.1 Codex Mini (current Zo session model) used to interpret the request and plan the analysis.
- **Python:** 3.12.1 executed via the system interpreter to run `theme_analysis.py`.
- **Pandoc:** 2.17.1.1 used to generate this PDF report from Markdown.

## Data Sources
- 27 cleaned OCR text files located in `Documents/OCR 1.1/Cleaned/`.
- The `theme_analysis.py` script lives alongside the reports in `Documents/OCR 1.1/AI_model#_Prompt2/` and performs keyword counting across motivations, categories, and diseases.

## Scripts and Outputs
- `theme_analysis.py`: Parses the entire corpus to produce `analysis/poster_summary.json`, `analysis/poster_summary.csv`, and `analysis/counts.json` without incremental biases.
- Report 1: `Report1_Motivations_and_Themes.md` summarizes motivational buckets and thematic counts.
- Report 2: `Report2_Disease_Categories.md` documents the disease mention breakdown.
- Report 3: This technical summary. The final version is exported as `Report3_TechnicalReport.pdf` within this folder for sharing.

## Reproducing the Analysis
1. Run `python theme_analysis.py` from `Documents/OCR 1.1/AI_model#_Prompt2/`.
2. Inspect `analysis/counts.json` for the aggregated frequencies and `analysis/poster_summary.csv` for poster-level tagging.
3. Convert or edit the Markdown summaries as needed; Pandoc can regenerate the PDF version of this technical report.
