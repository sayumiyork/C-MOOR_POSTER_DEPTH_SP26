# OCR Cleanup Script — Technical Documentation

**What happens during text cleanup**

---

## Overview

The cleanup script is a post-processing step that runs automatically when you download the **Cleaned** version of your OCR output. It fixes common OCR errors and improves readability.

---

## Cleanup Pipeline

The cleanup runs in this order:

```
Raw OCR Text
    ↓
1. Fix Word Splits (line breaks within words)
    ↓
2. Fix Gene Names (scientific naming)
    ↓
3. Fix f→t Substitutions (common OCR error)
    ↓
4. Apply Spell Check (conservative correction)
    ↓
5. Normalize Whitespace
    ↓
Cleaned Text
```

---

## Step 1: Fix Word Splits

**Problem:** OCR sometimes splits words at line breaks, especially in narrow columns.

| Raw OCR | Cleaned |
|---------|---------|
| `fer-\nment` | `ferment` |
| `over-\nview` | `overview` |
| `but-\nterfly` | `butterfly` |

**Method:** Detects hyphen followed by newline and removes both.

---

## Step 2: Fix Gene Names

**Problem:** Inconsistent formatting of scientific names and tools.

| Raw OCR | Cleaned |
|---------|---------|
| `DESeq` | `DESeq2` |
| `ClustrProfiler` | `ClusterProfiler` |
| `Flybase` | `FlyBase` |
| `Drosophila` | `Drosophila` (corrected spelling) |
| `melanogaster` | `melanogaster` (corrected spelling) |

**Method:** Simple find-and-replace dictionary.

---

## Step 3: Fix f→t Substitutions

**Problem:** The letter `f` is commonly misread as `t` (and vice versa) by OCR.

| Raw OCR | Cleaned |
|---------|---------|
| `confrol` | `control` |
| `communicafion` | `communication` |
| `frend` | `trend` |
| `funcion` | `function` |
| `refulation` | `regulation` |

**Method:** Replaces common `f`→`t` error patterns found in scientific text.

---

## Step 4: Spell Check (Symmetric Delete Algorithm)

**Problem:** Unknown OCR errors that aren't in our specific fix list.

**Solution:** Conservative spell checker that:
1. Generates possible corrections by deleting letters (symmetric delete)
2. Compares against a dictionary of ~80,000 common English words
3. Only corrects if exactly ONE match is found
4. Leaves gene names and unknowns untouched

**Why it's safe:**
- Gene names like `Acox3`, `KCNQ3`, `FBgn0039349` generate no dictionary matches → **preserved**
- `communicafion` generates one match (`communication`) → **corrected**
- `xyzabc` generates no matches → **preserved as-is**

---

## Step 5: Normalize Whitespace

**Problem:** Extra spaces, tabs, or irregular line breaks.

| Raw OCR | Cleaned |
|---------|---------|
| `word  multiple spaces` | `word multiple spaces` |
| `line1\n\n\n\nline2` | `line1\n\nline2` |
| `  leading spaces` | `leading spaces` |

---

## Additional Fixes

### Bar and Pipe Characters

| Raw OCR | Cleaned |
|---------|---------|
| `\|` (pipe) | `I` (capital i) |
| `midgut\|` | `midgut` |

### Scientific Formatting

| Raw OCR | Cleaned |
|---------|---------|
| `H~2~O` | `H2O` |
| `\u` (unicode) | cleaned |

---

## What Is NOT Changed

The cleanup is conservative. These are intentionally preserved:

| Type | Example | Reason |
|------|---------|--------|
| Gene names | `Acox3`, `KCNQ3` | Preserved exactly |
| FlyBase IDs | `FBgn0039349` | Preserved exactly |
| Unknown terms | `LFCFe` | No dictionary match |
| P-values | `p < 0.05` | Already correct format |
| URLs | `https://doi.org/...` | Preserved exactly |
| Reference numbers | `[1]`, `(2)` | Preserved exactly |

---

## Section Structure Preservation

The cleanup **does not** modify:
- Section headers (`SECTION: INTRODUCTION`)
- Line separators (`======`)
- References section formatting

The References section is kept as-is to preserve citation structure.

---

## Technical Details

### Embedded Dictionary
- ~80,000 common English words
- Includes scientific terms (biology, chemistry)
- Excludes gene names (they don't match)

### Algorithm: Symmetric Delete
```
For word "confrol":
1. Generate deletes: "onfol", "cnfol", "cofol", "conf", etc.
2. Check each against dictionary
3. If exactly 1 match found → correct
4. Otherwise → leave as-is
```

### Processing Time
- Typically < 1 second for entire poster
- Runs entirely in browser
- No server required

---

## Comparison Example

### Raw OCR:
```
The Gut-microbiome-brain axis (GUMBA) refers fo the
body communicafion between the gut and the brain and how they
work in tandem to uphold homeostasis. This connection has
linked disorders such as Aufism (ASD) to genes expressed within the
midgut.
```

### After Cleanup:
```
The Gut-microbiome-brain axis (GUMBA) refers to the
body communication between the gut and the brain and how they
work in tandem to uphold homeostasis. This connection has
linked disorders such as Autism (ASD) to genes expressed within the
midgut.
```

**Fixes applied:**
- `fo` → `to` (spell check)
- `communicafion` → `communication` (f→t fix)
- `Aufism` → `Autism` (spell check)

---

## Limitations

1. **Cannot fix unseen errors** — If an error generates multiple dictionary matches, it won't be corrected
2. **Gene name variations** — Only standardized gene names in our dictionary are corrected
3. **Context-dependent errors** — `their` vs `there` cannot be distinguished without context
4. **Handwriting** — Not designed for handwritten text

---

## Future Improvements

Potential additions:
- [ ] Larger scientific dictionary
- [ ] Context-aware corrections
- [ ] Custom gene name list
- [ ] Multi-language support

---

*Part of the Poster Panel OCR Tool — C-MOOR Research Project*
