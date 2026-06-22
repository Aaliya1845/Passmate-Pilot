import streamlit as st
import pdfplumber
import pandas as pd
from collections import Counter
import re

st.set_page_config(
    page_title="🎯 AI Exam Question Predictor",
    page_icon="🎯"
)

st.title("🎯 AI Exam Question Predictor")

st.write(
    "Upload previous year question papers and discover repeated & important questions."
)

uploaded_files = st.file_uploader(
    "Upload PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

all_questions = []

# Extract questions

def extract_questions(text):

    lines = text.split("\n")

    questions = []

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

    return questions


if uploaded_files:

    with st.spinner("Analyzing PDFs..."):

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

                st.warning(f"Could not read {file.name}")

    if len(all_questions) == 0:

        st.error("No questions found.")

    else:

        counter = Counter(all_questions)

        df = pd.DataFrame(
            counter.items(),
            columns=["Question", "Frequency"]
        )

        df = df.sort_values(
            by="Frequency",
            ascending=False
        )

        st.success("Analysis Complete!")

        st.subheader("🔥 Most Repeated Questions")

        st.dataframe(
            df,
            use_container_width=True
        )

        st.subheader("🎯 Predicted Important Questions")

        important = df[df["Frequency"] >= 2]

        if len(important):

            for q in important["Question"]:

                st.write("✅", q)

        else:

            st.info(
                "Upload more PDFs to improve prediction."
            )

        st.subheader("📊 Statistics")

        st.metric(
            "Total Questions",
            len(all_questions)
        )

        st.metric(
            "Unique Questions",
            len(df)
        )
