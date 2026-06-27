"""
PassMate Pilot Pro v3.0
Central Configuration File
"""

# ---------------------------------------------------
# APP METADATA
# ---------------------------------------------------

APP_NAME = "PassMate Pilot Pro"
APP_ICON = "📘"
APP_VERSION = "3.0.0"

# ---------------------------------------------------
# FILE LIMITS
# ---------------------------------------------------

MAX_FILE_SIZE_MB = 10

# ---------------------------------------------------
# DEFAULT SETTINGS
# ---------------------------------------------------

DEFAULT_LANGUAGE = "English"

DEFAULT_TEMPERATURE = 0.3
DEFAULT_MAX_TOKENS = 2048

# ---------------------------------------------------
# AI SETTINGS
# ---------------------------------------------------

GEMINI_MODEL = "gemini-1.5-pro"

RETRY_ATTEMPTS = 3
RETRY_DELAY_SECONDS = 2

# ---------------------------------------------------
# UI SETTINGS
# ---------------------------------------------------

SIDEBAR_WIDTH = 300

THEME_PRIMARY_COLOR = "#4F46E5"

# ---------------------------------------------------
# FEATURES TOGGLE (FOR SCALING LATER)
# ---------------------------------------------------

ENABLE_FLASHCARDS = True
ENABLE_QUIZ = True
ENABLE_STUDY_PLAN = True
ENABLE_PDF_EXPORT = True

# ---------------------------------------------------
# SESSION SETTINGS
# ---------------------------------------------------

MAX_HISTORY_ITEMS = 20
