#!/usr/bin/env python3
"""Complete pipeline wrapper for resume processing."""
import sys
import json
import shutil
from pathlib import Path

project_root = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(project_root))


def run_pipeline(input_path: str, output_path: str, jd_path: str = None):
    output_dir = project_root / "output"
    
    if output_dir.exists():
        for f in output_dir.iterdir():
            if f.is_file():
                f.unlink()
    
    cv_json_path = output_dir / "cv_data.json"
    
    import importlib.util
    spec = importlib.util.spec_from_file_location("parse_cv_main", project_root / "skills" / "active" / "parse-cv" / "tools" / "main.py")
    parse_cv_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(parse_cv_module)
    parse_cv_module.parse_cv(input_path, str(cv_json_path))
    
    if jd_path:
        jd_text_path = output_dir / "jd.txt"
        shutil.copy(jd_path, jd_text_path)
        
        gap_report_path = output_dir / "gap_analysis.txt"
        with open(cv_json_path, 'r', encoding='utf-8') as f:
            cv_data = json.load(f)
        with open(jd_path, 'r', encoding='utf-8') as f:
            jd_text = f.read()
        
        spec = importlib.util.spec_from_file_location("gap_analyzer_main", project_root / "skills" / "active" / "resume-builder" / "skills" / "rb-gap-analyzer" / "tools" / "main.py")
        gap_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gap_module)
        report = gap_module.analyze_gaps(cv_data, jd_text)
        gap_report_path.write_text(report, encoding='utf-8')
        print("\n" + "="*60)
        print("GAP ANALYSIS REPORT")
        print("="*60)
        print(report)
        print("="*60 + "\n")
    
    template_path = project_root / "skills" / "active" / "generate-latex" / "templates" / "classic" / "resume.tex"
    tex_path = output_dir / "resume.tex"
    
    spec = importlib.util.spec_from_file_location("latex_main", project_root / "skills" / "active" / "generate-latex" / "tools" / "main.py")
    latex_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(latex_module)
    json_data = latex_module.load_json(str(cv_json_path))
    latex_module.render_template(json_data, str(template_path), str(tex_path))
    
    pdf_path = Path(output_path) if output_path else output_dir / "resume.pdf"
    tex_name = tex_path.name
    
    spec = importlib.util.spec_from_file_location("compile_pdf_main", project_root / "skills" / "active" / "compile-pdf" / "tools" / "main.py")
    compile_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(compile_module)
    compile_module.compile_latex(tex_name, str(pdf_path))
    
    print(f"Final PDF: {pdf_path}")
    return str(pdf_path)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: pipeline.py <input_resume> <output_pdf> [jd_file]")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    jd_path = sys.argv[3] if len(sys.argv) > 3 else None
    
    run_pipeline(input_path, output_path, jd_path)