# Resume Agent

This agent transforms raw resume files (PDF/DOCX) into ATS-friendly PDF resumes using LaTeX templates and DeepAgents SkillsMiddleware.

## Skills

The agent has access to the following skills through progressive disclosure:

### 1. parse-cv
Extracts and parses content from PDF or DOCX resume files, outputting structured JSON with Contact, Summary, Experience, Education, and Skills sections. Uses LLM for intelligent extraction.

### 2. tailor-content
Uses LLM to rephrase CV JSON content to align with Job Description terminology. Adjusts summary, experience bullets, and skill ordering without adding new facts. (Prompt Skill - no Python tool)

### 3. generate-latex
Converts structured CV JSON into a LaTeX document using Jinja2 templates and resume.cls class file.

### 4. compile-pdf
Compiles LaTeX .tex files into ATS-friendly PDF documents using Docker/pdflatex.

## Workflow

```
Input (PDF/DOCX) + JD (optional) --> parse-cv --> tailor-content (if JD) --> generate-latex --> compile-pdf --> Output (PDF)
```

## Usage

```python
from agents.resume_agent import ResumeAgent

agent = ResumeAgent()
# Without JD
result = agent.process("input/resume.pdf", "output/resume.pdf")

# With JD for ATS tailoring
result = agent.process("input/resume.pdf", "output/resume.pdf", "input/jd.txt")
```
Input (PDF/DOCX) + JD (optional) --> parse-cv --> generate-docx --> Output (DOCX)
```

The user can save the final DOCX as PDF from Microsoft Word if needed.

## Usage

```python
from agents.resume_agent import ResumeAgent

agent = ResumeAgent()
# Without JD
result = agent.process("input/resume.pdf", "output/resume.docx")

# With JD for ATS tailoring
result = agent.process("input/resume.pdf", "output/resume.docx", "input/jd.txt")
```