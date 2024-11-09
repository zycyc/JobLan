from pathlib import Path
from typing import Dict
from langchain.prompts import PromptTemplate


class CoverLetterWriter:
    def __init__(self, llm, user_background_file: Path, cover_letters_dir: Path):
        self.llm = llm
        self.user_background_file = user_background_file
        self.cover_letters_dir = cover_letters_dir

        self.cover_letter_prompt = PromptTemplate(
            input_variables=["background_info", "job_description", "company_name"],
            template="""
            Using the following information, write a professional and personalized cover letter:
            
            Background Information:
            {background_info}
            
            Job Description:
            {job_description}
            
            Company:
            {company_name}
            
            The cover letter should:
            1. Show enthusiasm for the role and company
            2. Match the candidate's experience with job requirements
            3. Highlight relevant achievements
            4. Demonstrate knowledge of the company
            """,
        )

        self.cover_letter_chain = self.cover_letter_prompt | self.llm

    def load_background_info(self) -> str:
        """Load the user's background information"""
        with open(self.user_background_file, "r") as f:
            return f.read()

    def generate_cover_letter(self, job_info: Dict) -> str:
        """Generate a customized cover letter"""
        background_info = self.load_background_info()

        cover_letter = self.cover_letter_chain.invoke(
            {
                "background_info": background_info,
                "job_description": job_info["description"],
                "company_name": job_info["company"],
            }
        )

        return cover_letter

    def save_cover_letter(self, cover_letter: str, job_info: Dict):
        """Save the cover letter to a file"""
        filename = f"{job_info['company']}_{job_info['title']}.txt".replace(" ", "_")
        file_path = self.cover_letters_dir / filename

        with open(file_path, "w") as f:
            f.write(cover_letter)

        return file_path

    def run(self, job_info: Dict):
        """Main execution method"""
        cover_letter = self.generate_cover_letter(job_info)
        file_path = self.save_cover_letter(cover_letter, job_info)
        return file_path
