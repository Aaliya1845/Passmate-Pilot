"""
PassMate Pilot Pro v3.0
Main Streamlit Application
"""

from __future__ import annotations

import os
import time
from datetime import datetime

import streamlit as st

from ai_engine import GeminiEngine
from utils import (
    extract_text_from_pdf,
    clean_text,
    split_into_chunks,
)

from pdf_report import generate_pdf_report
from config import (
    APP_NAME,
    APP_ICON,
    APP_VERSION,
    MAX_FILE_SIZE_MB,
    DEFAULT_LANGUAGE,
)


# ---------------------------------------------------
# Page Config
# ---------------------------------------------------

st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------
# Session State
# ---------------------------------------------------

DEFAULTS = {
    "summary": "",
    "important_questions": "",
    "quiz": "",
    "flashcards": "",
    "study_plan": "",
    "notes": "",
    "history": [],
    "pdf_text": "",
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------------------------------------------
# Custom CSS
# ---------------------------------------------------

st.markdown(
    """
<style>

.block-container{
padding-top:1rem;
padding-bottom:2rem;
}

.stButton>button{
width:100%;
border-radius:10px;
height:45px;
font-weight:bold;
}

.card{
padding:18px;
border-radius:14px;
background:#f5f5f5;
margin-bottom:10px;
}

</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------
# Title
# ---------------------------------------------------

st.title(f"{APP_ICON} {APP_NAME}")

st.caption(f"Version {APP_VERSION}")

st.write(
"""
AI-powered exam preparation assistant using Gemini AI.
Upload notes and instantly generate:

• Smart Summary

• Important Questions

• Quiz

• Flashcards

• Study Plan

• PDF Report
"""
)

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

with st.sidebar:

    st.header("Settings")

    language = st.selectbox(
        "Output Language",
        [
            "English",
            "Hindi",
            "Marathi",
        ],
        index=0,
    )

    temperature = st.slider(
        "AI Creativity",
        0.0,
        1.0,
        0.3,
        0.1,
    )

    max_tokens = st.slider(
        "Maximum Tokens",
        512,
        4096,
        2048,
    )

    st.divider()

    st.subheader("Upload Notes")

    uploaded_file = st.file_uploader(
        "Choose PDF",
        type=["pdf"],
    )

    st.caption(
        f"Maximum recommended size: {MAX_FILE_SIZE_MB} MB"
    )

    st.divider()

    clear = st.button("🗑 Clear Session")

    if clear:

        for key in DEFAULTS:
            st.session_state[key] = DEFAULTS[key]

        st.success("Session Cleared")

        st.rerun()

# ---------------------------------------------------
# Gemini
# ---------------------------------------------------

engine = GeminiEngine(
    language=language,
    temperature=temperature,
    max_tokens=max_tokens,
)

# ---------------------------------------------------
# PDF Processing
# ---------------------------------------------------

if uploaded_file is not None:

    with st.spinner("Reading PDF..."):

        raw_text = extract_text_from_pdf(uploaded_file)

        raw_text = clean_text(raw_text)

        st.session_state.pdf_text = raw_text

    st.success("PDF Loaded Successfully")

    st.text_area(
        "Preview",
        raw_text[:3000],
        height=250,
    )

else:

    st.info("Upload your notes PDF from the sidebar.")
