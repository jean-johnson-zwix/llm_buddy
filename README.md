# LLM Evaluation & Benchmarking Platform

LLM Buddy helps you find the best LLM for your usecase.

An automated pipeline that evaluates multiple LLMs across tasks using LLM-as-a-judge scoring, MLflow experiment tracking, and BigQuery storage — with a live Streamlit leaderboard tracking model performance over time.

## Tech Stack
- **Languages:** Python 3.11
- **LLM APIs:** Google Gemini, Groq
- **Experiment Tracking:** MLflow
- **Storage:** SQLite (local), GCP BigQuery
- **Dashboard:** Streamlit
- **Deployment:** GCP Cloud Run, Docker
- **Scheduler:** GitHub Actions

## Models Evaluated
| Model | Provider |
|---|---|
| Gemini 2.5 Flash | Google AI Studio |
| LLaMA 4 Scout (17B) | Groq |
| LLaMA 3.1 8B | Groq |

## Judge Model
**LLaMA 4 Maverick (17B)** via Groq

## Task Categories
| Category |  What it tests |
|---|---|
| Coding | Correctness, debugging, design patterns |
| Reasoning | Logic, math, system design |
| Summarization | Clarity, conciseness, technical communication |
| RAG | Retrieval faithfulness, hallucination resistance |

## Scoring Dimensions
Each response is scored 1–10 on three dimensions:
- **Accuracy** — factual correctness and completeness of answer
- **Clarity** — structure, readability, and communication quality  
- **Completeness** — coverage of all aspects of the question


## Setup

### 1. Install dependencies
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment
```bash
# .env
GEMINI_API_KEY=
GROQ_API_KEY=
GCP_PROJECT_ID=
BQ_DATASET=
```

### 3. Run benchmark
```bash
python main.py
```

### 4. View results
```bash
# Streamlit dashboard
streamlit run dashboard/app.py

# MLflow experiment tracker
mlflow ui --backend-store-uri sqlite:///mlflow.db
```