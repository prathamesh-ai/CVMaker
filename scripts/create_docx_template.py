#!/usr/bin/env python3
"""
Script to create the DOCX resume template with Jinja2 placeholders.
Run this once to generate the template.
"""
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn

def create_resume_template():
    doc = Document()

    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(11)

    # TITLE - Name
    title = doc.add_heading('', level=0)
    run = title.add_run('{{ name }}')
    run.bold = True
    run.font.size = Pt(22)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Contact info - single line with pipes
    contact_para = doc.add_paragraph()
    contact_parts = []
    if email:
        contact_parts.append('{{ email }}')
    if phone:
        contact_parts.append('{{ phone }}')
    if location:
        contact_parts.append('{{ location }}')
    if linkedin:
        contact_parts.append('{{ linkedin }}')
    if github:
        contact_parts.append('{{ github }}')

    contact_run = contact_para.add_run(' | '.join(contact_parts))
    contact_run.font.size = Pt(10)
    contact_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph()

    # Summary Section
    add_section_heading(doc, 'Professional Summary')
    summary_para = doc.add_paragraph('{{ summary }}')
    doc.add_paragraph()

    # Education Section
    add_section_heading(doc, 'Education')
    # Jinja2 loop for education
    edu_para = doc.add_paragraph('{% for edu in education %}')
    edu_para.runs[0].font.italic = True
    doc.add_paragraph('{{ edu.institution }} - {{ edu.degree }} ({{ edu.year }})')
    doc.add_paragraph('{% endfor %}')
    doc.add_paragraph()

    # Skills Section
    add_section_heading(doc, 'Skills')
    skills_para = doc.add_paragraph('{{ skills | join(", ") }}')
    doc.add_paragraph()

    # Experience Section
    add_section_heading(doc, 'Experience')
    # Jinja2 loop for experience
    exp_para = doc.add_paragraph('{% for job in experience %}')
    exp_para.runs[0].font.italic = True

    # Job title + company
    job_title = doc.add_paragraph()
    job_title_run = job_title.add_run('{{ job.position }}')
    job_title_run.bold = True

    job_company = job_title.add_run(' at {{ job.company }}')
    job_company.italic = True
    job_title_run2 = job_title.add_run(' | {{ job.duration }}')

    # Job description bullets
    desc_para = doc.add_paragraph('{% for bullet in job.description %}')
    desc_para.runs[0].font.italic = True
    doc.add_paragraph('• {{ bullet }}')
    doc.add_paragraph('{% endfor %}')

    doc.add_paragraph('{% endfor %}')
    doc.add_paragraph()

    # Projects Section (optional)
    add_section_heading(doc, 'Projects')
    proj_para = doc.add_paragraph('{% for proj in projects %}')
    proj_para.runs[0].font.italic = True
    doc.add_paragraph('{{ proj.name }}')
    doc.add_paragraph('{{ proj.description }}')
    doc.add_paragraph('{% endfor %}')
    doc.add_paragraph()

    # Certifications Section (optional)
    add_section_heading(doc, 'Certifications')
    cert_para = doc.add_paragraph('{% for cert in certifications %}')
    cert_para.runs[0].font.italic = True
    doc.add_paragraph('• {{ cert }}')
    doc.add_paragraph('{% endfor %}')

    # Save template
    output_path = 'LatexCVMaker/skills/active/resume-builder/templates/classic/resume_base.docx'
    doc.save(output_path)
    print(f"Template created: {output_path}")

def add_section_heading(doc, text):
    heading = doc.add_heading(text, level=1)
    heading.runs[0].bold = True
    heading.runs[0].font.size = Pt(14)

if __name__ == '__main__':
    from pathlib import Path
    # Need to create with placeholders manually since Jinja2 in Word is tricky
    from docx import Document
    from docx.shared import Pt, Inches, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH

    doc = Document()

    # Name (centered, large)
    p = doc.add_paragraph()
    r = p.add_run('{{ name }}')
    r.bold = True
    r.font.size = Pt(22)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Contact line
    p2 = doc.add_paragraph()
    r2 = p2.add_run('{{ email }} | {{ phone }} | {{ location }} | {{ linkedin }} | {{ github }}')
    r2.font.size = Pt(10)
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph()

    # Summary heading
    h1 = doc.add_heading('Professional Summary', level=1)
    doc.add_paragraph('{{ summary }}')

    doc.add_paragraph()

    # Education heading
    h2 = doc.add_heading('Education', level=1)
    # Add template text for education loop
    edu_text = doc.add_paragraph('{% for edu in education %}{{ edu.institution }} - {{ edu.degree }} ({{ edu.year }}){% endfor %}')

    doc.add_paragraph()

    # Skills heading
    h3 = doc.add_heading('Skills', level=1)
    doc.add_paragraph('{{ skills | join(", ") }}')

    doc.add_paragraph()

    # Experience heading
    h4 = doc.add_heading('Experience', level=1)
    exp_text = doc.add_paragraph('{% for job in experience %}{{ job.position }} at {{ job.company }} ({{ job.duration }}){% for bullet in job.description %}• {{ bullet }}{% endfor %}{% endfor %}')

    doc.add_paragraph()

    # Projects heading
    h5 = doc.add_heading('Projects', level=1)
    proj_text = doc.add_paragraph('{% for proj in projects %}{{ proj.name }}: {{ proj.description }}{% endfor %}')

    doc.add_paragraph()

    # Certifications heading
    h6 = doc.add_heading('Certifications', level=1)
    cert_text = doc.add_paragraph('{% for cert in certifications %}• {{ cert }}{% endfor %}')

    # Save
    project_root = Path(__file__).parent.parent.resolve()
    output_path = project_root / 'skills/active/resume-builder/templates/classic/resume_base.docx'
    doc.save(str(output_path))
    print(f"Template created: {output_path}")
