import streamlit as st
import pdfplumber
import pandas as pd
from collections import Counter
import re

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="🎯 AI Exam Question Predictor",
    page_icon="🎯",
    layout="wide"
)

# ---------------- CUSTOM THEME ----------------

st.markdown("""
<style>

/* Main Background */

.stApp {

background: linear-gradient(
135deg,
#000000,
#1a120b,
#3e2723
);

color:white;

}

/* Headers */

h1,h2,h3 {

color:#D7A86E;

text-align:center;

}

/* Paragraph */

p,div,span,label{

color:white;

}

/* Buttons */

.stButton > button{

background:#5d4037;

color:white;

border-radius:15px;

border:2px solid #8d6e63;

font-weight:bold;

padding:10px 20px;

}

.stButton > button:hover{

background:#8d6e63;

}

/* File uploader */

section[data-testid="stFileUploader"]{

background:#2d1b14;

padding:20px;

border-radius:15px;

}

/* Metrics */

[data-testid="metric-container"]{

background:#2d1b14;

padding:15px;

border-radius:15px;

border:1px solid #8d6e63;

}

/* Dataframe */

[data-testid="stDataFrame"]{

background:#1e1e1e;

border-radius:15px;

}

/* Success */

.stSuccess{

background:#2e7d32;

}

/* Warning */

.stWarning{

background:#ef6c00;

}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------

st.title("🎯 AI Exam Question Predictor")

st.markdown(
"""
### Upload Previous Year Question Papers

Find:

✅ Most Repeated Questions  
✅ Important Questions  
✅ Question Frequency  
✅ Exam Statistics  

No API Key Required 🚀
"""
)

# ---------------- FILE UPLOADER ----------------

uploaded_files = st.file_uploader(

    "📄 Upload PDF Files",

    type=["pdf"],

    accept_multiple_files=True

)

# ---------------- FUNCTION ----------------

def extract_questions(text):

    questions = []

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if len(line) < 10:

            continue

        if "?" in line:

            questions.append(line)

        elif re.match(r"^\d+\.", line):

            questions.append(line)

        elif re.match(r"^Q\d+", line):

            questions.append(line)

        elif re.match(r"^Question", line, re.IGNORECASE):

            questions.append(line)

    return questions

# ---------------- PROCESS ----------------

all_questions = []

if uploaded_files:

    with st.spinner("🔍 Analyzing Question Papers..."):

        for file in uploaded_files:

            try:

                with pdfplumber.open(file) as pdf:

                    text = ""

                    for page in pdf.pages:

                        page_text = page.extract_text()

                        if page_text:

                            text += page_text + "\n"

                    questions = extract_questions(text)

                    all_questions.extend(questions)

            except:

                st.warning(f"❌ Could not read {file.name}")

# ---------------- RESULTS ----------------

if len(all_questions) > 0:

    counter = Counter(all_questions)

    df = pd.DataFrame(

        counter.items(),

        columns=["Question","Frequency"]

    )

    df = df.sort_values(

        by="Frequency",

        ascending=False

    )

    st.success("✅ Analysis Complete!")

    # Metrics

    c1,c2,c3 = st.columns(3)

    c1.metric(

        "📄 Total Questions",

        len(all_questions)

    )

    c2.metric(

        "🧠 Unique Questions",

        len(df)

    )

    c3.metric(

        "🔥 Most Repeated",

        df.iloc[0]["Frequency"]

    )

    st.divider()

    # Repeated Questions

    st.subheader("🔥 Most Repeated Questions")

    st.dataframe(

        df,

        use_container_width=True

    )

    st.divider()

    # Important Questions

    st.subheader("🎯 Predicted Important Questions")

    important = df[df["Frequency"] >= 2]

    if len(important):

        for q in important["Question"]:

            st.markdown(f"✅ **{q}**")

    else:

        st.info(

            "Upload more PDFs for better prediction."

        )

    st.divider()

    # Download CSV

    csv = df.to_csv(index=False)

    st.download_button(

        label="⬇ Download Analysis CSV",

        data=csv,

        file_name="exam_analysis.csv",

        mime="text/csv"

    )

else:

    st.info(

        "👆 Upload at least 2-5 previous year question papers to begin analysis."

    )

# ---------------- FOOTER ----------------

st.divider()

st.markdown(
"""
### Suggested Papers to Upload

📘 Operating System  
📘 Computer Networks  
📘 Data Structures  
📘 DBMS  
📘 Software Engineering  

Best Results: Upload 5 or more previous year papers.
"""
)
