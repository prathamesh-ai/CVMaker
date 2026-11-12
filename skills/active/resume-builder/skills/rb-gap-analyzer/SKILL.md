---
name: rb_gap_analyzer
description: Strategic gap analysis between CV Experience and Job Description.
allowed_tools: [execute]
---

# Gap Analyzer

## Overview

This skill performs a strategic analysis comparing the user's CV Experience section against the Job Description requirements. It provides actionable recommendations without modifying the CV JSON.

## How It Works

1. **Input**: Parsed CV JSON from parse-cv and Job Description text
2. **Analysis**: Uses LLM to identify gaps between JD requirements and CV evidence
3. **Output**: Text report titled "GAP ANALYSIS & RECOMMENDATIONS"

## Execution

### Tool Command

```bash
python skills/active/resume-builder/skills/rb-gap-analyzer/tools/main.py <cv_json_path> <jd_path> <output_report_path>
```

Example:
```bash
python skills/active/resume-builder/skills/rb-gap-analyzer/tools/main.py output/cv_data.json output/jd.txt output/gap_analysis.txt
```

## Output Format

The tool outputs a text report containing:

1. **Identified Gaps**
   - Undersold Skills: CV has experience but uses different terminology than JD
   - Missing Evidence: JD requirements with no supporting CV evidence

2. **Targeted Revisions**
   - 3-5 specific suggestions for improving experience bullets
   - Each revision includes:
     - Current bullet point
     - Suggested revision
     - JD keyword/reasoning

## Constraint

**DO NOT** modify the experience section in the CV JSON. This tool is strictly advisory and outputs recommendations only.