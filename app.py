"""
PassMate Pilot Pro v3.0
Main Streamlit App (FINAL VERSION)
"""

import streamlit as st
from datetime import datetime

from ai_engine import GeminiEngine
from utils import extract_text_from_pdf, clean_text

from config import APP_NAME, APP_ICON, APP_VERSION


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide"
)


# ---------------------------------------------------
# DARK BROWN + BLACK THEME
# ---------------------------------------------------
st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(135deg, #0b0b0b, #1a0f0a, #2b1a12);
        color: #f5f5f5;
    }

    section[data-testid="stSidebar"] {
        background-color: #120b08;
    }

    .stButton>button {
        background-color: #3b1f14;
        color: white;
        border-radius: 10px;
        border: 1px solid #5a2d1f;
        width: 100%;
        height: 45px;
        font-weight: bold;
    }

    .stButton>button:hover {
        background-color: #5a2d1f;
    }

    textarea {
        background-color: #120b08 !important;
        color: #f5f5f5 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.title(f"{APP_ICON} {APP_NAME}")
st.caption(f"Version {APP_VERSION}")


# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

if "history" not in st.session_state:
    st.session_state.history = []


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
with st.sidebar:
    st.header("⚙ Settings")

    language = st.selectbox("Language", ["English", "Hindi", "Marathi"])
    temperature = st.slider("Creativity", 0.0, 1.0, 0.3)

    st.divider()

    uploaded_files = st.file_uploader(
        "Upload PDF files (1–10 allowed)",
        type=["pdf"],
        accept_multiple_files=True
    )

    st.divider()

    if st.button("🗑 Clear Session"):
        st.session_state.pdf_text = ""
        st.session_state.history = []
        st.success("Cleared!")


# ---------------------------------------------------
# INIT AI ENGINE
# ---------------------------------------------------
engine = GeminiEngine(
    language=language,
    temperature=temperature,
    max_tokens=2048
)


# ---------------------------------------------------
# MULTI PDF PROCESSING
# ---------------------------------------------------
if uploaded_files:

    all_text = ""

    for file in uploaded_files:
        with st.spinner(f"Reading {file.name}..."):
            text = extract_text_from_pdf(file)
            text = clean_text(text)
            all_text += "\n" + text

    st.session_state.pdf_text = all_text

    st.success(f"{len(uploaded_files)} PDF(s) loaded successfully!")

    st.text_area("Preview", all_text[:3000], height=250)

else:
    st.info("Upload 1–10 PDF files to start.")


# ---------------------------------------------------
# AI FEATURES
# ---------------------------------------------------
st.divider()
st.header("⚡ AI Tools")

col1, col2, col3 = st.columns(3)
col4, col5 = st.columns(2)

pdf_text = st.session_state.pdf_text


# Summary
with col1:
    if st.button("📄 Summary"):
        if pdf_text:
            st.session_state.summary = engine.get_summary(pdf_text)
            st.session_state.history.append("Summary")

# Questions
with col2:
    if st.button("❓ Questions"):
        if pdf_text:
            st.session_state.questions = engine.get_questions(pdf_text)
            st.session_state.history.append("Questions")

# Quiz
with col3:
    if st.button("🧠 Quiz"):
        if pdf_text:
            st.session_state.quiz = engine.get_quiz(pdf_text)
            st.session_state.history.append("Quiz")

# Flashcards
with col4:
    if st.button("🃏 Flashcards"):
        if pdf_text:
            st.session_state.flashcards = engine.get_flashcards(pdf_text)
            st.session_state.history.append("Flashcards")

# Study Plan
with col5:
    if st.button("📅 Study Plan"):
        if pdf_text:
            st.session_state.study_plan = engine.get_study_plan(pdf_text)
            st.session_state.history.append("Study Plan")


# ---------------------------------------------------
# OUTPUT
# ---------------------------------------------------
st.divider()
st.header("📊 Results")

st.subheader("Summary")
st.write(st.session_state.get("summary", ""))

st.subheader("Questions")
st.write(st.session_state.get("questions", ""))

st.subheader("Quiz")
st.write(st.session_state.get("quiz", ""))

st.subheader("Flashcards")
st.write(st.session_state.get("flashcards", ""))

st.subheader("Study Plan")
st.write(st.session_state.get("study_plan", ""))


# ---------------------------------------------------
# HISTORY
# ---------------------------------------------------
st.divider()
st.subheader("🕒 History")

st.write(st.session_state.history if st.session_state.history else "No activity yet.")
