import json
import sys
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

try:
    from langchain_openrouter import ChatOpenRouter
except ImportError:
    ChatOpenRouter = None


def get_llm_client():
    if ChatOpenRouter is None:
        return None
    api_key = __import__("os").getenv("OPENROUTER_API_KEY")
    if not api_key:
        return None
    return ChatOpenRouter(
        model="mistralai/mistral-small-2603",
        api_key=api_key
    )


def analyze_gaps(cv_data: dict, jd_text: str) -> str:
    client = get_llm_client()
    if not client:
        return "Error: LLM client not available"

    experience = cv_data.get("experience", [])
    skills = cv_data.get("skills", [])

    experience_text = "\n".join([
        f"- {job.get('position', '')} at {job.get('company', '')}: {'; '.join(job.get('description', []))}"
        for job in experience
    ]) if experience else "No experience listed"

    skills_text = "\n".join([
        f"- {s.get('category', '')}: {s.get('items', '')}"
        for s in skills
    ]) if skills else "No skills listed"

    prompt = f"""You are a career strategist. Analyze the following resume experience and job description to identify gaps.

RESUME EXPERIENCE:
{experience_text}

RESUME SKILLS:
{skills_text}

JOB DESCRIPTION:
{jd_text}

Your task is to produce a strategic gap analysis report with the following sections:

## GAP ANALYSIS & RECOMMENDATIONS

### 1. UNDERSOLD SKILLS
Identify where the candidate has relevant experience but uses different terminology than the JD. The JD uses specific high-impact keywords that the resume should mirror.

### 2. MISSING EVIDENCE  
Identify JD requirements that have NO supporting evidence in the resume experience section.

### 3. TARGETED REVISIONS (3-5 specific suggestions)
For each suggestion, provide:
- **Job/Role**: Which position in the resume this applies to
- **Current Bullet**: The actual bullet point from resume
- **Suggested Revision**: How to rewrite it to better align with JD keywords
- **JD Keyword**: The keyword/reason from JD that this addresses

Be specific and actionable. Focus on quantifiable achievements and JD-aligned terminology."""

    try:
        response = client.invoke([{"role": "user", "content": prompt}])
        content = response.content if hasattr(response, 'content') else str(response)
        return content
    except Exception as e:
        return f"Error during analysis: {str(e)}"


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: main.py <cv_json_path> <jd_path> <output_report_path>")
        sys.exit(1)

    cv_json_path = sys.argv[1]
    jd_path = sys.argv[2]
    output_path = sys.argv[3]

    with open(cv_json_path, 'r', encoding='utf-8') as f:
        cv_data = json.load(f)

    jd_text = Path(jd_path).read_text(encoding='utf-8')

    report = analyze_gaps(cv_data, jd_text)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(report, encoding='utf-8')

    print(f"Gap analysis saved to: {output_path}")