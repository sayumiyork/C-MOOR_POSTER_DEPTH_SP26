# 🧒 What Are These Programs Doing? (ELI5 Version)

*Imagine explaining to a 5-year-old what these computer programs do with pictures of posters...*

---

## The Big Picture

You know how you have a coloring book with pictures, and you can color in the spaces with your crayons? 

This is like that, but with scientific posters (big papers with lots of words and pictures that scientists put on walls) and a computer program instead of crayons.

---

## What's Happening Step By Step

### 1. First, We Need a Picture of the Poster

The computer can't see a poster hanging on a wall like you can. So we have to take a picture of it and put it into the computer. That's what the "upload" button does.

```
Real Poster → Take Picture → Put on Computer Screen
```

---

### 2. We Draw Little Boxes on the Picture

The poster has different parts - like a title at the top, names of the scientists, and big sections about what they did and what they found.

We use the computer mouse to draw little boxes (called "panels") around each part we want:

```
┌─────────────────────────┐
│  Title of the Study     │  ← Draw box around this
├─────────────────────────┤
│  Scientists' Names       │  ← Draw box around this
├─────────────────────────┤
│  Introduction...         │  ← Draw box around this
│  (why they did it)      │
├─────────────────────────┤
│  Methods...              │  ← Draw box around this
│  (how they did it)      │
├─────────────────────────┤
│  Results...             │  ← Draw box around this
│  (what they found)      │
├─────────────────────────┤
│  Discussion...           │  ← Draw box around this
│  (what it means)        │
└─────────────────────────┘
```

We color-code the boxes so we know what's inside:
- 🔴 Red box = Title
- 🟠 Orange box = Authors (scientist names)
- 🟡 Yellow box = Introduction
- 🟢 Green box = Methods
- 🔵 Blue box = Results
- 🟣 Purple box = Discussion

---

### 3. The Computer Reads the Words (OCR)

OCR stands for "Optical Character Recognition." That's a fancy way of saying "the computer reading the words from the picture."

Think of it like this: when you see the letter "A", your brain knows it's an "A" because you've seen it a million times. The computer is learning to do the same thing - looking at the picture of a letter and figuring out which letter it is.

But the computer needs help:
- The picture of the poster is sometimes blurry
- Letters can look squished together or stretched out
- Some letters look like other letters (like "l" and "I" and "1")

So we make the picture 4 times bigger (zoomed in) before the computer tries to read the letters. This is like giving the computer a magnifying glass!

---

### 4. The Computer Puts the Words Together

When the computer reads each letter, it puts them together to make words, sentences, and paragraphs.

But sometimes it makes mistakes:
- It might think a blurry spot is a letter
- It might miss a letter that's faded
- It might join two words together or split one word in half

That's why we get two versions:
- **Original**: What the computer "heard" (with all its mistakes)
- **Cleaned**: What it should say (after we fixed the obvious mistakes)

---

### 5. We Tell the Computer Which Fixes to Make

The cleanup script is like having a teacher correct your spelling homework:

| Computer heard | Should be |
|----------------|-----------|
| "DESeq?" | "DESeq2" |
| "ClustrProfiler" | "ClusterProfiler" |
| "fatty\|acid" | "fatty acid" |
| "midgut" | "midgut" |
| (extra spaces) | (single space) |

The computer learned these rules from looking at lots of examples.

---

### 6. We Save the Words to a File

Finally, we can save the words to a special text file that we can read later or put into other programs.

---

## What Each File Does

### `poster_panel_define_ocr.html`
This is the MAIN tool. Think of it like a special art program where you can:
- Open a poster picture (like opening a coloring page)
- Draw boxes around things (like tracing with a crayon)
- Tell the computer what each box is for (like labeling your tracing)
- Make the computer read the words inside each box
- Get two versions of the words - one with mistakes and one fixed

### `poster_ocr_script.py` and `ocr_cleanup.py`
These are older programs that work differently. They're like teaching the computer to color without you being able to see what it's doing. The HTML tool is better because you can see everything and fix mistakes.

---

## Why Is This Hard?

You might think: "Why can't the computer just read the whole poster at once?"

Here's why it's tricky:

### Problem 1: Posters Have Different Layouts
Some posters have 2 columns, some have 3. Some have the title at the very top, some have it in the middle. The computer has to figure out WHERE things are.

### Problem 2: The Computer Can't "Understand" Yet
The computer can recognize letters and words, but it doesn't really know what they mean. It doesn't know that "Introduction" is supposed to come before "Methods" or that references go at the end. That's why WE have to draw the boxes and tell it what each section is.

### Problem 3: Text in Pictures is Messy
Real-world text (like on a poster) has:
- Shadows and highlights
- Colors behind letters
- Lines and borders
- Different fonts mixed together

It's much harder for a computer to read than clean text on a white page.

---

## What Would Make It Easier?

If EVERY poster used the SAME layout with the SAME colors in the SAME positions, we could teach the computer to read them automatically. But scientists are creative! They like to design their posters differently.

So for now, we have to help the computer by:
1. Drawing boxes around each section
2. Telling it what type of section each box is
3. Fixing the mistakes it makes when reading

---

## The Funny Parts

Sometimes the computer makes REALLY silly mistakes:

| Poster actually said | Computer read it as |
|----------------------|---------------------|
| "DESeq2" | "DESeq?" or "OESeq2" |
| "ClusterProfiler" | "ClustrProfiler" |
| "midgut" | "\|midgut" or "rnidgut" |
| "Acox3" | "Acox3" (sometimes this one works!) |

The cleanup script fixes these funny mistakes.

---

## Summary (In One Sentence)

**We take pictures of scientific posters, draw boxes around different parts, teach the computer to read the words inside each box, fix the reading mistakes, and save the words to a file we can use later.**

---

*ELI5 Guide generated: 2026-04-24*