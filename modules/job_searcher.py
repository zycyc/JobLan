import pandas as pd
from typing import List, Dict
from linkedin_api import Linkedin
from config import USERNAME, PASSWORD


class JobSearcher:
    def __init__(self, job_listings_file: str):
        self.job_listings_file = job_listings_file

    def search_jobs(
        self, keywords: List[str], location: str, num_jobs: int = 5
    ) -> List[Dict]:
        """Search for jobs using provided keywords with error handling"""
        print("Searching for jobs...")
        jobs = []

        api = Linkedin(USERNAME, PASSWORD)

        keywords_str = " ".join(keywords)
        jobs = api.search_jobs(keywords=keywords_str, location=location, limit=num_jobs)
        print(f"Found {len(jobs)} jobs")

        cleaned_jobs = []
        for job in jobs:
            job_id = "".join(filter(str.isdigit, job["trackingUrn"]))
            job_info = api.get_job(job_id)
            job_title = job_info["title"]
            job_company = job_info["companyDetails"][
                "com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany"
            ]["companyResolutionResult"]["name"]
            job_description = job_info["description"]["text"]
            job_url = job_info["applyMethod"]["com.linkedin.voyager.jobs.OffsiteApply"][
                "companyApplyUrl"
            ]

            cleaned_jobs.append(
                {
                    "title": job_title,
                    "company": job_company,
                    "description": job_description,
                    "url": job_url,
                }
            )

        return cleaned_jobs

    def update_job_listings(self, new_jobs: List[Dict]):
        """Update the job listings CSV file"""
        df = pd.DataFrame(new_jobs)

        try:
            # Try to read existing file
            existing_df = pd.read_csv(self.job_listings_file)
            if not existing_df.empty:
                # Only concatenate if existing file has data
                df = pd.concat([existing_df, df]).drop_duplicates(
                    subset=["url"], keep="first"
                )
        except (FileNotFoundError, pd.errors.EmptyDataError):
            # Handle both cases: file doesn't exist or is empty
            pass

        df.to_csv(self.job_listings_file, index=False)

    def run(self, keywords: List[str], location: str, num_jobs: int = 5):
        """Main execution method"""
        jobs = self.search_jobs(keywords, location, num_jobs)
        self.update_job_listings(jobs)
        return jobs
