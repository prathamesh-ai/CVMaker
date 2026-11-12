---
name: parse-cv
description: "Extract and parse content from PDF or DOCX resume files. Outputs structured JSON compatible with LaTeX resume template."
allowed_tools: [execute]
---

# Parse CV

## Overview

This skill extracts content from PDF or DOCX resume files and transforms them into structured JSON format suitable for LaTeX resume template population.

## Instructions (CRITICAL)

### Step 1: Execute the Tool (REQUIRED)

You MUST run the parse-cv tool via shell command. DO NOT try to parse the PDF manually:

```bash
python skills/active/parse-cv/tools/main.py <input_path> output/cv_data.json
```

Example:
```bash
python skills/active/parse-cv/tools/main.py input/resume.pdf output/cv_data.json
```

With JD (for copying to output directory):
```bash
python skills/active/parse-cv/tools/main.py input/resume.pdf output/cv_data.json input/jd.txt
```

### Output

1. The JSON will be written to: `output/cv_data.json`
2. If JD provided, copy to: `output/jd.txt`

## JSON Format

The output JSON must follow this structure:

```json
{
  "name": "Full Name",
  "phone": "+1 234 567 8900",
  "location": "City, State",
  "email": "email@example.com",
  "linkedin_url": "https://linkedin.com/in/username",
  "linkedin_display": "linkedin.com/in/username",
  "website_url": "",
  "website_display": "",
  "summary": "Professional summary...",
  "education": [
    {"degree": "Degree Name", "institution": "University Name", "duration": "2020", "details": "CGPA: 3.8"}
  ],
  "skills": [
    {"category": "Programming", "items": "Python, Java, C"}
  ],
  "experience": [
    {
      "position": "Job Title",
      "company": "Company Name",
      "duration": "Jan 2020 - Present",
      "location": "City, State",
      "description": ["Bullet point 1", "Bullet point 2"]
    }
  ],
  "projects": [],
  "activities": [],
  "leadership": []
}
```

## Notes

- Uses LLM (via OpenRouter) for intelligent CV extraction
- Groups skills by category when possible
- Optional sections (projects, activities, leadership) default to empty arrays
- Use the execute tool to run the Python script