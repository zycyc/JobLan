from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "models"
COVER_LETTERS_DIR = BASE_DIR / "cover_letters"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
COVER_LETTERS_DIR.mkdir(exist_ok=True)

# File paths
USER_BACKGROUND_FILE = DATA_DIR / "user_background.txt"
JOB_LISTINGS_FILE = DATA_DIR / "job_listings.csv"

# Model configurations
MODEL_NAME = "Llama-3.2-3B-Instruct"  # Replace with your preferred local LLM
MODEL_CONFIG = {
    "temp": 0.7,
    "max_tokens": 512,
    "repetition_penalty": 1.05,
    "repetition_context_size": 20,
    "top_p": 0.9,
}

# LinkedIn credentials
USERNAME = "X"  # Replace X with your LinkedIn username
PASSWORD = "Y"  # Replace Y with your LinkedIn password
