from pathlib import Path
from typing import Optional

from deepagents import create_deep_agent
from deepagents.backends.local_shell import LocalShellBackend
from langchain_openrouter import ChatOpenRouter

from engine.core.configs import Config
from engine.core.logger import logger
from engine.models.llm import LLMClient


def resolve_path(user_path: str, base_dir: Path) -> Path:
    path = Path(user_path)
    if path.is_absolute():
        return path
    if str(path).startswith("input/") or str(path).startswith("input\\"):
        return Config.PROJECT_ROOT / path
    return base_dir / path


class ResumeAgent:
    def __init__(
        self,
        model: str = None,
        workspace_root: str = None,
    ):
        self.model = model or Config.MODEL
        self.workspace_root = workspace_root or Config.WORKSPACE_ROOT
        self._agent = None
    
    def _create_agent(self):
        logger.info(f"Creating ResumeAgent with model: {self.model}")
        
        backend = LocalShellBackend(root_dir=self.workspace_root)
        
        chat_model = ChatOpenRouter(
            model=self.model,
            api_key=Config.OPENROUTER_API_KEY,
        )
        
        agent = create_deep_agent(
            model=chat_model,
            skills=[Config.SKILLS_PATH],
            backend=backend,
        )
        
        return agent
    
    @property
    def agent(self):
        if self._agent is None:
            self._agent = self._create_agent()
        return self._agent
    
    def process(
        self,
        input_path: str,
        output_path: str = None,
        job_description_path: str = None
    ) -> dict:
        Config.validate()
        
        if Config.OUTPUT_DIR.exists():
            for f in Config.OUTPUT_DIR.iterdir():
                if f.is_file():
                    f.unlink()
        
        input_file = resolve_path(input_path, Config.INPUT_DIR)
        
        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        output_file = resolve_path(output_path, Config.OUTPUT_DIR) if output_path else Config.OUTPUT_DIR / "resume.pdf"
        
        jd_file = None
        if job_description_path:
            jd_file = resolve_path(job_description_path, Config.INPUT_DIR)
            if jd_file.exists():
                logger.info(f"Using JD: {jd_file}")
            else:
                logger.warning(f"JD file not found: {jd_file}, proceeding without JD matching")
                jd_file = None
        
        logger.info(f"Processing: {input_file}")
        
        if jd_file:
            user_message = (
                f"Process resume from input/resume.pdf with JD from input/jd.txt.\n"
                f"Steps:\n"
                f"1. Run: python skills/active/parse-cv/tools/main.py input/resume.pdf output/cv_data.json\n"
                f"2. Run: python skills/active/resume-builder/skills/rb-gap-analyzer/tools/main.py output/cv_data.json input/jd.txt output/gap_analysis.txt\n"
                f"   Print the gap_analysis.txt content after running.\n"
                f"3. Copy JD to output: copy input/jd.txt output/jd.txt\n"
                f"4. Run: python skills/active/generate-latex/tools/main.py output/cv_data.json skills/active/generate-latex/templates/classic/resume.tex output/resume.tex\n"
                f"5. Run: python skills/active/compile-pdf/tools/main.py output/resume.tex output/resume.pdf\n"
                f"Final PDF should be at output/resume.pdf"
            )
        else:
            user_message = (
                f"Process the resume at {input_file}. "
                f"Follow the resume-builder workflow: "
                f"parse-cv -> generate-latex -> compile-pdf. "
                f"Output should be at {output_file}"
            )
        
        result = self.agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_message,
                    }
                ]
            }
        )
        
        logger.info(f"Processing complete: {output_file}")
        return result
    
    def run(
        self,
        input_path: str,
        output_path: str = None,
        job_description_path: str = None
    ) -> str:
        result = self.process(input_path, output_path, job_description_path)
        return str(result)