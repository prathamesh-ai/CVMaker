# ATS Resume Builder - Technical Documentation

## Overview

ATS Resume Builder is an intelligent agentic application that transforms raw CVs (PDF/DOCX) into ATS-friendly professional resumes. Built using DeepAgents framework with Anthropic's Agent Skills pattern.

---

## Architecture

```
LatexCVMaker/
├── engine/                          # Core engine components
│   ├── core/
│   │   ├── configs.py              # Configuration management
│   │   └── logger.py              # Logging utilities
│   ├── models/
│   │   └── llm.py                 # LLM client wrapper
│   └── constants.py               # Project constants
│
├── agents/
│   └── resume_agent/
│       ├── resume_agent.py         # Main agent definition
│       ├── agent.md                # Agent documentation
│       └── relative_skills_middleware.py  # Custom middleware
│
├── skills/
│   └── active/
│       └── resume-builder/          # Top-level skill
│           ├── SKILL.md           # Orchestration skill
│           ├── templates/
│           │   ├── modern/
│           │   └── classic/
│           └── skills/
│               ├── parse-cv/       # CV parsing skill
│               ├── generate-latex/
│               └── compile-pdf/
│
├── input/                          # Input files (PDF/DOCX)
├── output/                         # Generated files
└── scripts/
    └── run_agent.py               # CLI entry point
```

---

## Framework: DeepAgents

### What is DeepAgents?

DeepAgents is an agent harness built on LangChain/LangGraph that provides:
- **Tool calling** capabilities
- **Skills** (progressive disclosure pattern)
- **Filesystem middleware** for context management
- **Planning** and task decomposition

### Key Components

| Component | Purpose |
|-----------|---------|
| `create_deep_agent()` | Creates configurable deep agent |
| `FilesystemBackend` | Virtual filesystem for agent context |
| `SkillsMiddleware` | Loads and manages skills |
| `ChatOpenRouter` | Model integration via OpenRouter |

---

## Workflow

### Pipeline Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Input CV       │───▶│   Parse CV       │───▶│   Generate      │
│ (PDF/DOCX)      │    │ (Extract JSON)  │    │   Document      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                                
                        Step 1: parse-cv     Step 2: generate
                        
                        ↓                                          ↓
                        
┌──────────────────────────────────────────────────────────────────────┐
│                      AGENT ORCHESTRATION                           │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ 1. Read user input                                          │ │
│  │ 2. Trigger parse-cv skill → extract to JSON                  │ │
│  │ 3. Trigger generate-* skill → populate template            │ │
│  │ 4. Trigger compile-pdf skill → compile to PDF               │ │
│  └─────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────┘
```

### Detailed Flow

1. **User Input**
   - CV file path (PDF or DOCX)
   - Optional Job Description (.txt) for JD-aware tailoring

2. **Parse CV** (`parse-cv` skill)
   ```python
   # Extracts:
   {
     "contact": {"name", "email", "phone", "location", "linkedin", "github"},
     "summary": "...",
     "experience": [{"company", "position", "duration", "description"}],
     "education": [{"institution", "degree", "year"}],
     "skills": ["Skill1", "Skill2", ...]
   }
   ```

3. **Generate Document** (`generate-latex` skill)
   - Reads JSON data
   - Populates LaTeX template
   - JD-aware skill scoring
   - Outputs `.tex` file

4. **Compile PDF** (`compile-pdf` skill)
   - Runs pdflatex
   - Outputs final PDF

---

## Agent Skills Pattern

### What are Skills?

Skills follow Anthropic's **Agent Skills** pattern with **progressive disclosure**:

```
┌─────────────────────────────────────────────────────────────┐
│            PROGRESSIVE DISCLOSURE                         │
├─────────────────────────────────────────────────────────────┤
│ Level 1: Metadata (always loaded)                       │
│   - Skill name + description in system prompt            │
│ Level 2: Instructions (loaded when triggered)           │
│   - SKILL.md content                                  │
│ Level 3: Resources (loaded as needed)                 │
│   - tools/, templates/, docs/                         │
└─────────────────────────────────────────────────────┘
```

### Skill Structure

```
skill-name/
├── SKILL.md           # Instructions + metadata (YAML frontmatter)
├── tools/
│   └── main.py        # Executable code
├── templates/        # Optional templates
└── docs/            # Optional documentation
```

### Skills in This Application

| Skill | Purpose | Trigger |
|-------|---------|---------|
| `resume-builder` | Orchestration | Always |
| `parse-cv` | Extract CV to JSON | User submits CV |
| `generate-latex` | JSON → LaTeX | After parse-cv |
| `compile-pdf` | LaTeX → PDF | After generate |

---

## Agent Configuration

```python
from deepagents import create_deep_agent
from deepagents.backends.filesystem import FilesystemBackend
from langchain_openrouter import ChatOpenRouter

# Model: Mistral Small via OpenRouter
chat_model = ChatOpenRouter(
    model="mistralai/mistral-small-2603",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Backend: Filesystem for virtual file access
backend = FilesystemBackend(root_dir=PROJECT_ROOT)

# Create agent with skills
agent = create_deep_agent(
    model=chat_model,
    skills=[SKILLS_PATH],  # Points to skills/active/
    backend=backend,
)
```

---

## JD-Aware Processing

### Flow with Job Description

```
User CV + JD ──��� Parse CV ──▶ Generate (JD-aware) ──▶ Output

                     │
                     ▼
              ┌─────────────────┐
              │ JD Processing   │
              ├─────────────────┤
              │ 1. Extract JD   │
              │    keywords    │
              │ 2. Score CV    │
              │    skills      │
              │ 3. Reorder by   │
              │    match %     │
              │ 4. Rewrite    │
              │    summary     │
              └─────────────────┘
```

### Scoring Algorithm

```python
def score_skills(cv_skills, jd_keywords):
    for skill in cv_skills:
        if exact_match(skill, jd): score = 100%
        elif related_match(skill, jd): score = 70%
        elif domain_match(skill, jd): score = 50%
        else: score = 30%
```

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `deepagents` | Agent framework |
| `langchain-openrouter` | Model integration |
| `pdfplumber` | PDF extraction |
| `python-docx` | DOCX handling |
| `python-dotenv` | Configuration |

---

## Usage

### CLI

```bash
# Without JD
python scripts/run_agent.py input/resume.pdf -o output/resume.pdf

# With JD for tailoring
python scripts/run_agent.py input/resume.pdf -j input/jd.txt -o output/tailored_resume.pdf
```

### Python API

```python
from agents.resume_agent import ResumeAgent
from engine.core.configs import Config

Config.validate()
agent = ResumeAgent()
result = agent.process("input/resume.pdf", "output/resume.pdf", "input/jd.txt")
```

---

## Future Enhancements

1. **DOCX Output**: Generate Word documents directly (bypasses LaTeX)
2. **Docker**: Containerize for production
3. **Templates**: Add more professional templates
4. **Enhanced Scoring**: Improve JD matching algorithm

---

## Notes

- Model: `mistralai/mistral-small-2603` via OpenRouter
- Progressive disclosure minimizes context usage
- Skills can be extended by adding new `skills/` directories
- All transformations preserve original CV facts (no invented details)