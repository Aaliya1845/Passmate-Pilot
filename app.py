import streamlit as st
import pdfplumber
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

import tempfile
import re

# ---------------- PAGE CONFIG ----------------

st.set_page_config(

    page_title="🚀 PassMate Pilot",

    page_icon="🚀",

    layout="wide"

)

# ---------------- THEME ----------------

st.markdown("""

<style>

.stApp{

background:linear-gradient(

135deg,

#000000,

#1a120b,

#3e2723

);

color:white;

}

h1,h2,h3{

color:#D7A86E;

text-align:center;

}

p,div,label,span{

color:white;

}

.stButton>button{

background:#5d4037;

color:white;

border-radius:15px;

border:2px solid #8d6e63;

font-weight:bold;

}

.stButton>button:hover{

background:#8d6e63;

}

section[data-testid="stFileUploader"]{

background:#2d1b14;

padding:20px;

border-radius:15px;

}

[data-testid="metric-container"]{

background:#2d1b14;

padding:15px;

border-radius:15px;

}

</style>

""", unsafe_allow_html=True)

# ---------------- TITLE ----------------

st.title("🚀 PassMate Pilot")

st.markdown("""

### Your Smart AI Exam Companion

📚 Upload Previous Year Papers

PassMate Pilot helps you discover:

✅ Important Questions

✅ Similar Questions

✅ Important Topics

✅ Probability of Topics

✅ Smart Charts

✅ Download PDF Reports

🎯 Predict Smarter • Study Better • Pass Confidently

""")

# ---------------- FILE UPLOADER ----------------

uploaded_files = st.file_uploader(

    "📄 Upload Previous Year Question Papers",

    type=["pdf"],

    accept_multiple_files=True

)

# ---------------- QUESTION EXTRACTION ----------------

def extract_questions(text):

    questions=[]

    lines=text.split("\n")

    for line in lines:

        line=line.strip()

        if len(line)<10:

            continue

        if "?" in line:

            questions.append(line)

        elif re.match(r"^\d+\.",line):

            questions.append(line)

        elif re.match(r"^Q\d+",line):

            questions.append(line)

        elif re.match(r"^Question",line,re.I):

            questions.append(line)

    return questions


# ---------------- SIMILAR QUESTION DETECTION ----------------

def group_similar_questions(questions):

    if len(questions)<=1:

        return questions

    tfidf=TfidfVectorizer(

        stop_words='english'

    )

    X=tfidf.fit_transform(

        questions

    )

    similarity=cosine_similarity(X)

    grouped=[]

    used=set()

    for i in range(len(questions)):

        if i in used:

            continue

        temp=[questions[i]]

        used.add(i)

        for j in range(i+1,len(questions)):

            if j in used:

                continue

            if similarity[i][j]>0.6:

                temp.append(

                    questions[j]

                )

                used.add(j)

        grouped.append(

            temp[0]

        )

    return grouped


# ---------------- TOPIC LIST ----------------

TOPICS=[

"deadlock",

"process",

"scheduling",

"thread",

"paging",

"inheritance",

"oop",

"java",

"jdbc",

"exception",

"interface",

"multithreading",

"collection",

"thevenin",

"norton",

"mesh",

"nodal",

"resonance",

"network",

"dbms",

"normalization",

"sql",

"testing",

"osi",

"tcp",

"udp"

]


# ---------------- TOPIC EXTRACTION ----------------

def extract_topics(questions):

    topic_count={}

    text=" ".join(

        questions

    ).lower()

    for topic in TOPICS:

        count=text.count(

            topic

        )

        if count>0:

            topic_count[topic]=count

    return topic_count


# ---------------- PDF REPORT ----------------

def generate_report(

questions,

topics

):

    temp=tempfile.NamedTemporaryFile(

        delete=False,

        suffix=".pdf"

    )

    doc=SimpleDocTemplate(

        temp.name

    )

    styles=getSampleStyleSheet()

    story=[]

    story.append(

        Paragraph(

            "<b>PassMate Pilot - AI Exam Analysis Report</b>",

            styles["Title"]

        )

    )

    story.append(

        Spacer(

            1,

            20

        )

    )

    story.append(

        Paragraph(

            "<b>Important Questions</b>",

            styles["Heading2"]

        )

    )

    for q in questions[:10]:

        story.append(

            Paragraph(

                q,

                styles["BodyText"]

            )

        )

    story.append(

        Spacer(

            1,

            20

        )

    )

    story.append(

        Paragraph(

            "<b>Important Topics</b>",

            styles["Heading2"]

        )

    )

    for t,c in topics.items():

        story.append(

            Paragraph(

                f"{t} : {c}",

                styles["BodyText"]

            )

        )

    doc.build(

        story

    )

    return temp.name

# ---------------- PROCESS PDFs ----------------

all_questions=[]

if uploaded_files:

    with st.spinner("🔍 Analyzing PDFs..."):

        for file in uploaded_files:

            try:

                with pdfplumber.open(file) as pdf:

                    text=""

                    for page in pdf.pages:

                        page_text=page.extract_text()

                        if page_text:

                            text+=page_text+"\n"

                    questions=extract_questions(text)

                    all_questions.extend(questions)

            except:

                st.warning(

                    f"❌ Could not read {file.name}"

                )


# ---------------- RESULTS ----------------

if len(all_questions)>0:

    similar_questions=group_similar_questions(

        all_questions

    )

    counter=Counter(

        similar_questions

    )

    df=pd.DataFrame(

        counter.items(),

        columns=[

            "Question",

            "Frequency"

        ]

    )

    df=df.sort_values(

        by="Frequency",

        ascending=False

    )

    st.success("✅ Analysis Complete")

    c1,c2,c3=st.columns(3)

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

        df["Frequency"].max()

    )

    st.divider()

    # Important Questions

    st.subheader(

        "🔥 Important Questions"

    )

    st.dataframe(

        df,

        use_container_width=True

    )

    st.divider()

    # Topics

    topics=extract_topics(

        all_questions

    )

    topic_df=pd.DataFrame(

        topics.items(),

        columns=[

            "Topic",

            "Count"

        ]

    )

    if len(topic_df)>0:

        topic_df=topic_df.sort_values(

            by="Count",

            ascending=False

        )

        topic_df["Probability"]=round(

            topic_df["Count"]

            /

            topic_df["Count"].sum()

            *100,

            2

        )

        topic_df["Chance"]=round(

            topic_df["Count"]

            /

            topic_df["Count"].max()

            *100,

            0

        )

        st.subheader(

            "🎯 Most Likely To Appear"

        )

        st.dataframe(

            topic_df,

            use_container_width=True

        )

        st.divider()

        # Chart

        st.subheader(

            "📊 Topic Frequency Chart"

        )

        fig,ax=plt.subplots(

            figsize=(8,4)

        )

        top=topic_df.head(10)

        ax.bar(

            top["Topic"],

            top["Count"]

        )

        plt.xticks(

            rotation=45

        )

        st.pyplot(fig)

        st.divider()

        # Study Planner

        st.subheader(

            "📅 Study Planner"

        )

        days=st.number_input(

            "Days left for exam",

            min_value=1,

            max_value=60,

            value=7

        )

        if st.button(

            "Generate Study Plan"

        ):

            plan=topic_df.head(days)

            for i,row in enumerate(

                plan.itertuples(),

                start=1

            ):

                st.write(

                    f"Day {i} → {row.Topic}"

                )

        st.divider()

        # Quiz Mode

        st.subheader(

            "📝 Quiz Mode"

        )

        if len(df)>0:

            q=df.iloc[0]["Question"]

            st.write(

                "Question:"

            )

            st.info(q)

            ans=st.text_area(

                "Your Answer"

            )

            if st.button(

                "Submit Answer"

            ):

                st.success(

                    "✅ Good Attempt! Keep Practicing."

                )

        st.divider()

        # PDF Report

        report=generate_report(

            list(

                df["Question"]

            ),

            topics

        )

        with open(

            report,

            "rb"

        ) as f:

            st.download_button(

                "⬇ Download PDF Report",

                f,

                file_name=

                "PassMate_Pilot_Report.pdf",

                mime=

                "application/pdf"

            )

else:

    st.info(

        "👆 Upload at least 2-5 previous year PDFs."

    )


# ---------------- FOOTER ----------------

st.divider()

st.markdown("""

## 🚀 PassMate Pilot

Your Smart AI Exam Companion

📚 Predict Important Questions

🧠 Discover Important Topics

📊 Analyze Previous Papers

🎯 Study Smarter & Pass Confidently

Best Results:

Upload 5–10 previous year papers.

""")
