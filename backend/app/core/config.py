import os
from pathlib import Path
from dotenv import load_dotenv

# Points to the .env file inside the backend folder
# Structure: backend/app/core/config.py -> parent(core) -> parent(app) -> parent(backend)
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class Settings:
    # Retrieve keys and strip any accidental whitespace or hidden characters
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "").strip()
    
    # Official endpoint for the Gemini 1.5 Flash model
    GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    OPENAI_URL = "https://api.openai.com/v1/chat/completions"

settings = Settings()

# --- Debugging Logs (Visible in your Terminal on startup) ---
if settings.GEMINI_API_KEY:
    # Only prints the first 5 characters for security
    print(f"DEBUG: Gemini Key loaded: {settings.GEMINI_API_KEY[:5]}...") 
else:
    print("DEBUG: Gemini Key NOT found in .env! Check file path: " + str(env_path))

if settings.OPENAI_API_KEY:
    print(f"DEBUG: OpenAI Key loaded: {settings.OPENAI_API_KEY[:5]}...")