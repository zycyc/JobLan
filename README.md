# JobLan

JobLan is an open-source automated job application assistant that helps streamline the job search and application process using local LLM models. It provides modular functionality for background analysis, job searching, and customized cover letter generation.

Lan means "language" (as in large language model), "land" (land a job!), "langchain" (langchain and langgraph used in this project), etc. ;)

## Features

- **Background Analysis**: Automatically analyzes resumes and professional information to create comprehensive candidate profiles
- **Automated Job Search**: Integrates with LinkedIn to search and collect relevant job postings
- **Custom Cover Letter Generation**: Creates personalized cover letters for each job application using local LLM
- **Local File Management**: Maintains organized storage of all generated documents

## Prerequisites

- Any M-chip Mac (tested on M3)
- Python 3.8+ (tested on 3.12)
- Local LLM model (default: MLX Pipeline with Llama-3.2-3B-Instruct)
- LinkedIn Account (for job search functionality, *please use at your own risk and try to use a non-personal account if possible*)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/zycyc/JobLan.git
cd JobLan
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Configure your settings:
Edit config.py with your LinkedIn credentials, LLM preferences, and other settings

## Usage

```bash
python main.py
```

## TODO

- [ ] Add more search options
- [ ] Fine-tune LLMs on user-edited cover letters
- [ ] ...

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [MLX team](https://github.com/ml-explore/mlx) bringing LLMs to M-chip Macs with increasingly improved APIs
- [GangGraph](https://github.com/langchain-ai/langgraph) for easy implementation of LLM agents as graphs
- [linkedin-api](https://github.com/tomquirk/linkedin-api) for scraping LinkedIn job listings