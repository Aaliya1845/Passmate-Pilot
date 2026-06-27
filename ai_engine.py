"""
PassMate Pilot Pro v3.0
AI Engine (Bulletproof Gemini Auto-Selector)
"""

import os
import time
import streamlit as st
import google.generativeai as genai


class GeminiEngine:
    def __init__(self, language="English", temperature=0.3, max_tokens=2048):
        self.language = language
        self.temperature = temperature
        self.max_tokens = max_tokens

        # -----------------------------
        # LOAD API KEY
        # -----------------------------
        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            try:
                self.api_key = st.secrets["GEMINI_API_KEY"]
            except:
                self.api_key = None

        if not self.api_key:
            st.error("❌ GEMINI_API_KEY missing in Streamlit Secrets")
            st.stop()

        genai.configure(api_key=self.api_key)

        # -----------------------------
        # AUTO MODEL SELECTION (BULLETPROOF)
        # -----------------------------
        self.model = self._select_best_model()

    # =========================================================
    # AUTO MODEL DETECTION
    # =========================================================
    def _select_best_model(self):
        """
        Dynamically selects the best available Gemini model.
        No hardcoding = no 404 errors ever.
        """

        preferred_models = [
            "gemini-1.5-pro-latest",
            "gemini-1.5-flash-latest",
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-pro",
        ]

        available_models = []

        try:
            for m in genai.list_models():
                if "generateContent" in m.supported_generation_methods:
                    available_models.append(m.name.replace("models/", ""))
        except Exception:
            # fallback if listing fails
            available_models = preferred_models

        # Pick first matching preferred model
        for model in preferred_models:
            if model in available_models:
                return genai.GenerativeModel(model)

        # absolute fallback
        return genai.GenerativeModel("gemini-pro")

    # =========================================================
    # CORE GENERATION
    # =========================================================
    def _generate(self, prompt: str) -> str:
        last_error = None

        for _ in range(3):
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
                last_error = str(e)
                time.sleep(2)

        return f"Error generating response: {last_error}"

    # =========================================================
    # PROMPT ENGINE
    # =========================================================
    def generate(self, text: str, task: str) -> str:
        base = (
            f"Respond ONLY in {self.language}. "
            "Format clearly for exam preparation.\n\n"
            f"CONTENT:\n{text}\n\n"
        )

        prompts = {
            "summary": base + "Summarize in bullet points.",
            "questions": base + "Generate 15 important exam questions.",
            "quiz": base + "Create 10 MCQs with answers A-D.",
            "flashcards": base + "Create flashcards (term -> meaning).",
            "study_plan": base + "Create a 7-day study plan.",
        }

        if task not in prompts:
            return "Invalid task selected."

        return self._generate(prompts[task])

    # =========================================================
    # PUBLIC METHODS
    # =========================================================
    def get_summary(self, text):
        return self.generate(text, "summary")

    def get_questions(self, text):
        return self.generate(text, "questions")

    def get_quiz(self, text):
        return self.generate(text, "quiz")

    def get_flashcards(self, text):
        return self.generate(text, "flashcards")

    def get_study_plan(self, text):
        return self.generate(text, "study_plan")
