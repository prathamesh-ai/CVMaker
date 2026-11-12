import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()

class Config:
    PROJECT_ROOT = PROJECT_ROOT
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
    MODEL = os.getenv("MODEL", "mistralai/mistral-small-2603")
    
    SKILLS_PATH = str(PROJECT_ROOT / "skills" / "active")
    WORKSPACE_ROOT = str(PROJECT_ROOT)
    
    INPUT_DIR = PROJECT_ROOT / "input"
    OUTPUT_DIR = PROJECT_ROOT / "output"
    
    TEMPLATES_DIR = str(PROJECT_ROOT / "skills" / "active" / "resume-builder" / "templates")
    
    @classmethod
    def validate(cls):
        if not cls.OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY not set in environment")
        return True