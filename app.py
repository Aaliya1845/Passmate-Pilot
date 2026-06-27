"""
PassMate Pilot (Pro Max)
AI Exam Preparation Assistant
"""

import streamlit as st
from datetime import datetime

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
# FUTURISTIC DARK THEME (BLACK + PURPLE + BLUE)
# ---------------------------------------------------
st.markdown(
    """
    <style>

    .stApp {
        background: radial-gradient(circle at top left, #0b0b0f, #050510, #0a0015);
        color: #e6e6ff;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b0b0f, #120022);
    }

    h1, h2, h3 {
        color: #b794f4;
    }

    .stButton>button {
        background: linear-gradient(90deg, #6d28d9, #2563eb);
        color: white;
        border-radius: 10px;
        border: none;
        width: 100%;
        height: 45px;
        font-weight: bold;
    }

    .stButton>button:hover {
        background: linear-gradient(90deg, #2563eb, #6d28d9);
        transform: scale(1.02);
    }

    textarea {
        background-color: #0b0b0f !important;
        color: #e6e6ff !important;
        border: 1px solid #6d28d9 !important;
    }

    .block-container {
        padding-top: 2rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.title("📘 PassMate Pilot")
st.caption("AI-powered exam preparation assistant (Pro Max Edition)")


# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------
for key in ["pdf_text", "chat_history"]:
    if key not in st.session_state:
        st.session_state[key] = "" if key == "pdf_text" else []


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
with st.sidebar:
    st.header("⚙ Settings")

    language = st.selectbox("Language", ["English", "Hindi", "Marathi"])
    temperature = st.slider("Creativity", 0.0, 1.0, 0.4)

    st.divider()

    uploaded_files = st.file_uploader(
        "Upload 1–10 PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    st.divider()

    if st.button("🗑 Reset"):
        st.session_state.pdf_text = ""
        st.session_state.chat_history = []
        st.success("Reset Done")


# ---------------------------------------------------
# INIT AI ENGINE
# ---------------------------------------------------
engine = GeminiEngine(language=language, temperature=temperature)


# ---------------------------------------------------
# MULTI PDF PROCESSING
# ---------------------------------------------------
if uploaded_files:
    combined_text = ""

    for file in uploaded_files:
        with st.spinner(f"Processing {file.name}..."):
            text = extract_text_from_pdf(file)
            text = clean_text(text)
            combined_text += "\n" + text

    st.session_state.pdf_text = combined_text

    st.success(f"{len(uploaded_files)} PDFs loaded")

    st.text_area("Preview", combined_text[:2500], height=200)

else:
    st.info("Upload PDFs to begin analysis")


# ---------------------------------------------------
# AI TOOLS
# ---------------------------------------------------
st.divider()
st.header("⚡ AI Tools")

col1, col2, col3 = st.columns(3)
col4, col5 = st.columns(2)

text = st.session_state.pdf_text


with col1:
    if st.button("📄 Summary"):
        st.session_state.summary = engine.get_summary(text)

with col2:
    if st.button("❓ Questions"):
        st.session_state.questions = engine.get_questions(text)

with col3:
    if st.button("🧠 Quiz"):
        st.session_state.quiz = engine.get_quiz(text)

with col4:
    if st.button("🃏 Flashcards"):
        st.session_state.flashcards = engine.get_flashcards(text)

with col5:
    if st.button("📅 Study Plan"):
        st.session_state.study_plan = engine.get_study_plan(text)


# ---------------------------------------------------
# CHAT WITH PDF (NEW FEATURE)
# ---------------------------------------------------
st.divider()
st.header("💬 Chat with PDF")

user_query = st.text_input("Ask anything from your notes")

if user_query:
    prompt = f"""
    You are PassMate Pilot AI Tutor.

    Use the following notes:
    {text}

    Question: {user_query}
    """

    response = engine._generate(prompt)

    st.markdown("### Answer")
    st.write(response)

    st.session_state.chat_history.append((user_query, response))


# ---------------------------------------------------
# OUTPUT SECTION
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
# CHAT HISTORY
# ---------------------------------------------------
st.divider()
st.subheader("🧠 Chat History")

for q, a in st.session_state.chat_history[-10:]:
    st.markdown(f"**Q:** {q}")
    st.markdown(f"**A:** {a}")
    st.write("---")
