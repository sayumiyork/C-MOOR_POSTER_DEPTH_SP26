# Getting Started — Poster Panel OCR Tool

**A step-by-step guide for new users**

---

## What Is This Tool?

The Poster Panel OCR Tool extracts text from research posters. Unlike a simple screenshot OCR, this tool lets you define sections by drawing panels around areas, so the text stays organized by topic.

**Key benefit:** Text from different sections (Introduction, Methods, Results, etc.) stays separate instead of getting jumbled together.

---

## Quick Start (5 Minutes)

### Step 1: Open the Tool

1. Navigate to the folder: `Documents/C-MOOR Poster OCR - Instance 2/`
2. Open the file `poster_panel_define_ocr.html` by double-clicking it
3. The tool opens in your default web browser

> **Note:** If you see a blank white screen, try refreshing the page or using a different browser (Chrome, Firefox, Edge recommended).

### Step 2: Upload Your Poster

1. Click **📤 Upload** button in the top toolbar, OR
2. Drag and drop your poster image directly onto the upload area

**Supported formats:** JPG, PNG, WebP, GIF

### Step 3: Zoom and Navigate

| Action | How |
|--------|-----|
| Zoom in | Click ➕ or drag slider right |
| Zoom out | Click ➖ or drag slider left |
| Pan | Right-click and drag |

### Step 4: Select a Section Type

Before drawing, click one of the colored buttons to select what section you're defining:

| Button | Section | When to Use |
|--------|---------|-------------|
| 🔴 Title | Title | The poster's main title at the top |
| 🟠 Authors | Authors | Author names and affiliations |
| 🟢 Abstract | Abstract | Abstract text (if separate from intro) |
| 🟡 Intro | Introduction | Background, objectives |
| 🟢 Methods | Methods | How the research was done |
| 🔵 Results | Results | Data, figures, findings |
| 🟣 Discussion | Discussion | Analysis and conclusions |
| ⚪ Refs | References | Citations |
| ⚫ Other | Other | Anything else (acknowledgements, etc.) |

### Step 5: Draw Panels Around Sections

1. Click and hold your mouse on one corner of a text area
2. Drag to the opposite corner
3. Release — a colored rectangle appears

**Tips:**
- Draw tightly around the text, excluding headers/footers
- You can draw multiple panels for the same section (e.g., two Introduction panels)
- The panel is automatically labeled with its section type

### Step 6: Run OCR

1. Click **🚀 Run OCR** button
2. Wait for processing (progress shows in status area)
3. Results appear in the sidebar

### Step 7: Review and Download

1. Toggle between **Original** and **Cleaned** tabs to see both versions
2. Click **📥 Original** to download raw OCR text
3. Click **📥 Cleaned** to download corrected text

---

## Understanding the Results

### Original Version
Raw text extracted from your poster. May contain:
- Broken words (e.g., `fer-\nment`)
- OCR errors (e.g., `f` instead of `t`)
- Preserves exact layout and structure

### Cleaned Version
Post-processed text with automatic corrections:
- Words rejoined
- Common OCR errors fixed
- Scientific terms standardized (e.g., `DESeq` → `DESeq2`)

---

## Tips for Best Accuracy

### Do:
- ✅ Use high-resolution poster images
- ✅ Draw panels tightly around text
- ✅ Exclude headers, footers, and logos
- ✅ Keep figures and captions in the same panel
- ✅ Review the Cleaned output before publishing

### Don't:
- ❌ Don't include section headers inside panels
- ❌ Don't overlap panels
- ❌ Don't use blurry or compressed images

---

## Troubleshooting

### "Panel draws far from where I click"
This is a known browser issue. Try:
1. Refresh the page
2. Upload the poster again
3. Make sure you're not zoomed in too far

### "OCR doesn't recognize my poster"
- Ensure the poster is a clear image (not a PDF scan)
- Try a higher resolution version
- Make sure text is readable in the image

### "Wrong text extracted"
- The panel may include unintended areas
- Try redrawing with tighter bounds
- Some very small text may not OCR well

---

## Privacy

**Your posters never leave your computer.** This tool runs entirely in your browser:
- No upload to any server
- No internet connection required after loading
- Your data stays on your device

---

## Keyboard Reference

| Action | Mouse |
|--------|-------|
| Draw panel | Left-click + drag |
| Pan | Right-click + drag |
| Zoom | Ctrl/Cmd + scroll |

---

## Getting Help

If you encounter issues:
1. Refresh the page and try again
2. Try a different browser
3. Ensure your poster image is clear and high-resolution

---

*For more details, see the Feature Guide.*
