"""
PassMate Pilot Pro Max v2
SaaS-Level AI Exam Assistant
"""

import streamlit as st
from datetime import datetime

from ai_engine import GeminiEngine
from utils import extract_text_from_pdf, clean_text


# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="PassMate Pilot Pro",
    page_icon="📘",
    layout="wide"
)


# ---------------------------------------------------
# THEME (BLACK + PURPLE + PINK SAAS STYLE)
# ---------------------------------------------------
st.markdown(
    """
    <style>

    .stApp {
        background: radial-gradient(circle at top, #05050a, #0b0015, #120018);
        color: #f5e9ff;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b0015, #1a0025);
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
    }

    .stButton>button:hover {
        transform: scale(1.03);
        box-shadow: 0px 0px 15px #ec489955;
    }

    textarea {
        background-color: #0b0015 !important;
        color: #f5e9ff !important;
    }

    .card {
        background: linear-gradient(135deg, #120018, #0b0b12);
        border: 1px solid #7c3aed55;
        padding: 15px;
        border-radius: 14px;
        margin-bottom: 12px;
    }

    .title {
        color: #ec4899;
        font-weight: bold;
        font-size: 18px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.title("📘 PassMate Pilot Pro Max")
st.caption("AI-powered exam success assistant")


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
    st.header("⚙ Settings")

    language = st.selectbox("Language", ["English", "Hindi", "Marathi"])
    temperature = st.slider("Creativity", 0.0, 1.0, 0.4)

    uploaded_files = st.file_uploader(
        "Upload 1–10 PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    st.divider()

    if st.button("🗑 Reset Everything"):
        st.session_state.pdf_text = ""
        st.session_state.chat_history = []
        st.success("Reset done")


# ---------------------------------------------------
# AI ENGINE
# ---------------------------------------------------
engine = GeminiEngine(language=language, temperature=temperature)


# ---------------------------------------------------
# PDF PROCESSING
# ---------------------------------------------------
if uploaded_files:
    all_text = ""

    for file in uploaded_files:
        raw = extract_text_from_pdf(file)
        clean = clean_text(raw)
        all_text += "\n" + clean

    st.session_state.pdf_text = all_text

    st.success(f"{len(uploaded_files)} PDFs loaded")

    st.text_area("Preview", all_text[:2000], height=200)

else:
    st.info("Upload PDFs to begin")


text = st.session_state.pdf_text


# ---------------------------------------------------
# AI DASHBOARD BUTTONS
# ---------------------------------------------------
st.divider()
st.header("⚡ AI Dashboard")

col1, col2, col3 = st.columns(3)
col4, col5 = st.columns(2)


def card(title, content):
    st.markdown(f"""
    <div class="card">
        <div class="title">{title}</div>
        <div>{content}</div>
    </div>
    """, unsafe_allow_html=True)


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
# CHAT WITH PDF (SAAS FEATURE)
# ---------------------------------------------------
st.divider()
st.header("💬 AI Chat Assistant")

user_input = st.text_input("Ask anything from your PDFs")

if user_input:
    prompt = f"""
    You are PassMate Pilot AI Tutor.

    Use this content:
    {text}

    Question:
    {user_input}
    """

    response = engine._generate(prompt)

    st.session_state.chat_history.append((user_input, response))

    card("Answer", response)


# ---------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------
st.divider()
st.subheader("🧠 Chat History")

for q, a in st.session_state.chat_history[-10:]:
    st.markdown(f"**Q:** {q}")
    st.markdown(f"**A:** {a}")
    st.write("---")


# ---------------------------------------------------
# PDF DOWNLOAD REPORT
# ---------------------------------------------------
st.divider()
st.header("📄 Export Report")

if st.button("Download Summary Report"):

    report = f"""
PASSMATE PILOT REPORT
Generated: {datetime.now()}

SUMMARY:
{st.session_state.get('summary', '')}

QUESTIONS:
{st.session_state.get('questions', '')}

QUIZ:
{st.session_state.get('quiz', '')}

STUDY PLAN:
{st.session_state.get('study_plan', '')}
"""

    st.download_button(
        "⬇ Download TXT Report",
        report,
        file_name="passmate_report.txt"
    )
