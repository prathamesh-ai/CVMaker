from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()

SKILLS_DIR = PROJECT_ROOT / "skills" / "active" / "resume-builder"
TEMPLATES_DIR = SKILLS_DIR / "templates"
INPUT_DIR = PROJECT_ROOT / "input"
OUTPUT_DIR = PROJECT_ROOT / "output"

DEFAULT_MODEL = "mistralai/mistral-small-3.1"
API_PROVIDER = "openrouter"

OUTPUT_FILENAME = "resume.pdf"
INTERMEDIATE_JSON = "cv_data.json"
INTERMEDIATE_TEX = "resume.tex"