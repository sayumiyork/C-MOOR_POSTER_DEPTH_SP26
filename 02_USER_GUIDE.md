# User Guide: Poster Panel OCR Tool

**For totally new users** — how to run the HTML tool on your local system.

---

## What Is This Tool?

The Poster Panel OCR Tool is a web-based application that lets you:
1. Upload an image of a scientific research poster
2. Draw boxes (panels) around different sections of the poster
3. Automatically extract text from each panel using OCR
4. Download the extracted text in two versions: Original (raw) and Cleaned (fixed)

**No installation required** — it runs in your web browser!

---

## Prerequisites

- A modern web browser (Chrome, Firefox, Edge, or Safari)
- An image file of your poster (JPG, PNG, or similar format)
- Internet connection (to load the OCR library from CDN)

---

## How to Get Started

### Step 1: Open the HTML File

1. Navigate to the folder: `Documents/C-MOOR Poster OCR - Instance 2/`
2. Find the file named: `poster_panel_define_ocr.html`
3. **Double-click** the file to open it in your web browser

> **Tip**: If double-clicking doesn't work, right-click the file and choose "Open with" → your browser name.

---

## Interface Overview

```
┌─────────────────────────────────────────────────────────┐
│ 📄 Poster Panel OCR                    ➖ [slider] ➕ 100%│
├─────────────────────────────────────────────────────────┤
│ [📤 Upload] [Title] [Authors] [Intro] [Methods]... ↩️ 🗑️ │
│                                    [output.txt] [🚀 Run]│
├─────────────────────────────────────────────────────────┤
│                                                         │
│              POSTER IMAGE AREA                          │
│         (drag & drop or click to upload)                │
│                                                         │
│    ┌─────────────────────┐                              │
│    │   Your poster will  │                              │
│    │   appear here after │                              │
│    │   uploading         │                              │
│    └─────────────────────┘                              │
│                                                         │
├─────────────────────────────────────────────────────────┤
│ 📋 Panels (0)    │ 📄 Results                           │
│ ┌──────────────┐ │ [Original] [Cleaned]                  │
│ │ No panels... │ │ ┌─────────────────────────────────┐   │
│ └──────────────┘ │ │ Run OCR to see results...      │   │
│ [↩️ Undo] [🗑️]   │ │                                 │   │
│                  │ └─────────────────────────────────┘   │
│                  │ [📥 Original] [📥 Cleaned]            │
└─────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Instructions

### 1. Upload Your Poster

**Option A**: Click the "📤 Upload" button in the top controls bar
**Option B**: Click anywhere in the upload area (dashed border zone)
**Option C**: Drag and drop your poster image file onto the upload area

The poster will automatically scale to fit the viewing area.

---

### 2. Navigate the Poster

| Action | How |
|--------|-----|
| **Zoom In** | Click ➕ button or drag zoom slider right |
| **Zoom Out** | Click ➖ button or drag zoom slider left |
| **Pan** | Hold middle mouse button + drag |
| **Fit to screen** | Use zoom slider to adjust |

---

### 3. Draw Panels Around Sections

**Before drawing**: Select the section type from the buttons:
- **Title** (red) — poster title at top
- **Authors** (orange) — author names and affiliations
- **Introduction** (yellow) — background/objectives
- **Methods** (green) — methodology
- **Results** (blue) — findings
- **Discussion** (purple) — interpretation
- **Abstract** (teal) — summary
- **References** (gray) — citations
- **Other** (pink) — anything else

**To draw a panel**:
1. Click and hold on the poster where you want the corner of the panel
2. Drag to create a box around a section
3. Release to create the panel
4. The panel will appear with a colored border and label

---

### 4. Manage Your Panels

| Action | How |
|--------|-----|
| **Delete a panel** | Click the ✕ button next to it in the panel list |
| **Change section type** | Use the dropdown in the panel list |
| **Undo last panel** | Click "↩️ Undo" button |
| **Clear all panels** | Click "🗑️ Clear" button |

---

### 5. Run OCR

1. Make sure you've drawn at least one panel
2. Click the "🚀 Run OCR" button (green)
3. Wait for processing to complete (progress shown in status area)
4. Results appear in the "Results" section

---

### 6. View and Download Results

**Toggle between versions**:
- Click "Original" to see raw OCR output
- Click "Cleaned" to see text with fixes applied

**Download files**:
- Click "📥 Original" to download raw text
- Click "📥 Cleaned" to download cleaned text

The filename will be based on your poster's name.

---

## Understanding the Cleanup

The "Cleaned" version applies these fixes:

| Issue | Example | Fixed To |
|-------|---------|----------|
| Line breaks in middle of words | "fatty\nacid" | "fattyacid" |
| Pipe characters mistaken for I | "\|" | "I" |
| Backslash errors | "\midgut" | "midgut" |
| DESeq version errors | "DESeq?" | "DESeq2" |
| ClusterProfiler typos | "ClustrProfiler" | "ClusterProfiler" |
| Extra spaces | multiple spaces | single space |

---

## Troubleshooting

### "Upload button doesn't work"
- Try clicking directly on the text "Drop poster image here or click to upload"
- Try dragging a file onto the upload area
- Make sure you're clicking inside the dashed border area

### "Panel draws in wrong position"
- Make sure you're clicking on the canvas (poster image), not the background
- Try zooming in for more precision
- Pan to re-center the poster if needed

### "OCR is taking too long"
- Large posters take longer to process
- Try drawing fewer, larger panels instead of many small ones
- 4x upscaling is intentional for accuracy — don't reduce it

### "Zoom stopped working"
- Refresh the page and start over
- Make sure you're not accidentally in pan mode (middle mouse button)

---

## Keyboard Shortcuts (Optional)

Currently not implemented — future enhancement.

---

## File Locations

| File | Purpose |
|------|---------|
| `poster_panel_define_ocr.html` | Main tool (open this!) |
| `poster_ocr_script.py` | Standalone Python OCR (optional) |
| `ocr_cleanup.py` | Standalone cleanup script (optional) |

---

## Getting Help

If something isn't working:
1. Refresh the page and start over
2. Try a different browser (Chrome recommended)
3. Check that your poster image isn't corrupted
4. Make sure you have internet connectivity (for OCR library)

---

*Guide generated: 2026-04-24*