#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agents.resume_agent import ResumeAgent
from engine.core.configs import Config
from engine.core.logger import logger


def main():
    parser = argparse.ArgumentParser(description="ATS Resume Builder")
    parser.add_argument("input", help="Path to input PDF or DOCX file")
    parser.add_argument("-o", "--output", default=None, help="Output PDF path")
    parser.add_argument("-j", "--job-description", default=None, help="Path to Job Description .txt file")
    args = parser.parse_args()
    
    try:
        Config.validate()
        
        agent = ResumeAgent()
        result = agent.process(
            input_path=args.input,
            output_path=args.output,
            job_description_path=args.job_description
        )
        
        logger.info(f"Success: {result}")
        print(f"Resume generated: {args.output or 'resume.pdf'}")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()