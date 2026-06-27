"""
PassMate Pilot Pro v3.0
AI Engine (Gemini Integration)
"""

import os
import time
import google.generativeai as genai


class GeminiEngine:
    def __init__(self, language="English", temperature=0.3, max_tokens=2048):
        self.language = language
        self.temperature = temperature
        self.max_tokens = max_tokens

        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            try:
                import streamlit as st
                self.api_key = st.secrets["GEMINI_API_KEY"]
            except:
                self.api_key = None

        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-pro")

    def _generate(self, prompt: str) -> str:
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
                time.sleep(2)
                last_error = str(e)

        return f"Error: {last_error}"

    def generate(self, text: str, task: str) -> str:
        base = f"Respond in {self.language}. Use clear exam format.\n\nTEXT:\n{text}\n\n"

        prompts = {
            "summary": base + "Summarize notes in bullet points.",
            "questions": base + "Generate 15 important exam questions.",
            "quiz": base + "Create 10 MCQs with options A-D.",
            "flashcards": base + "Create term -> definition flashcards.",
            "study_plan": base + "Create a 7-day study plan.",
        }

        if task not in prompts:
            return "Invalid task"

        return self._generate(prompts[task])

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
