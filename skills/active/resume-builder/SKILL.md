---
name: resume-builder
description: "Transform raw CV files into ATS-friendly PDF resumes. Orchestrates: parse-cv -> generate-latex -> compile-pdf. With optional JD tailoring via tailor-content."
allowed_tools: [execute]
---

# Resume Builder Orchestration

You are responsible for the end-to-end transformation of a CV into a professional ATS-friendly PDF resume.

## Sequence

1. **Extract**: Use `parse-cv` to convert the input file into a structured JSON object.
2. **Tailor (Conditional)**: 
   - If the user provided a Job Description, invoke `tailor-content` to update the JSON's `summary`, `experience` bullets, and `skills` order to match the JD.
3. **Generate**: Use `generate-latex` to populate the `templates/classic/resume.tex` with the final JSON data.
4. **Compile**: Use `compile-pdf` to produce the final document.

## Workflow Details

### Step 1: Parse CV
- Input: PDF or DOCX resume file path
- Output: JSON at `output/cv_data.json`
- Tool: `python skills/active/parse-cv/tools/main.py <input_path> output/cv_data.json`
- If JD provided: Copy JD to `output/jd.txt`

### Step 2: Tailor Content (Conditional)
- Trigger: Only when JD file exists at `output/jd.txt`
- Input: `output/cv_data.json` and `output/jd.txt`
- Output: Tailored JSON at `output/cv_data_tailored.json`
- Read the `tailor-content` SKILL.md for detailed instructions
- Agent uses LLM to rephrase content matching JD terminology

### Step 3: Generate LaTeX
- Input: Check for `output/cv_data_tailored.json` first, else `output/cv_data.json`
- Output: LaTeX file at `output/resume.tex`
- Tool: `python skills/active/generate-latex/tools/main.py <json_path> skills/active/generate-latex/templates/classic/resume.tex output/resume.tex`
- Copy resume.cls to output directory if needed for compilation

### Step 4: Compile PDF
- Input: `output/resume.tex` and `output/resume.cls`
- Output: Final PDF at `output/resume.pdf`
- Tool: `python skills/active/compile-pdf/tools/main.py output/resume.tex output/resume.pdf`
- Requires Docker image `resume-compiler-minimal`

## Output

Final resume is at: `output/resume.pdf`

## Notes

- Always check if JD file exists before invoking tailor-content
- Use the execute tool to run Python scripts for each step
- Ensure resume.cls is available for LaTeX compilation
- The resume can be opened in any PDF viewer or submitted to ATS systems