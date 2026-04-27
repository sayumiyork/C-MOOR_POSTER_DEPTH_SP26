# Conversation Summary: C-MOOR Poster OCR Tool Development

**Date**: 2026-04-24  
**User**: Researcher extracting text from student research posters  
**Goal**: Create a tool to extract text from scientific research poster images using OCR

---

## 1. Initial Request and Context

The user is a researcher working with the C-MOOR (Center for Mobile Cognition Research) project at Lesley University. They needed to extract text from student research posters to analyze educational content. The posters follow a scientific research poster format with sections: Introduction, Methods, Results, and Discussion (IMRD).

### Data Location
- **Source posters**: `/home/workspace/Images/C-MOOR SP26 Poster OER Analysis/`
- **Output folder**: `/home/workspace/Documents/C-MOOR Poster OCR - Instance 2/`
- **Posters processed**: Otala, Camara, Avetisyan, Gill, Diaz (5 total)

---

## 2. Development Journey

### Phase 1: Initial OCR Scripts (Versions 1-6)
- Started with basic tesseract OCR on full poster images
- Problem: OCR captured everything including headers, footers, acknowledgments, references
- Added section detection using keyword classifiers (Introduction, Methods, Results, Discussion)
- Problem: Keywords appeared in multiple contexts, causing misclassification
- Attempted to use visual layout analysis (column detection, horizontal bands) to identify sections
- Problem: Different poster layouts (LU vs CCC) had different structures, making automatic detection unreliable

### Phase 2: Interactive Tool (Option C)
After evaluating four approaches, the user chose **Option C**: Interactive panel definition with web-based tool.

**Key Features Implemented**:
1. Visual panel drawing with color-coded sections
2. Zoom and pan controls for large posters
3. Multiple section types: Title, Authors, Introduction, Methods, Results, Discussion, Abstract, References, Other
4. 4x upscaling for better OCR accuracy
5. Automatic and manual cleanup of OCR text
6. Original vs. Cleaned text comparison
7. Download functionality for both versions

### Phase 3: Bug Fixes and Refinements (Ongoing)
Multiple iterations addressed:
- Upload button responsiveness
- Panel offset issues during drawing
- Zoom and pan functionality conflicts
- Layout reorganization (poster on top, controls below)
- Viewing port sizing and containment
- File naming from poster filename
- Cleanup script preserving section headers

---

## 3. Current State (As of Last Session)

### Files Created
| File | Purpose |
|------|---------|
| `poster_panel_define_ocr.html` | Main interactive HTML tool |
| `poster_config_create.py` | Optional Python script for panel config generation |
| `poster_ocr_script.py` | Earlier standalone OCR script |
| `ocr_cleanup.py` | Standalone cleanup script |

### Known Issues (Unresolved)
1. **File naming**: Downloads still use "output.txt" instead of extracting poster filename
2. **Cleanup script**: Still modifying header lines when it shouldn't
3. **Zoom controls**: Periodically become unresponsive after interactions
4. **Upload functionality**: Sometimes fails to trigger on some browsers

### Unfinished Features
1. Tesseract worker initialization check (may cause delays on first OCR)
2. Better handling of multi-column poster layouts
3. Panel reordering functionality
4. Config file save/load for consistent panel definitions across similar posters

---

## 4. User Feedback Summary

### What Worked Well
- Interactive panel drawing concept
- Color-coded section visualization
- Zoom and pan for large posters
- Original vs. Cleaned text comparison
- Sidebar panel list for tracking drawn sections

### What Needed Fixing
- Upload mechanism repeatedly broke during development
- Zoom/pan conflicting with panel drawing
- Layout changes sometimes reverted
- Cleanup script behavior confusing

### User Preferences
- Prefer poster image area on TOP, controls below
- Want automatic filename extraction from uploaded poster
- Want cleanup to only modify content lines, not headers
- Want 9 section types including Title, Authors, Abstract, References

---

## 5. Technical Decisions Made

| Decision | Rationale |
|----------|-----------|
| Browser-based (HTML/JS) instead of Python | Easier distribution, no installation needed |
| Tesseract.js for OCR | Runs entirely in browser, no server needed |
| Color-coded panels | Visual distinction helps user track sections |
| 4x image upscaling before OCR | Improves text recognition accuracy |
| Client-side cleanup | No server round-trip needed |
| Normalize section order in output | Ensures consistent format across posters |

---

## 6. Path Forward (For Future Sessions)

1. **Fix remaining bugs**: File naming, cleanup behavior, zoom/pan stability
2. **Add config save/load**: Allow saving panel definitions as JSON for reuse
3. **Batch processing**: Process multiple posters with same panel configuration
4. **Improve cleanup script**: Better handling of scientific terminology (gene names, etc.)
5. **Add panel edit**: Allow adjusting panel boundaries after drawing
6. **Keyboard shortcuts**: Power users prefer keyboard over mouse

---

*Report generated: 2026-04-24*