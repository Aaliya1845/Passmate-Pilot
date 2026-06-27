import streamlit as st
import time

from ai_engine import GeminiEngine
from utils import extract_text_from_pdf, clean_text


# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="PassMate Pilot",
    page_icon="📘",
    layout="wide"
)


# ---------------------------------------------------
# THEME (BLACK + PURPLE + PINK)
# ---------------------------------------------------
st.markdown("""
<style>

.stApp {
    background: radial-gradient(circle at top, #05050a, #0b0015, #120018);
    color: #f5e9ff;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b0015, #1a0025);
}

h1, h2, h3 {
    color: #e879f9;
}

.stButton>button {
    background: linear-gradient(90deg, #7c3aed, #ec4899);
    color: white;
    border-radius: 12px;
    border: none;
    height: 45px;
    width: 100%;
}

.stButton>button:hover {
    transform: scale(1.02);
}

.card {
    background: rgba(20,10,40,0.6);
    border: 1px solid rgba(168,85,247,0.3);
    padding: 15px;
    border-radius: 14px;
    margin-bottom: 12px;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

if "last_click" not in st.session_state:
    st.session_state.last_click = 0


# ---------------------------------------------------
# ENGINE
# ---------------------------------------------------
engine = GeminiEngine()


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
with st.sidebar:
    st.title("PassMate Pilot")

    uploaded_files = st.file_uploader(
        "Upload 1–10 PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button("Reset"):
        st.session_state.pdf_text = ""
        st.success("Reset done")


# ---------------------------------------------------
# MULTI PDF
# ---------------------------------------------------
if uploaded_files:
    text = ""

    for file in uploaded_files:
        raw = extract_text_from_pdf(file)
        text += clean_text(raw)

    st.session_state.pdf_text = text

    st.success(f"{len(uploaded_files)} PDFs loaded")


pdf_text = st.session_state.pdf_text


# ---------------------------------------------------
# SAFE BUTTON WRAPPER
# ---------------------------------------------------
def safe_click():
    if time.time() - st.session_state.last_click < 5:
        st.warning("Wait 5 seconds before next request")
        st.stop()
    st.session_state.last_click = time.time()


# ---------------------------------------------------
# UI CARD
# ---------------------------------------------------
def card(title, content):
    st.markdown(f"""
    <div class="card">
        <h3>{title}</h3>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------
# AI TOOLS
# ---------------------------------------------------
st.title("⚡ AI Dashboard")

col1, col2, col3 = st.columns(3)
col4, col5 = st.columns(2)


if col1.button("Summary"):
    safe_click()
    st.session_state.summary = engine.get_summary(pdf_text)
    card("Summary", st.session_state.summary)

if col2.button("Questions"):
    safe_click()
    st.session_state.questions = engine.get_questions(pdf_text)
    card("Questions", st.session_state.questions)

if col3.button("Quiz"):
    safe_click()
    st.session_state.quiz = engine.get_quiz(pdf_text)
    card("Quiz", st.session_state.quiz)

if col4.button("Flashcards"):
    safe_click()
    st.session_state.flashcards = engine.get_flashcards(pdf_text)
    card("Flashcards", st.session_state.flashcards)

if col5.button("Study Plan"):
    safe_click()
    st.session_state.study_plan = engine.get_study_plan(pdf_text)
    card("Study Plan", st.session_state.study_plan)


# ---------------------------------------------------
# CHAT
# ---------------------------------------------------
st.divider()
st.title("💬 Chat")

query = st.text_input("Ask anything from PDF")

if query:
    safe_click()

    prompt = f"""
Use this content:
{pdf_text}

Question:
{query}
"""

    response = engine._generate(prompt)

    card("Answer", response)
