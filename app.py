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

"""
PassMate Pilot Pro v3.0
Main Streamlit App - Part 2 (AI Features)
"""

import streamlit as st

# ---------------------------------------------------
# AI ACTION BUTTONS
# ---------------------------------------------------

st.header("⚡ AI Study Tools")

col1, col2, col3 = st.columns(3)
col4, col5 = st.columns(2)

pdf_text = st.session_state.get("pdf_text", "")

# -----------------------------
# SUMMARY
# -----------------------------
with col1:
    if st.button("📄 Generate Summary"):
        if pdf_text:
            with st.spinner("Generating summary..."):
                st.session_state.summary = engine.get_summary(pdf_text)

                st.session_state.history.append({
                    "time": str(datetime.now()),
                    "task": "summary"
                })
        else:
            st.warning("Upload a PDF first.")

# -----------------------------
# IMPORTANT QUESTIONS
# -----------------------------
with col2:
    if st.button("❓ Important Questions"):
        if pdf_text:
            with st.spinner("Generating questions..."):
                st.session_state.important_questions = engine.get_questions(pdf_text)

                st.session_state.history.append({
                    "time": str(datetime.now()),
                    "task": "questions"
                })
        else:
            st.warning("Upload a PDF first.")

# -----------------------------
# QUIZ
# -----------------------------
with col3:
    if st.button("🧠 Generate Quiz"):
        if pdf_text:
            with st.spinner("Creating quiz..."):
                st.session_state.quiz = engine.get_quiz(pdf_text)

                st.session_state.history.append({
                    "time": str(datetime.now()),
                    "task": "quiz"
                })
        else:
            st.warning("Upload a PDF first.")

# -----------------------------
# FLASHCARDS
# -----------------------------
with col4:
    if st.button("🃏 Flashcards"):
        if pdf_text:
            with st.spinner("Creating flashcards..."):
                st.session_state.flashcards = engine.get_flashcards(pdf_text)

                st.session_state.history.append({
                    "time": str(datetime.now()),
                    "task": "flashcards"
                })
        else:
            st.warning("Upload a PDF first.")

# -----------------------------
# STUDY PLAN
# -----------------------------
with col5:
    if st.button("📅 Study Plan"):
        if pdf_text:
            with st.spinner("Generating study plan..."):
                st.session_state.study_plan = engine.get_study_plan(pdf_text)

                st.session_state.history.append({
                    "time": str(datetime.now()),
                    "task": "study_plan"
                })
        else:
            st.warning("Upload a PDF first.")

# ---------------------------------------------------
# OUTPUT DISPLAY SECTION
# ---------------------------------------------------

st.divider()
st.header("📊 Results")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Summary",
    "Questions",
    "Quiz",
    "Flashcards",
    "Study Plan"
])

with tab1:
    st.write(st.session_state.summary or "No summary generated yet.")

with tab2:
    st.write(st.session_state.important_questions or "No questions generated yet.")

with tab3:
    st.write(st.session_state.quiz or "No quiz generated yet.")

with tab4:
    st.write(st.session_state.flashcards or "No flashcards generated yet.")

with tab5:
    st.write(st.session_state.study_plan or "No study plan generated yet.")

# ---------------------------------------------------
# HISTORY PANEL
# ---------------------------------------------------

st.divider()
st.subheader("🕒 Session History")

if st.session_state.history:
    for item in reversed(st.session_state.history[-10:]):
        st.write(f"• {item['time']} → {item['task']}")
else:
    st.info("No activity yet.")
