"""
PassMate Pilot (Ultra UI Version)
Black + Purple + Pink AI SaaS Style
"""

import streamlit as st

from ai_engine import GeminiEngine
from utils import extract_text_from_pdf, clean_text


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="PassMate Pilot",
    page_icon="📘",
    layout="wide"
)


# ---------------------------------------------------
# ULTRA MODERN DARK THEME (BLACK + PURPLE + PINK)
# ---------------------------------------------------
st.markdown(
    """
    <style>

    .stApp {
        background: radial-gradient(circle at top, #07070c, #0a0015, #120018);
        color: #f5e9ff;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b0b10, #1a0025);
    }

    h1, h2, h3 {
        color: #d946ef;
    }

    .stButton>button {
        background: linear-gradient(90deg, #7c3aed, #ec4899);
        color: white;
        border-radius: 12px;
        border: none;
        width: 100%;
        height: 45px;
        font-weight: bold;
        box-shadow: 0px 0px 10px #7c3aed55;
    }

    .stButton>button:hover {
        background: linear-gradient(90deg, #ec4899, #7c3aed);
        transform: scale(1.02);
    }

    textarea {
        background-color: #0b0015 !important;
        color: #f5e9ff !important;
        border: 1px solid #7c3aed !important;
    }

    /* ---------------- AI OUTPUT CARDS ---------------- */

    .ai-card {
        background: linear-gradient(135deg, #120018, #0a0a12);
        border: 1px solid #7c3aed55;
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 15px;
        box-shadow: 0px 0px 12px #ec489922;
    }

    .ai-title {
        color: #ec4899;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 8px;
    }

    .highlight-box {
        background: linear-gradient(90deg, #7c3aed22, #ec489922);
        padding: 12px;
        border-radius: 10px;
        border-left: 4px solid #ec4899;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.title("📘 PassMate Pilot")
st.caption("Ultra AI Exam Assistant — Dark SaaS Edition")


# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
with st.sidebar:
    st.header("⚙ Settings")

    language = st.selectbox("Language", ["English", "Hindi", "Marathi"])
    temperature = st.slider("Creativity", 0.0, 1.0, 0.4)

    uploaded_files = st.file_uploader(
        "Upload PDFs (1–10)",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button("🗑 Reset"):
        st.session_state.pdf_text = ""
        st.success("Reset done")


# ---------------------------------------------------
# AI ENGINE
# ---------------------------------------------------
engine = GeminiEngine(language=language, temperature=temperature)


# ---------------------------------------------------
# MULTI PDF PROCESSING
# ---------------------------------------------------
if uploaded_files:
    text = ""

    for file in uploaded_files:
        raw = extract_text_from_pdf(file)
        text += clean_text(raw) + "\n"

    st.session_state.pdf_text = text

    st.success(f"{len(uploaded_files)} PDFs loaded")

    st.markdown("### 📄 Preview")
    st.text_area("", text[:2000], height=200)

else:
    st.info("Upload PDFs to start analysis")


pdf_text = st.session_state.pdf_text


# ---------------------------------------------------
# AI TOOL BUTTONS
# ---------------------------------------------------
st.divider()
st.header("⚡ AI Tools")

col1, col2, col3 = st.columns(3)
col4, col5 = st.columns(2)


def show_card(title, content):
    st.markdown(f"""
    <div class="ai-card">
        <div class="ai-title">{title}</div>
        <div class="highlight-box">{content}</div>
    </div>
    """, unsafe_allow_html=True)


if col1.button("📄 Summary"):
    result = engine.get_summary(pdf_text)
    show_card("Summary", result)

if col2.button("❓ Questions"):
    result = engine.get_questions(pdf_text)
    show_card("Important Questions", result)

if col3.button("🧠 Quiz"):
    result = engine.get_quiz(pdf_text)
    show_card("Quiz", result)

if col4.button("🃏 Flashcards"):
    result = engine.get_flashcards(pdf_text)
    show_card("Flashcards", result)

if col5.button("📅 Study Plan"):
    result = engine.get_study_plan(pdf_text)
    show_card("Study Plan", result)
