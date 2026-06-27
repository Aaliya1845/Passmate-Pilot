"""
PassMate Pilot SaaS v3
Startup-Level AI Learning Platform
"""

import streamlit as st
from datetime import datetime

from ai_engine import GeminiEngine
from utils import extract_text_from_pdf, clean_text


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="PassMate Pilot ",
    page_icon="📘",
    layout="wide"
)


# ---------------------------------------------------
# PREMIUM SAAS THEME (BLACK + PURPLE + PINK)
# ---------------------------------------------------
st.markdown(
    """
    <style>

    .stApp {
        background: radial-gradient(circle at top, #05050a, #0b0015, #120018);
        color: #f5e9ff;
        font-family: 'Arial';
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
        font-weight: bold;
        transition: 0.2s;
    }

    .stButton>button:hover {
        transform: scale(1.03);
        box-shadow: 0px 0px 18px #ec489966;
    }

    textarea {
        background-color: #0b0015 !important;
        color: #f5e9ff !important;
        border: 1px solid #7c3aed !important;
    }

    /* SaaS CARDS */
    .card {
        background: rgba(20, 10, 40, 0.6);
        border: 1px solid rgba(168, 85, 247, 0.3);
        padding: 16px;
        border-radius: 16px;
        margin-bottom: 14px;
        backdrop-filter: blur(10px);
        box-shadow: 0px 0px 20px rgba(236, 72, 153, 0.1);
    }

    .title {
        color: #ec4899;
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 8px;
    }

    .small {
        font-size: 12px;
        opacity: 0.7;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.title("📘 PassMate Pilot")
st.caption("AI-powered Smart Learning & Exam Assistant")


# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
with st.sidebar:
    st.header("⚙ Control Panel")

    language = st.selectbox("Language", ["English", "Hindi", "Marathi"])
    temperature = st.slider("AI Creativity", 0.0, 1.0, 0.4)

    uploaded_files = st.file_uploader(
        "Upload PDFs (1–10)",
        type=["pdf"],
        accept_multiple_files=True
    )

    st.divider()

    if st.button("🧹 Reset Session"):
        st.session_state.pdf_text = ""
        st.session_state.chat_history = []
        st.success("Session Cleared")


# ---------------------------------------------------
# AI ENGINE
# ---------------------------------------------------
engine = GeminiEngine(language=language, temperature=temperature)


# ---------------------------------------------------
# PDF PROCESSING (SMART MERGE)
# ---------------------------------------------------
if uploaded_files:
    full_text = ""

    for file in uploaded_files:
        raw = extract_text_from_pdf(file)
        clean = clean_text(raw)
        full_text += "\n" + clean

    st.session_state.pdf_text = full_text

    st.success(f"{len(uploaded_files)} PDFs processed successfully")

    st.text_area("📄 Preview", full_text[:2000], height=200)

else:
    st.info("Upload PDFs to unlock AI features")


text = st.session_state.pdf_text


# ---------------------------------------------------
# CARD UI FUNCTION
# ---------------------------------------------------
def card(title, content):
    st.markdown(f"""
    <div class="card">
        <div class="title">{title}</div>
        <div>{content}</div>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------
# AI DASHBOARD
# ---------------------------------------------------
st.divider()
st.header("⚡ AI Dashboard")

col1, col2, col3 = st.columns(3)
col4, col5 = st.columns(2)


if col1.button("📄 Summary"):
    st.session_state.summary = engine.get_summary(text)
    card("Summary", st.session_state.summary)

if col2.button("❓ Questions"):
    st.session_state.questions = engine.get_questions(text)
    card("Important Questions", st.session_state.questions)

if col3.button("🧠 Quiz"):
    st.session_state.quiz = engine.get_quiz(text)
    card("Quiz", st.session_state.quiz)

if col4.button("🃏 Flashcards"):
    st.session_state.flashcards = engine.get_flashcards(text)
    card("Flashcards", st.session_state.flashcards)

if col5.button("📅 Study Plan"):
    st.session_state.study_plan = engine.get_study_plan(text)
    card("Study Plan", st.session_state.study_plan)


# ---------------------------------------------------
# AI CHAT SYSTEM (SAAS STYLE)
# ---------------------------------------------------
st.divider()
st.header("💬 AI Tutor Chat")

query = st.text_input("Ask your AI Tutor anything")

if query:
    prompt = f"""
    You are PassMate Pilot AI Tutor.

    Context:
    {text}

    Question:
    {query}
    """

    response = engine._generate(prompt)

    st.session_state.chat_history.append((query, response))

    card("AI Answer", response)


# ---------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------
st.subheader("🧠 Recent Conversations")

for q, a in st.session_state.chat_history[-10:]:
    st.markdown(f"**Q:** {q}")
    st.markdown(f"**A:** {a}")
    st.write("---")


# ---------------------------------------------------
# EXPORT SYSTEM
# ---------------------------------------------------
st.divider()
st.header("📄 Export Report")

if st.button("Generate Report"):

    report = f"""
PASSMATE PILOT SAAS REPORT
Generated: {datetime.now()}

========================
SUMMARY
========================
{st.session_state.get('summary', '')}

========================
QUESTIONS
========================
{st.session_state.get('questions', '')}

========================
QUIZ
========================
{st.session_state.get('quiz', '')}

========================
STUDY PLAN
========================
{st.session_state.get('study_plan', '')}
"""

    st.download_button(
        "⬇ Download Report",
        report,
        file_name="passmate_pilot_report.txt"
    )
