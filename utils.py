"""
PassMate Pilot Pro v3.0
Utility Functions (Clean Fixed Version)
"""

import pdfplumber
import re
from typing import List
from collections import Counter


# -----------------------------
# PDF EXTRACTION
# -----------------------------
def extract_text_from_pdf(file) -> str:
    text = ""

    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        return f"PDF Error: {str(e)}"

    return text


# -----------------------------
# CLEAN TEXT
# -----------------------------
def clean_text(text: str) -> str:
    if not text:
        return ""

    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s\.,;:()\-\n]", "", text)

    return text.strip()


# -----------------------------
# SPLIT TEXT
# -----------------------------
def split_into_chunks(text: str, max_words: int = 800) -> List[str]:
    words = text.split()
    chunks = []

    for i in range(0, len(words), max_words):
        chunks.append(" ".join(words[i:i + max_words]))

    return chunks
