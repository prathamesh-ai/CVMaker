import json
import sys
import os
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def render_template(json_data: dict, template_path: str, output_path: str) -> str:
    """Render LaTeX template with JSON data using Jinja2."""
    
    template_dir = os.path.dirname(template_path)
    template_name = os.path.basename(template_path)
    
    env = Environment(
        block_start_string='{%',
        block_end_string='%}',
        variable_start_string='{{',
        variable_end_string='}}',
        loader=FileSystemLoader(template_dir)
    )
    
    template = env.get_template(template_name)
    rendered_tex = template.render(**json_data)
    
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(rendered_tex, encoding='utf-8')
    
    cls_source = Path(template_dir) / 'resume.cls'
    cls_dest = output_file.parent / 'resume.cls'
    if cls_source.exists() and not cls_dest.exists():
        shutil.copy(str(cls_source), str(cls_dest))
    
    return str(output_file)


def load_json(json_path: str) -> dict:
    """Load CV data from JSON file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: main.py <json_path> <template_path> <output_path>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    template_file = sys.argv[2]
    output_file = sys.argv[3]
    
    json_data = load_json(json_file)
    result = render_template(json_data, template_file, output_file)
    print(f"Generated: {result}")