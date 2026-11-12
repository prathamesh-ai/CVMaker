---
name: tailor-content
description: "Uses LLM to rephrase CV JSON content to align with Job Description terminology. Adjusts summary, experience bullets, and skill ordering without adding new facts."
---

# Tailor Content

## Overview

This prompt skill uses the agent's LLM to intelligently adapt CV content for a specific Job Description. It updates the JSON data to better match JD keywords and terminology.

## Input Files

1. `output/cv_data.json` - Raw CV data extracted by parse-cv
2. `output/jd.txt` - Job Description text

## Instructions

### Step 1: Read Input Files

Use the read_file tool to read:
- `output/cv_data.json` - contains the raw CV structured data
- `output/jd.txt` - contains the job description text

### Step 2: Analyze Job Description

Extract key requirements from the JD:
1. Technical skills and tools mentioned
2. Keywords that appear frequently
3. Required vs preferred qualifications
4. Industry-specific terminology

### Step 3: Transform CV Content

Using the LLM, rephrase the CV content to:

1. **Summary**: Rewrite the professional summary to highlight JD-relevant skills and experience
2. **Skills**: Reorder skill categories and items to prioritize JD-relevant skills first
3. **Experience Bullets**: Rephrase job descriptions using JD terminology while preserving original facts
   - Replace generic terms with specific JD keywords where applicable
   - Highlight achievements that match JD requirements

### Step 4: Write Output

Save the tailored JSON to `output/cv_data_tailored.json` using the write_file tool.

## Strict Constraints

- **DO NOT invent new facts** - Only rephrase existing content
- **DO NOT add new technologies** - Use only what exists in the original CV
- **DO NOT change job titles or company names**
- **Preserve all dates, metrics, and specific achievements**
- **Maintain truthful representation** of the candidate's experience

## JSON Format

The output JSON must maintain the same structure as the input:
```json
{
  "name": "...",
  "phone": "...",
  "location": "...",
  "email": "...",
  "linkedin_url": "...",
  "linkedin_display": "...",
  "website_url": "...",
  "website_display": "...",
  "summary": "...",
  "education": [...],
  "skills": [...],
  "experience": [...],
  "projects": [...],
  "activities": [...],
  "leadership": [...]
}
```

## Notes

- If no JD file exists (path `output/jd.txt` is missing), skip this skill and use the raw CV data from `output/cv_data.json`
- Always preserve the original meaning and facts of the CV
- Use professional rephrasing appropriate for ATS systems