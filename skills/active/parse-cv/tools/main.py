import json
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
load_dotenv()

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    from docx import Document
except ImportError:
    Document = None

try:
    from langchain_openrouter import ChatOpenRouter
except ImportError:
    ChatOpenRouter = None


def get_llm_client():
    """Get LLM client for structured extraction."""
    if ChatOpenRouter is None:
        return None
    api_key = __import__("os").getenv("OPENROUTER_API_KEY")
    if not api_key:
        return None
    return ChatOpenRouter(
        model="mistralai/mistral-small-2603",
        api_key=api_key
    )


def extract_from_pdf(file_path: str) -> str:
    if pdfplumber is None:
        raise ImportError("pdfplumber not installed")
    with pdfplumber.open(file_path) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    return text


def extract_from_docx(file_path: str) -> str:
    if Document is None:
        raise ImportError("python-docx not installed")
    doc = Document(file_path)
    text = "\n".join(p.text for p in doc.paragraphs if p.text)
    return text


def copy_jd_file(jd_path: str, output_path: str) -> bool:
    """Copy Job Description file to output directory."""
    jd_file = Path(jd_path)
    if not jd_file.exists():
        return False
    content = jd_file.read_text(encoding="utf-8")
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        f.write(content)
    return True


def parse_cv_with_llm(text: str) -> dict:
    """Use LLM to parse raw CV text into structured JSON."""
    client = get_llm_client()
    if not client:
        return None
    
    prompt = f"""Extract the following resume text into a structured JSON format for LaTeX resume template.

Resume text:
{text}

Return ONLY valid JSON (no markdown formatting) with this exact structure:
{{
  "name": "Full Name (extract from top of resume)",
  "phone": "+1 234 567 8900",
  "location": "City, State or Country",
  "email": "email@example.com",
  "linkedin_url": "https://linkedin.com/in/username or empty string",
  "linkedin_display": "linkedin.com/in/username or empty string",
  "website_url": "website URL or empty string",
  "website_display": "Display text or empty string",
  "summary": "2-3 sentence professional summary",
  "education": [
    {{"degree": "Degree Name and Major", "institution": "University Name", "duration": "2020", "details": "Notable achievements like CGPA, honors, or empty string"}}
  ],
  "skills": [
    {{"category": "Programming", "items": "Python, Java, C"}},
    {{"category": "ML/AI", "items": "TensorFlow, PyTorch, Scikit-learn"}},
    {{"category": "Databases", "items": "MySQL, PostgreSQL, MongoDB"}}
  ],
  "experience": [
    {{
      "position": "Job Title",
      "company": "Company Name",
      "duration": "Jan 2020 - Present",
      "location": "City, State",
      "description": ["Bullet point 1", "Bullet point 2", "Bullet point 3"]
    }}
  ],
  "projects": [],
  "activities": [],
  "leadership": []
}}

Requirements:
- Group skills by category (Programming, ML/AI, Databases, Cloud, Tools, etc.)
- Extract 3-5 bullet points per job from the description
- Include all education entries with years/dates
- Use empty arrays [] for optional sections if not present in resume
- For any missing fields, use empty strings or empty arrays"""

    try:
        response = client.invoke([{"role": "user", "content": prompt}])
        content = response.content if hasattr(response, 'content') else str(response)
        
        import re
        json_match = re.search(r'\{[\s\S]*\}', content)
        if json_match:
            result = json.loads(json_match.group())
            # Ensure all required fields exist
            required_fields = [
                "name", "phone", "location", "email",
                "linkedin_url", "linkedin_display", "website_url", "website_display",
                "summary", "education", "skills", "experience",
                "projects", "activities", "leadership"
            ]
            for field in required_fields:
                if field not in result:
                    result[field] = "" if field in ["name", "phone", "location", "email",
                        "linkedin_url", "linkedin_display", "website_url", "website_display", "summary"] else []
            return result
    except Exception as e:
        print(f"LLM parsing failed: {e}", file=sys.stderr)
    
    return None


def parse_cv(input_path: str, output_path: str, jd_path: str = None) -> dict:
    """Parse CV file and extract structured JSON."""
    path = Path(input_path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    ext = path.suffix.lower()
    if ext == ".pdf":
        text = extract_from_pdf(input_path)
    elif ext == ".docx":
        text = extract_from_docx(input_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    # Try LLM-based parsing first
    structured = parse_cv_with_llm(text)
    
    # Fallback to empty structure if LLM fails
    if not structured:
        structured = {
            "name": "",
            "phone": "",
            "location": "",
            "email": "",
            "linkedin_url": "",
            "linkedin_display": "",
            "website_url": "",
            "website_display": "",
            "summary": "",
            "education": [],
            "skills": [],
            "experience": [],
            "projects": [],
            "activities": [],
            "leadership": []
        }

    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(structured, f, indent=2)

    if jd_path:
        jd_output = Path(output_path).parent / "jd.txt"
        copy_jd_file(jd_path, str(jd_output))

    return structured


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "input/resume.pdf"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output/cv_data.json"
    jd_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    result = parse_cv(input_file, output_file, jd_file)
    print(f"Parsed: {result.get('name', 'Unknown')}")