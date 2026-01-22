import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    PROMPT_PATH = os.getenv("PROMPT", "app/prompts/few_shot.txt")
    PICKLIST_PATH = os.getenv("PICKLIST_PATH", "app/data/picklist.json")
    AGENT_MODEL = "gemini-3-flash-preview"


settings = Settings()