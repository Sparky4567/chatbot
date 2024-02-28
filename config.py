# ========== MAIN SETTINGS ==========
SIMILARITY_SCORE = 75
USE_TRANSLATION_SERVICE = False
SPEAK_BACK = False

# ========== VOICE INPUT ==========

# ========== DEFAULT SETTING: MICROPHONE OFF ==========

USE_VOICE_INPUT = False

# ========== DEFAULT SETTING: FALSE, DOES NOT REQUIRE TO PRESS R KEY EVERYTIME ==========

CONTINUOUS_LEARNING = False

# ========== VOICE RECOGNITION ==========


# ========== DEFAULT USAGE: POCKET SPHINX ==========


ENABLE_OFFLINE_RECOGNITION = False

# ========== DEFAULT MICROPHONE TIMEOUT IN SECONDS ==========

DEFAULT_MIC_TIMEOUT = 10

# ========== PREDEFINED COMMANDS USAGE ==========

USE_PREDEFINED_COMMANDS = True


# ========== AN ENDPOINT TO CONNECT WHITE RABBOT AND LOCAL LLM INSTANCES ==========

DEFAULT_LLM_URL = "http://localhost:11434/api/generate"


# ========== DATABASE LOCATION ==========

DEFAULT_DB = "database/db.db"


# ========== PDF DIRECTORY ==========


DEFAULT_PDF_FOLDER = "pdf/"

# ========== AUTOCOMPLETION LIST ==========


AUTOCOMPLETION_LIST = [
                        "open browser",
                        "open new browser tab",
                        "open gpt",
                        "open giphy",
                        "open terminal",
                        "open thunderbird",
                        "open obsidian",
                        "open cheese",
                        "open calculator",
                        "open office application",
                        "open vs code",
                        "go to store",
                        "list directory",
                        "search youtube for",
                        "search google for",
                        "search giphy for",
                        "ask llm",
                        "read pdf"
                       ]