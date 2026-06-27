"""
PassMate Pilot v2.0
utils.py (Part 1)

Utility functions:
- Read PDF files
- Extract questions
- Clean text
- Remove duplicate questions
- Detect subject
- Group similar questions
"""

import re
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from config import SUBJECT_TOPICS


# ======================================================
# READ PDF
# ======================================================

def extract_text_from_pdf(uploaded_file):
    """
    Extract text from uploaded PDF.
    """

    text = ""

    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

    except Exception:
        return ""

    return text


# ======================================================
# CLEAN TEXT
# ======================================================

def clean_text(text):
    """
    Clean unnecessary spaces and symbols.
    """

    text = re.sub(r"\s+", " ", text)
    text = text.replace("\t", " ")
    text = text.strip()

    return text


# ======================================================
# EXTRACT QUESTIONS
# ======================================================

def extract_questions(text):
    """
    Extract likely questions from text.
    """

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

        elif re.match(r"^Q\d+", line, re.IGNORECASE):
            questions.append(line)

        elif re.match(r"^Question", line, re.IGNORECASE):
            questions.append(line)

    return questions


# ======================================================
# REMOVE DUPLICATES
# ======================================================

def remove_duplicate_questions(questions):
    """
    Remove exact duplicate questions.
    """

    unique = []

    seen = set()

    for q in questions:

        q = clean_text(q)

        if q.lower() not in seen:

            unique.append(q)

            seen.add(q.lower())

    return unique


# ======================================================
# TF-IDF SIMILARITY
# ======================================================

def group_similar_questions(
    questions,
    threshold=0.60
):
    """
    Merge very similar questions.
    """

    if len(questions) <= 1:
        return questions

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    matrix = vectorizer.fit_transform(questions)

    similarity = cosine_similarity(matrix)

    grouped = []

    used = set()

    for i in range(len(questions)):

        if i in used:
            continue

        grouped.append(questions[i])

        used.add(i)

        for j in range(i + 1, len(questions)):

            if j in used:
                continue

            if similarity[i][j] >= threshold:

                used.add(j)

    return grouped


# ======================================================
# SUBJECT DETECTION
# ======================================================

def detect_subject(questions):
    """
    Detect the subject from uploaded papers.
    """

    combined_text = " ".join(questions).lower()

    scores = {}

    for subject, keywords in SUBJECT_TOPICS.items():

        score = 0

        for keyword in keywords:

            score += combined_text.count(keyword.lower())

        scores[subject] = score

    if max(scores.values()) == 0:
        return "Unknown Subject"

    return max(scores, key=scores.get)


# ======================================================
# SUBJECT SCORE TABLE
# ======================================================

def get_subject_scores(questions):
    """
    Returns score of every subject.
    """

    combined_text = " ".join(questions).lower()

    scores = {}

    for subject, keywords in SUBJECT_TOPICS.items():

        score = 0

        for keyword in keywords:

            score += combined_text.count(keyword.lower())

        scores[subject] = score

    return scores

# ======================================================
# TOPIC EXTRACTION
# ======================================================

from collections import Counter
import pandas as pd


def extract_topics(questions):
    """
    Extract important topics from questions.
    """

    topic_counter = Counter()

    combined_text = " ".join(questions).lower()

    for subject, keywords in SUBJECT_TOPICS.items():

        for keyword in keywords:

            count = combined_text.count(keyword.lower())

            if count > 0:
                topic_counter[keyword] += count

    return dict(topic_counter)


# ======================================================
# TOPIC DATAFRAME
# ======================================================

def create_topic_dataframe(topic_dict):
    """
    Convert topic dictionary to DataFrame.
    """

    if not topic_dict:
        return pd.DataFrame(
            columns=["Topic", "Frequency"]
        )

    df = pd.DataFrame(
        topic_dict.items(),
        columns=["Topic", "Frequency"]
    )

    df = df.sort_values(
        by="Frequency",
        ascending=False
    )

    df.reset_index(drop=True, inplace=True)

    return df


# ======================================================
# PROBABILITY CALCULATION
# ======================================================

def calculate_probability(df):
    """
    Calculate probability of topic appearing.
    """

    if df.empty:
        return df

    total = df["Frequency"].sum()

    df["Probability (%)"] = round(
        (df["Frequency"] / total) * 100,
        2
    )

    highest = df["Frequency"].max()

    df["Chance Score"] = round(
        (df["Frequency"] / highest) * 100,
        0
    )

    return df


# ======================================================
# QUESTION FREQUENCY
# ======================================================

def question_frequency(questions):
    """
    Count repeated questions.
    """

    counter = Counter(questions)

    df = pd.DataFrame(
        counter.items(),
        columns=[
            "Question",
            "Frequency"
        ]
    )

    df = df.sort_values(
        by="Frequency",
        ascending=False
    )

    df.reset_index(drop=True, inplace=True)

    return df


# ======================================================
# SEARCH QUESTIONS
# ======================================================

def search_questions(df, keyword):
    """
    Search questions using keyword.
    """

    if keyword == "":
        return df

    return df[
        df["Question"]
        .str.contains(
            keyword,
            case=False,
            na=False
        )
    ]


# ======================================================
# TOP QUESTIONS
# ======================================================

def top_questions(df, limit=10):
    """
    Return top repeated questions.
    """

    if df.empty:
        return df

    return df.head(limit)

# ======================================================
# utils.py (Part 2B)
# PassMate Pilot v2.0
# ======================================================

import io
import plotly.express as px


# ======================================================
# DASHBOARD METRICS
# ======================================================

def get_dashboard_metrics(
    total_questions,
    unique_questions,
    topic_df
):
    """
    Generate dashboard metrics.
    """

    metrics = {}

    metrics["total_questions"] = total_questions

    metrics["unique_questions"] = unique_questions

    if topic_df.empty:

        metrics["top_topic"] = "-"

        metrics["top_topic_frequency"] = 0

    else:

        metrics["top_topic"] = topic_df.iloc[0]["Topic"]

        metrics["top_topic_frequency"] = int(
            topic_df.iloc[0]["Frequency"]
        )

    return metrics


# ======================================================
# STUDY PLAN
# ======================================================

def generate_study_plan(
    topic_df,
    days
):
    """
    Generate day-wise study planner.
    """

    if topic_df.empty:

        return []

    topics = topic_df["Topic"].tolist()

    plan = []

    total_topics = len(topics)

    for day in range(days):

        topic = topics[day % total_topics]

        plan.append(

            {

                "Day": day + 1,

                "Topic": topic

            }

        )

    return plan


# ======================================================
# EXPORT CSV
# ======================================================

def dataframe_to_csv(df):

    return df.to_csv(

        index=False

    ).encode("utf-8")


# ======================================================
# WORD CLOUD DATA
# ======================================================

def create_word_frequency(topic_dict):

    return topic_dict


# ======================================================
# PLOTLY BAR CHART
# ======================================================

def create_bar_chart(topic_df):

    if topic_df.empty:

        return None

    fig = px.bar(

        topic_df.head(10),

        x="Topic",

        y="Frequency",

        title="Top Important Topics",

        text="Frequency"

    )

    fig.update_layout(

        template="plotly_dark",

        height=450

    )

    return fig


# ======================================================
# PIE CHART
# ======================================================

def create_pie_chart(topic_df):

    if topic_df.empty:

        return None

    fig = px.pie(

        topic_df,

        values="Frequency",

        names="Topic",

        title="Topic Distribution"

    )

    fig.update_layout(

        template="plotly_dark"

    )

    return fig


# ======================================================
# CONFIDENCE SCORE
# ======================================================

def calculate_confidence(topic_df):

    if topic_df.empty:

        return 0

    score = round(

        topic_df["Chance Score"].mean(),

        2

    )

    return score


# ======================================================
# ANALYSIS SUMMARY
# ======================================================

def generate_summary(

    subject,

    total_questions,

    unique_questions,

    confidence

):

    summary = f"""

Subject Detected : {subject}

Total Questions : {total_questions}

Unique Questions : {unique_questions}

Prediction Confidence : {confidence} %

Recommendation :

Focus on repeated topics first.

Study high probability questions.

Revise previous year papers thoroughly.

"""

    return summary


# ======================================================
# END OF utils.py
# ======================================================
