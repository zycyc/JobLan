from pathlib import Path
from typing import Dict, Optional
import json
from langchain.prompts import PromptTemplate
from pypdf import PdfReader


class BackgroundChecker:
    def __init__(self, llm, user_background_file: Path):
        self.llm = llm
        self.user_background_file = user_background_file

        self.summary_prompt = PromptTemplate(
            input_variables=["background_info"],
            template="""
            Analyze the following background information and create a detailed summary 
            that would be useful for job applications and cover letters:
            
            {background_info}
            
            Please provide a detailed professional summary including:
            1. Professional experience
            2. Technical skills
            3. Educational background
            4. Notable achievements
            5. Professional interests
            """,
        )

        self.summary_chain = self.summary_prompt | self.llm

        self.resume_analysis_prompt = PromptTemplate(
            input_variables=["resume_text"],
            template="""
            Extract key professional information from the following resume text. 
            Be precise and maintain factual accuracy:

            {resume_text}

            Please extract and organize the following information:
            1. Work Experience (with dates, companies, and roles)
            2. Education (with institutions, degrees, and dates)
            3. Technical Skills (categorized if possible)
            4. Certifications and Awards
            5. Projects (if any)

            Format the output as a structured JSON with these categories.
            Only include information that is explicitly stated in the resume.
            """,
        )

        self.resume_chain = self.resume_analysis_prompt | self.llm

    def collect_user_input(self) -> Dict:
        """Collect user background information interactively"""
        print("Please provide your background information:")

        background_info = {
            "resume_path": input("Path to your resume file: "),
            "linkedin_url": input("LinkedIn URL (optional): "),
            "github_url": input("GitHub URL (optional): "),
            "additional_info": input(
                "Any additional information you'd like to include: "
            ),
        }

        return background_info

    def analyze_resume(self, resume_path: str) -> str:
        """Analyze resume content from PDF file"""
        try:
            # Read PDF file
            reader = PdfReader(resume_path)
            resume_text = ""
            for page in reader.pages:
                resume_text += page.extract_text()

            if not resume_text.strip():
                raise ValueError("No text could be extracted from the PDF")

            # Analyze resume content using LLM
            analysis_result = self.resume_chain.invoke({"resume_text": resume_text})

            # Parse the JSON response
            try:
                parsed_result = json.loads(analysis_result)
                return json.dumps(parsed_result, indent=2)
            except json.JSONDecodeError:
                return analysis_result  # Return raw text if JSON parsing fails

        except Exception as e:
            raise Exception(f"Error analyzing resume: {str(e)}")

    def generate_background_summary(self, background_info: Dict) -> str:
        """Generate a detailed summary of user background"""
        # First analyze the resume
        resume_analysis = self.analyze_resume(background_info["resume_path"])

        # Combine all information
        combined_info = f"""
        Resume Analysis: {resume_analysis}
        LinkedIn: {background_info['linkedin_url']}
        GitHub: {background_info['github_url']}
        Additional Information: {background_info['additional_info']}
        """

        # Generate summary using LLM
        summary = self.summary_chain.invoke({"background_info": combined_info})
        return summary

    def save_background_info(self, summary: str):
        """Save the background summary to a file"""
        with open(self.user_background_file, "w") as f:
            f.write(summary)
        # print head of the file
        print(f"Saved background info to: {self.user_background_file}")
        with open(self.user_background_file, "r") as f:
            print(f.readlines()[:10])
        print("-" * 100)

    def run(self):
        """Main execution method"""
        # Check if background file already exists
        if self.user_background_file.exists():
            print(f"Loading existing background from: {self.user_background_file}")
            with open(self.user_background_file, "r") as f:
                return f.read()

        # If no existing file, collect new information and generate summary
        background_info = self.collect_user_input()
        summary = self.generate_background_summary(background_info)
        self.save_background_info(summary)
        return summary
