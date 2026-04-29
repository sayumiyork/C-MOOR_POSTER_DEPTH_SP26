# Report 3: Technical Analysis — Methods, Tools, and Prompt Documentation


**Analyst:** AI (MiniMax M2.7, via Zo Computer)  

**Date:** 2026-04-28  


---


## 1. Original Research Prompt


> *We are part of a team of researchers doing a study on student research posters. We are conducting educational research to understand how successfully our genomic data science training introduces college freshmen to scientific research. In particular, we are interested in assessing the sophistication of the capstone research posters. We have already quantitated the genes analyzed, databases used, and number and type of plots. We're now interested in a thematic analysis of the text.*


> *We have a total of 29 posters which I have extracted text from using OCR... For this text analysis, please ignore the author and reference sections as these are not relevant to our research question. I have included only the 27 high quality posters in these folders.*


> *Please conduct a thematic analysis of the raw text files. Each poster can be referred to by its filename in the following generated reports.*


> *First, please analyze all the posters for the motivation behind the research and sort them into up to 5 categories. You may choose the categories... Please also include a 6th 'Other' category... Please only assign one category per poster. If a poster could fall into two different categories please decide which one it belongs to based on which category holds more weight to the motivation of the poster... The report should include 1) A table with the total count of posters included in each category, a list of posters included in each category, a short and easy to understand explanation of what each category means... 2) For each poster please create a bullet-point list of text from the poster that supports assigning it to the category you chose... If the poster is in the other category please detail what category it would have been placed in if you were allowed more categories...*


> *Second... we would like to know what human diseases are included in the text of each poster... Create a PDF report that includes 1) A table relating the poster to any human diseases that were listed in the text. Please also include posters that did not list human diseases. 2) A broader analysis that shows that percent of posters in total mentioned broader categories of disease states.*


> *Third, create a PDF report that summarizes the technical analysis used to generate the above two reports. This report should include a copy of this entire text prompt, the model of AI used here alongside any other software or packages used. Include the version of the AI and any other software.*


> *All 3 reports should be placed in a new directory within the OCR 1.1 directory that is titled with the format 'AI_model#_Prompt2'. Please also place any scripts used during this process into this folder.*


## 2. AI Model and Version


| Component | Version / Details |

|---|---|

| AI Model | MiniMax M2.7 (Zo Computer) |

| Underlying LLM | MiniMax text-generation model (vercel:minimax/minimax-m2.7) |

| Session Context | 27 raw OCR text files read into context |

| Analysis Date | 2026-04-28 |


## 3. Software and Toolchain


| Tool | Version | Purpose |

|---|---|---|

| Python | 3.12 | Core scripting and analysis |

| pandoc | 2.17.1.1 | Markdown to PDF conversion |

| TeX Live | 2023 Debian package | LaTeX engine for pandoc |

| Operating System | Debian GNU/Linux 12 (bookworm) | Execution environment |

| Zo Computer | Current | AI orchestration platform |


## 4. Analysis Pipeline


**Step 1 — Data Loading**  
All 27 raw OCR text files were read from `/home/workspace/Documents/OCR 1.1/Raw/`. Authors and References sections were stripped before analysis.


**Step 2 — Keyword-Based Thematic Scoring with Strong-Pattern Override**  
Each poster's text was searched against keyword lists for five motivation categories. A separate set of 'strong disease-framing patterns' (e.g., named diseases like 'Zellweger' or 'KRAS') acts as an override: if any strong pattern matches, that category wins regardless of keyword count. This ensures posters explicitly modeling a named disease are correctly classified.


**Step 3 — Tie-Breaking Rule**  
When multiple non-strong categories have equal keyword scores, a predefined priority order (Neurological > Cancer > Inherited > Metabolic > Basic Biology > Other) is applied to deterministically assign exactly one category per poster.


**Step 4 — Disease Extraction**  
Keyword pattern matching across all poster texts identified human disease mentions. Authors and References sections were excluded.


**Step 5 — Report Generation**  
Three Python scripts generated Markdown reports, converted to PDF via pandoc + pdflatex.


## 5. Category Assignment Reproducibility


- **Basic Biology**: Research focused on understanding fundamental biological mechanisms — such as gene expression patterns, regional tissue specialization, signaling pathways, or developmental processes — without explici...

- **Neurological & Psychiatric Disease**: Research motivated by understanding the molecular basis of brain or nervous system disorders. These posters investigate genes and pathways linked to cognitive, behavioral, or neuropsychiatric conditio...

- **Cancer**: Research motivated by understanding cancer biology, specifically oncogenes, tumor suppressor genes, cell cycle regulation, or cancer-related pathways. These posters frame the work around uncontrolled ...

- **Metabolic & Digestive Disease**: Research motivated by understanding metabolic or digestive disorders, including conditions affecting the liver, gut, or nutrient processing. These posters focus on pathways such as carbohydrate metabo...

- **Inherited / Genetic Disorder**: Research motivated by understanding specific inherited or rare genetic disorders. These posters explicitly name and characterize a clinical genetic condition and use the model organism to understand i...

- **Other**: Research that does not fit into any of the five primary categories. This may include posters focused purely on applied biotechnology method validation, insect physiology without disease framing, or to...


**Tie-breaking rule**: Predefined priority order applied when scores are tied.
