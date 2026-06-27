"""
PassMate Pilot v2.0
Configuration File
"""

import streamlit as st

# ===========================
# APP CONFIG
# ===========================

APP_NAME = "🚀 PassMate Pilot"

APP_TAGLINE = "Your Smart AI Exam Companion"

VERSION = "2.0 Professional"

DEFAULT_THEME = "Dark"

# ===========================
# GEMINI MODEL
# ===========================

GEMINI_MODEL = "gemini-2.5-flash"

# ===========================
# SUBJECT TOPICS
# ===========================

SUBJECT_TOPICS = {

    "Operating System": [
        "process",
        "thread",
        "deadlock",
        "paging",
        "memory",
        "cpu scheduling",
        "semaphore",
        "mutex",
        "virtual memory"
    ],

    "DBMS": [
        "dbms",
        "sql",
        "normalization",
        "transaction",
        "acid",
        "join",
        "er diagram",
        "indexing"
    ],

    "Computer Networks": [
        "osi",
        "tcp",
        "udp",
        "ip",
        "routing",
        "switch",
        "network",
        "dns",
        "http"
    ],

    "Java": [
        "java",
        "oop",
        "inheritance",
        "polymorphism",
        "exception",
        "interface",
        "collection",
        "jdbc",
        "multithreading"
    ],

    "Python": [
        "python",
        "list",
        "tuple",
        "dictionary",
        "numpy",
        "pandas",
        "function",
        "oop"
    ],

    "Machine Learning": [
        "machine learning",
        "regression",
        "classification",
        "clustering",
        "decision tree",
        "random forest",
        "svm",
        "naive bayes",
        "knn"
    ]
}

# ===========================
# COLORS
# ===========================

PRIMARY = "#D7A86E"

SECONDARY = "#5D4037"

BACKGROUND = "#000000"

CARD = "#2D1B14"

TEXT = "#FFFFFF"

SUCCESS = "#00C853"

WARNING = "#FFC107"

ERROR = "#FF5252"

# ===========================
# PDF SETTINGS
# ===========================

PDF_TITLE = "PassMate Pilot AI Report"

PDF_AUTHOR = "PassMate Pilot"

# ===========================
# DEFAULT PROMPTS
# ===========================

SUMMARY_PROMPT = """
Summarize these exam questions.
Generate:
- Important topics
- Frequently asked concepts
- Revision notes
"""

QUESTION_PROMPT = """
Predict the most probable university examination questions based on the uploaded previous year papers.
Generate:
- 2 Mark Questions
- 5 Mark Questions
- 10 Mark Questions
"""

EXPLAIN_PROMPT = """
Explain this topic in simple language suitable for university exam preparation.
Include examples wherever possible.
"""

STUDY_PLAN_PROMPT = """
Create an intelligent study plan according to the remaining number of days before the exam.
"""

# ===========================
# PAGE STYLE
# ===========================

CUSTOM_CSS = """
<style>

.stApp{
background:linear-gradient(
135deg,
#000000,
#1A120B,
#3E2723
);
color:white;
}

h1,h2,h3{
color:#D7A86E;
text-align:center;
}

.stButton>button{
background:#5D4037;
color:white;
border-radius:12px;
border:none;
font-weight:bold;
}

.stButton>button:hover{
background:#8D6E63;
}

[data-testid="metric-container"]{
background:#2D1B14;
padding:18px;
border-radius:15px;
}

</style>
"""

# ===========================
# STREAMLIT CONFIG
# ===========================

def setup_page():

    st.set_page_config(

        page_title=APP_NAME,

        page_icon="🚀",

        layout="wide"

    )

    st.markdown(

        CUSTOM_CSS,

        unsafe_allow_html=True

    )
