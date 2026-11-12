1. New Skill Structure
Following your project's directory logic, the new skill will be self-contained within the resume-builder hierarchy:

skills/active/resume-builder/skills/generate-docx/
├── SKILL.md              # Instructions and metadata for the agent
├── templates/
│   └── resume_base.docx  # The visual "skeleton" with Jinja2 tags
└── tools/
    └── main.py           # The Python logic to render the template

2. Implementation Steps
Step 1: Dependency Management
Add docxtpl to your project dependencies. This library allows you to use Jinja2-like syntax directly inside Microsoft Word documents.
pip install docxtpl

Step 2: The .docx Template (templates/resume_base.docx)
Create a standard Word document. Instead of static text, use placeholders that match your structured JSON keys.

Header: {{ name }}

Summary: {{ summary }}

Experience Loop:

{% for job in experience %}
{{ job.position }}, {{ job.company }} ({{ job.duration }})
{% for bullet in job.description %}

{{ bullet }}
{% endfor %}
{% endfor %}

Step 3: The Python Tool (tools/main.py)
This tool handles the mechanical "Search and Replace" operation, mapping the JSON attributes to your template.

import json
import os
from docxtpl import DocxTemplate

def run(json_data_path: str, output_path: str):
    """
    Renders a DOCX resume by injecting JSON data into a Word template.
    """
    # 1. Load the structured JSON extracted by the parse-cv skill
    with open(json_data_path, 'r') as f:
        data = json.load(f)

    # 2. Path to the template within the skill folder
    template_path = os.path.join(os.path.dirname(__file__), "../templates/resume_base.docx")
    
    # 3. Load and render
    doc = DocxTemplate(template_path)
    doc.render(data)
    
    # 4. Save to the output directory
    doc.save(output_path)
    return f"Successfully generated DOCX at {output_path}"

Step 4: The Agent Skill (SKILL.md)
This file defines the Progressive Disclosure instructions for your agent. It tells the agent when and how to trigger the tool.

---
name: generate-docx
description: Converts structured CV JSON into a professional ATS-friendly Word document.
tools:
  - name: generate_resume_docx
    description: Takes the path to a JSON file and returns a formatted .docx file.
---

# Instruction
When the `parse-cv` skill has successfully finished extracting the user's information into a JSON format, use this skill to populate the `resume_base.docx` template.

## Strategy
1. Locate the JSON file in the `output/` directory.
2. Trigger the `generate_resume_docx` tool.
3. Inform the user that their professional Word-based CV is ready for download.

3. Updated Workflow Integration
Your agent's orchestration pipeline will now be streamlined:

Input: User uploads a PDF/DOCX.

Step 1 (parse-cv): Extract details to resume.json.

Step 2 (generate-docx): Render resume.json into professional_resume.docx.

Output: Provide the .docx file directly to the user.