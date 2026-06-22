import streamlit as st
import pdfplumber
import pandas as pd
import matplotlib.pyplot as plt

from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer

import re

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="🎯 AI Exam Question Predictor",
    page_icon="🎯",
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

st.title("🎯 AI Exam Question Predictor")

st.markdown("""
### Upload Previous Year Question Papers

Find:

✅ Repeated Questions  
✅ Important Topics  
✅ Topic Probability  
✅ Charts  
✅ Download CSV

No API Required 🚀
""")

# ---------------- UPLOADER ----------------

uploaded_files = st.file_uploader(

    "📄 Upload PDF Files",

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


# ---------------- TOPIC EXTRACTION ----------------

def extract_topics(questions):

    vectorizer=CountVectorizer(

        stop_words='english',

        max_features=20

    )

    X=vectorizer.fit_transform(questions)

    words=vectorizer.get_feature_names_out()

    counts=X.sum(axis=0).A1

    topics=dict(zip(words,counts))

    return topics


# ---------------- PROCESS ----------------

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

                    f"Could not read {file.name}"

                )


# ---------------- RESULTS ----------------

if len(all_questions)>0:

    counter=Counter(all_questions)

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

        "🔥 Max Frequency",

        df["Frequency"].max()

    )

    st.divider()

    # Questions

    st.subheader("🔥 Most Repeated Questions")

    st.dataframe(

        df,

        use_container_width=True

    )

    st.divider()

    # Important Questions

    st.subheader(

        "🎯 Predicted Important Questions"

    )

    important=df[

        df["Frequency"]>=2

    ]

    if len(important):

        for q in important["Question"]:

            st.write("✅",q)

    else:

        st.info(

            "Upload more papers."

        )

    st.divider()

    # Topics

    st.subheader(

        "🧠 Important Topics"

    )

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

    top10=topic_df.head(10)

    ax.bar(

        top10["Topic"],

        top10["Count"]

    )

    plt.xticks(rotation=45)

    st.pyplot(fig)

    st.divider()

    # Download CSV

    csv=topic_df.to_csv(

        index=False

    )

    st.download_button(

        "⬇ Download Topic Analysis CSV",

        csv,

        file_name=

        "topic_analysis.csv",

        mime="text/csv"

    )

else:

    st.info(

        "👆 Upload at least 2-5 PDFs."

    )

st.divider()

st.markdown("""

### Best Results

Upload papers of:

📘 Operating System  
📘 Computer Networks  
📘 DBMS  
📘 Data Structures  
📘 Software Engineering  

The more PDFs you upload,

the better the predictions.

""")
