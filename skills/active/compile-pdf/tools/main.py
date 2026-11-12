import subprocess
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent.resolve()


def get_docker_path(windows_path: str) -> str:
    """Convert Windows path to Docker-compatible Unix path."""
    unix_path = windows_path.replace("\\", "/")
    if ":" in unix_path:
        unix_path = unix_path.replace("c:/", "/c/").replace("C:/", "/c/")
    return unix_path


def compile_latex(tex_file_name: str, output_path: str = None) -> str:
    """Compile LaTeX file to PDF using Docker container.
    
    Args:
        tex_file_name: Name of the .tex file (e.g., 'resume.tex')
        output_path: Optional path for the output PDF
    
    Returns:
        Success message or error string
    """
    output_dir = str(PROJECT_ROOT / "output")
    docker_output = get_docker_path(output_dir)
    
    cmd = [
        "docker", "run", "--rm",
        "-v", f"{docker_output}:/data",
        "-w", "/data",
        "resume-compiler-minimal",
        tex_file_name
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    pdf_name = tex_file_name.replace('.tex', '.pdf')
    pdf_path = Path(output_dir) / pdf_name
    
    if pdf_path.exists():
        return f"Successfully compiled: {pdf_path}"
    else:
        return f"LaTeX Error: {result.stderr or result.stdout or 'Unknown error'}"


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: main.py <tex_path> <pdf_output_path>")
        print("Example: main.py output/resume.tex output/resume.pdf")
        sys.exit(1)
    
    tex_file = sys.argv[1]
    pdf_output = sys.argv[2]
    
    tex_name = os.path.basename(tex_file)
    
    result = compile_latex(tex_name, pdf_output)
    
    if result.startswith("Successfully"):
        print(result)
        sys.exit(0)
    else:
        print(result, file=sys.stderr)
        sys.exit(1)