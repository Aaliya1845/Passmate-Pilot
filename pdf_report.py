"""
PassMate Pilot Pro v3.0
PDF Report Generator
"""

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from datetime import datetime


# ---------------------------------------------------
# MAIN REPORT GENERATOR
# ---------------------------------------------------

def generate_pdf_report(
    filename: str,
    summary: str,
    questions: str,
    quiz: str,
    flashcards: str,
    study_plan: str,
):
    """
    Generates a full AI study report PDF.
    """

    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()

    content = []

    # ---------------------------------------------------
    # TITLE
    # ---------------------------------------------------

    title = Paragraph(
        f"<b>PassMate Pilot Pro Report</b><br/>Generated: {datetime.now()}",
        styles["Title"],
    )

    content.append(title)
    content.append(Spacer(1, 12))

    # ---------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------

    content.append(Paragraph("<b>1. Summary</b>", styles["Heading2"]))
    content.append(Spacer(1, 6))
    content.append(Paragraph(summary or "No summary available.", styles["BodyText"]))
    content.append(PageBreak())

    # ---------------------------------------------------
    # IMPORTANT QUESTIONS
    # ---------------------------------------------------

    content.append(Paragraph("<b>2. Important Questions</b>", styles["Heading2"]))
    content.append(Spacer(1, 6))
    content.append(Paragraph(questions or "No questions available.", styles["BodyText"]))
    content.append(PageBreak())

    # ---------------------------------------------------
    # QUIZ
    # ---------------------------------------------------

    content.append(Paragraph("<b>3. Quiz</b>", styles["Heading2"]))
    content.append(Spacer(1, 6))
    content.append(Paragraph(quiz or "No quiz available.", styles["BodyText"]))
    content.append(PageBreak())

    # ---------------------------------------------------
    # FLASHCARDS
    # ---------------------------------------------------

    content.append(Paragraph("<b>4. Flashcards</b>", styles["Heading2"]))
    content.append(Spacer(1, 6))
    content.append(Paragraph(flashcards or "No flashcards available.", styles["BodyText"]))
    content.append(PageBreak())

    # ---------------------------------------------------
    # STUDY PLAN
    # ---------------------------------------------------

    content.append(Paragraph("<b>5. Study Plan</b>", styles["Heading2"]))
    content.append(Spacer(1, 6))
    content.append(Paragraph(study_plan or "No study plan available.", styles["BodyText"]))

    # ---------------------------------------------------
    # BUILD PDF
    # ---------------------------------------------------

    doc.build(content)

    return filename
