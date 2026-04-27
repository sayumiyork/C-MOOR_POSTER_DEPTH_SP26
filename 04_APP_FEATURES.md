# Poster Panel OCR Tool — Feature Guide

**Version 1.0 | C-MOOR Research Project**

---

## Overview

The Poster Panel OCR Tool is a browser-based application designed for extracting text from scientific research posters using Optical Character Recognition (OCR). It runs entirely in your browser with no server required — your posters never leave your computer.

## Core Features

### 1. Panel-Based OCR
Instead of OCR-ing an entire poster (which produces messy, mixed-up text), you draw rectangles ("panels") around each section. The tool then OCR's each panel separately, preserving the logical structure of the poster.

**Supported Sections:**

| Section | Color | Use For |
|---------|-------|---------|
| Title | 🔴 Red | Poster title at top |
| Authors | 🟠 Orange | Author names and affiliations |
| Abstract | 🟢 Teal | Abstract text |
| Introduction | 🟡 Yellow | Background, objectives |
| Methods | 🟢 Green | Methodology |
| Results | 🔵 Blue | Findings, data |
| Discussion | 🟣 Purple | Analysis, conclusions |
| References | ⬛ Gray | Citations |
| Other | ⚫ Pink | Acknowledgements, appendices |

### 2. Visual Panel Editor

**Drawing Panels:**
- Select a section type from the color-coded buttons
- Click and drag on the poster image to draw a panel
- Panels are numbered and color-coded by section type
- Use Undo to remove the last panel, or Clear to remove all

**Panel Management:**
- Click any panel's dropdown to change its section type
- Click ✕ to remove individual panels
- Panel list shows all drawn panels with their types

### 3. Zoom and Pan Controls

**Zoom:**
- Use ➕/➖ buttons in the header
- Drag the zoom slider
- Ctrl+scroll (or Cmd+scroll on Mac) also works

**Pan:**
- Middle-mouse button drag to pan around the poster
- Right-click drag also works

### 4. Dual Output Versions

After running OCR, you get **two versions**:

| Version | Description | Download Button |
|---------|-------------|----------------|
| **Original** | Raw OCR output with structure preserved | 📥 Original |
| **Cleaned** | Post-processed with fixes applied | 📥 Cleaned |

### 5. Integrated Cleanup Script

The **Cleaned** version applies automatic corrections:

| Fix Type | Example |
|----------|---------|
| Word splits | `fer-\nment` → `ferment` |
| Common OCR errors | `confrol` → `control` |
| Gene name formatting | `DESeq` → `DESeq2` |
| f→t substitutions | `communicafion` → `communication` |
| Scientific terms | `Flybase` → `FlyBase` |
| Spell check | Uses symmetric delete algorithm for unknown errors |

### 6. Smart Filename Handling

- Uploaded posters automatically set the output filename
- You can manually edit the filename before downloading
- Cleaned files automatically get `_cleaned` appended

### 7. Offline Operation

- All processing happens in your browser
- Tesseract.js OCR engine runs locally
- No data is sent to any server

---

## Technical Details

### OCR Engine
- **Tesseract.js v5** — Industry-standard OCR running in JavaScript
- Trained on English text
- Processes at 4x resolution for better accuracy

### Spell Checker
- **Symmetric Delete algorithm** — generates corrections by deleting letters
- Embedded dictionary of ~80,000 common English words
- Preserves gene names, technical terms, and unknowns automatically

### Browser Requirements
- Modern browser with JavaScript enabled
- Canvas API support
- FileReader API support

---

## File Formats Supported

| Format | Extension | Status |
|--------|-----------|--------|
| JPEG | .jpg, .jpeg | ✅ Tested |
| PNG | .png | ✅ Tested |
| WebP | .webp | ✅ Supported |
| GIF | .gif | ✅ Supported |

---

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Pan | Middle-click drag |
| Zoom In | Ctrl/Cmd + Scroll Up |
| Zoom Out | Ctrl/Cmd + Scroll Down |

---

## Tips for Best Results

1. **Draw panels tightly** around text areas, excluding headers/footers
2. **Use high-resolution images** when possible
3. **Separate sections** into individual panels for cleaner output
4. **Review the Cleaned version** before using in publications

---

## Privacy

Your posters and OCR results **never leave your computer**. All processing occurs locally in your browser. No data is transmitted to any external server.

---

*Developed for C-MOOR Research Project — April 2026*
