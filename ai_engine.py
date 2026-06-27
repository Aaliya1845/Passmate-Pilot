"""
PassMate Pilot Pro v3.0
AI Engine (Gemini Integration)
"""

from __future__ import annotations

import os
import time
from typing import Optional

import google.generativeai as genai


class GeminiEngine:
    """
    Wrapper around Google Gemini API for all AI operations:
    - Summary generation
    - Question generation
    - Quiz creation
    - Flashcards
    - Study plans
    """

    def __init__(
        self,
        language: str = "English",
        temperature: float = 0.3,
        max_tokens: int = 2048,
    ):
        self.language = language
        self.temperature = temperature
        self.max_tokens = max_tokens

        # Load API key from environment / Streamlit secrets
        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            try:
                import streamlit as st
                self.api_key = st.secrets["GEMINI_API_KEY"]
            except Exception:
                self.api_key = None

        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. Add it to environment or Streamlit secrets."
            )

        genai.configure(api_key=self.api_key)

        # Use Gemini model
        self.model = genai.GenerativeModel("gemini-1.5-pro")

    # ---------------------------------------------------
    # Internal helper
    # ---------------------------------------------------

    def _generate(self, prompt: str) -> str:
        """
        Core generation method with retry logic.
        """

        for attempt in range(3):
            try:
                response = self.model.generate_content(
                    prompt,
                    generation_config={
                        "temperature": self.temperature,
                        "max_output_tokens": self.max_tokens,
                    },
                )

                return response.text

            except Exception as e:
                if attempt == 2:
                    return f"Error generating response: {str(e)}"

                time.sleep(2)

          """
PassMate Pilot Pro v3.0
AI Engine (Gemini Integration) - Part 2
"""

from typing import List


class
    # -----------------------------
    # PROMPT HELPERS
    # -----------------------------

    def _lang(self) -> str:
        return self.language

    def _base_instruction(self) -> str:
        return (
            f"Respond ONLY in {self.language}. "
            "Keep output clear, structured, and student-friendly. "
            "Use bullet points, headings, and short explanations where needed."
        )

    def _context_block(self, text: str) -> str:
        return f"""
You are an expert exam preparation assistant.

{self._base_instruction()}

STUDENT NOTES:
----------------
{text}
----------------
"""

    # -----------------------------
    # PROMPT TEMPLATES
    # -----------------------------

    def _summary_prompt(self, text: str) -> str:
        return self._context_block(text) + """
Task: Create a concise, high-quality exam revision summary.

Rules:
- Keep it short but complete
- Use bullet points
- Highlight key concepts
- Avoid unnecessary explanation
"""

    def _questions_prompt(self, text: str) -> str:
        return self._context_block(text) + """
Task: Generate IMPORTANT EXAM QUESTIONS.

Rules:
- Provide 10–20 questions
- Mix short + long answer types
- Focus on frequently asked exam topics
- Do NOT provide answers
Format clearly as a numbered list.
"""

    def _quiz_prompt(self, text: str) -> str:
        return self._context_block(text) + """
Task: Create a multiple-choice quiz.

Rules:
- 10 MCQs
- 4 options each (A, B, C, D)
- Mark correct answer clearly
- Cover key concepts from notes
"""

    def _flashcards_prompt(self, text: str) -> str:
        return self._context_block(text) + """
Task: Create FLASHCARDS for revision.

Rules:
- Format: Term -> Simple explanation
- 15–25 flashcards
- Keep answers short and easy
"""

    def _study_plan_prompt(self, text: str) -> str:
        return self._context_block(text) + """
Task: Create a STUDY PLAN.

Rules:
- Divide into daily schedule (7 days or custom revision plan)
- Include revision strategy
- Prioritize important topics first
"""

    # -----------------------------
    # HIGH LEVEL DISPATCHER
    # -----------------------------

    def generate(self, text: str, task: str) -> str:
        """
        Unified entry point for all AI tasks.
        """

        if task == "summary":
            prompt = self._summary_prompt(text)

        elif task == "questions":
            prompt = self._questions_prompt(text)

        elif task == "quiz":
            prompt = self._quiz_prompt(text)

        elif task == "flashcards":
            prompt = self._flashcards_prompt(text)

        elif task == "study_plan":
            prompt = self._study_plan_prompt(text)

        else:
            return "Invalid task selected."

        return self._generate(prompt)

  """
PassMate Pilot Pro v3.0
AI Engine (Gemini Integration) - Part 3 (Final)
"""

from typing import Optional

    # -----------------------------
    # PUBLIC METHODS (USED BY APP)
    # -----------------------------

    def get_summary(self, text: str) -> str:
        if not text:
            return "No input text found."
        return self.generate(text, "summary")

    def get_questions(self, text: str) -> str:
        if not text:
            return "No input text found."
        return self.generate(text, "questions")

    def get_quiz(self, text: str) -> str:
        if not text:
            return "No input text found."
        return self.generate(text, "quiz")

    def get_flashcards(self, text: str) -> str:
        if not text:
            return "No input text found."
        return self.generate(text, "flashcards")

    def get_study_plan(self, text: str) -> str:
        if not text:
            return "No input text found."
        return self.generate(text, "study_plan")

    # -----------------------------
    # OPTIONAL: HEALTH CHECK
    # -----------------------------

    def test_connection(self) -> str:
        """
        Quick test to verify Gemini is working.
        """
        try:
            return self._generate("Say 'Gemini AI is working' in one line.")
        except Exception as e:
            return f"Connection failed: {str(e)}"
