"""
PassMate Pilot Pro v3.0
Utility Functions (PDF + Text Processing)
"""

import pdfplumber
import re
from typing import List


# ---------------------------------------------------
# PDF TEXT EXTRACTION
# ---------------------------------------------------

def extract_text_from_pdf(file) -> str:
    """
    Extract text from uploaded PDF file.
    """
    text = ""

    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

    except Exception as e:
        return f"Error reading PDF: {str(e)}"

    return text


# ---------------------------------------------------
# TEXT CLEANING
# ---------------------------------------------------

def clean_text(text: str) -> str:
    """
    Clean extracted PDF text for better AI processing.
    """

    if not text:
        return ""

    # Remove multiple spaces
    text = re.sub(r"\s+", " ", text)

    # Remove weird special characters
    text = re.sub(r"[^\w\s\.,;:()\-\n]", "", text)

    # Strip extra spaces
    return text.strip()


# ---------------------------------------------------
# TEXT CHUNKING
# ---------------------------------------------------

def split_into_chunks(text: str, max_words: int = 800) -> List[str]:
    """
    Split long text into smaller chunks for AI processing.
    """

    words = text.split()
    chunks = []

    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i + max_words])
        chunks.append(chunk)

    return chunks

"""
PassMate Pilot Pro v3.0
Utility Functions (Smart Helpers)
"""

from collections import Counter
import re


# ---------------------------------------------------
# KEYWORD EXTRACTION
# ---------------------------------------------------

def extract_keywords(text: str, top_n: int = 10):
    """
    Extract most common meaningful words from text.
    Used for quick topic insight.
    """

    if not text:
        return []

    # Remove common stopwords (basic set)
    stopwords = {
        "the", "is", "in", "and", "to", "of", "a", "an",
        "for", "on", "with", "this", "that", "it", "as",
        "are", "was", "were", "be", "by", "or", "at"
    }

    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    filtered = [w for w in words if w not in stopwords]

    freq = Counter(filtered)

    return [word for word, _ in freq.most_common(top_n)]


# ---------------------------------------------------
# DIFFICULTY ESTIMATOR
# ---------------------------------------------------

def estimate_difficulty(text: str) -> str:
    """
    Very simple heuristic-based difficulty detection.
    """

    if not text:
        return "Unknown"

    length = len(text.split())
    complex_words = len([
        w for w in text.split()
        if len(w) > 8
    ])

    ratio = complex_words / max(length, 1)

    if ratio > 0.25:
        return "Hard"
    elif ratio > 0.12:
        return "Medium"
    else:
        return "Easy"


# ---------------------------------------------------
# FALLBACK SUMMARY (NO AI)
# ---------------------------------------------------

def fallback_summary(text: str, max_sentences: int = 5) -> str:
    """
    Simple extractive summarizer used if Gemini fails.
    """

    if not text:
        return "No content available."

    sentences = re.split(r"(?<=[.!?])\s+", text)

    # Take first meaningful sentences
    summary = sentences[:max_sentences]

    return "\n".join(summary)

