import os
import json
from typing import Dict, List, Annotated
from typing_extensions import TypedDict
from langgraph.graph import Graph
from config import *
from modules.background_checker import BackgroundChecker
from modules.job_searcher import JobSearcher
from modules.cover_letter_writer import CoverLetterWriter
from langchain_community.llms.mlx_pipeline import MLXPipeline
from mlx_lm import load
from huggingface_hub import snapshot_download


# Define the State schema
class WorkflowState(TypedDict):
    """
    Represents the state of our job application workflow.

    Attributes:
        user_background: The parsed user background information
        keywords: Job search keywords
        location: Job search location
        num_jobs: Number of jobs to search for
        jobs: List of found job listings
        cover_letters: List of generated cover letters
        current_step: Tracks the current step in the workflow
    """

    user_background: Dict
    keywords: List[str]
    location: str
    num_jobs: int
    jobs: List[Dict]
    cover_letters: List[Dict]
    current_step: str


def create_workflow():
    # Initialize LLM
    local_model_dir = os.path.join(MODEL_DIR, MODEL_NAME)

    # Create model directory if it doesn't exist
    os.makedirs(local_model_dir, exist_ok=True)

    # Check if model files exist, if not download them
    if not os.path.exists(os.path.join(local_model_dir, "tokenizer_config.json")):
        print(f"Downloading model {MODEL_NAME} to {local_model_dir}...")
        snapshot_download(
            repo_id=f"mlx-community/{MODEL_NAME}", local_dir=local_model_dir
        )

    with open(os.path.join(local_model_dir, "tokenizer_config.json"), "r") as f:
        tokenizer_config = json.load(f)
    tokenizer_config["trust_remote_code"] = True

    model, tokenizer = load(local_model_dir, tokenizer_config)
    pipeline_kwargs = MODEL_CONFIG
    llm = MLXPipeline(model=model, tokenizer=tokenizer, pipeline_kwargs=pipeline_kwargs)

    # Initialize components
    background_checker = BackgroundChecker(llm, USER_BACKGROUND_FILE)
    job_searcher = JobSearcher(JOB_LISTINGS_FILE)
    cover_letter_writer = CoverLetterWriter(
        llm, USER_BACKGROUND_FILE, COVER_LETTERS_DIR
    )

    # Create the graph
    workflow = Graph()

    # Add nodes with state-aware functions
    workflow.add_node(
        "check_background",
        lambda state: {
            **state,
            "user_background": background_checker.run(),
            "current_step": "check_background",
        },
    )

    workflow.add_node(
        "search_jobs",
        lambda state: {
            **state,
            "jobs": job_searcher.run(
                state["keywords"], state["location"], num_jobs=state["num_jobs"]
            ),
            "current_step": "search_jobs",
        },
    )

    workflow.add_node(
        "write_cover_letters",
        lambda state: {
            **state,
            "cover_letters": [cover_letter_writer.run(job) for job in state["jobs"]],
            "current_step": "write_cover_letters",
        },
    )

    # Set the entry point and connections
    workflow.set_entry_point("check_background")
    workflow.add_edge("check_background", "search_jobs")
    workflow.add_edge("search_jobs", "write_cover_letters")
    workflow.set_finish_point("write_cover_letters")

    return workflow.compile()


def main():
    # Create the workflow
    workflow = create_workflow()

    # Get user input
    print("Enter job search keywords (comma-separated):")
    keywords = [k.strip() for k in input().split(",")]
    location = input("Enter location: ")
    num_jobs = int(input("Enter number of jobs to search for: "))

    # Initialize the state
    initial_state = WorkflowState(
        user_background={},  # Will be populated by background_checker
        keywords=keywords,
        location=location,
        num_jobs=num_jobs,
        jobs=[],  # Will be populated by job_searcher
        cover_letters=[],  # Will be populated by cover_letter_writer
        current_step="init",
    )

    # Execute the workflow with the initial state
    results = workflow.invoke(initial_state)

    print("\nWorkflow completed!")
    print(f"Generated cover letters can be found in: {COVER_LETTERS_DIR}")


if __name__ == "__main__":
    main()
