import os
import time
import streamlit as st
import google.generativeai as genai


class GeminiEngine:
    def __init__(self, language="English", temperature=0.4, max_tokens=2048):

        self.language = language
        self.temperature = temperature
        self.max_tokens = max_tokens

        # API KEY
        self.api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

        if not self.api_key:
            st.error("Missing GEMINI_API_KEY")
            st.stop()

        genai.configure(api_key=self.api_key)

        # safe model (no hardcoding risk)
        self.model = genai.GenerativeModel("gemini-1.5-flash-latest")

    # ---------------------------------------------------
    # SAFE + CACHE + QUOTA OPTIMIZED GENERATION
    # ---------------------------------------------------
    def _generate(self, prompt: str):

        cache_key = f"cache_{hash(prompt)}"

        # CACHE HIT
        if cache_key in st.session_state:
            return st.session_state[cache_key]

        last_error = None

        for _ in range(2):
            try:
                response = self.model.generate_content(
                    prompt,
                    generation_config={
                        "temperature": self.temperature,
                        "max_output_tokens": self.max_tokens,
                    },
                )

                result = response.text

                # SAVE CACHE
                st.session_state[cache_key] = result

                return result

            except Exception as e:
                last_error = str(e)
                time.sleep(1)

        return f"Error: {last_error}"

    # ---------------------------------------------------
    # PROMPTS
    # ---------------------------------------------------
    def generate(self, text, task):

        base = f"""
Respond ONLY in {self.language}.
Use clear exam-friendly formatting.

CONTENT:
{text}
"""

        prompts = {
            "summary": base + "\nSummarize in bullet points.",
            "questions": base + "\nGenerate important exam questions.",
            "quiz": base + "\nCreate MCQ quiz with answers.",
            "flashcards": base + "\nCreate flashcards (term → meaning).",
            "study_plan": base + "\nCreate 7-day study plan.",
        }

        return self._generate(prompts.get(task, base))

    # ---------------------------------------------------
    # METHODS
    # ---------------------------------------------------
    def get_summary(self, text): return self.generate(text, "summary")
    def get_questions(self, text): return self.generate(text, "questions")
    def get_quiz(self, text): return self.generate(text, "quiz")
    def get_flashcards(self, text): return self.generate(text, "flashcards")
    def get_study_plan(self, text): return self.generate(text, "study_plan")
