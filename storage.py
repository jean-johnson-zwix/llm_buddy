import os
import json
import sqlite3
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

DB_PATH = "data/benchmarks.db"
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
BQ_DATASET = os.getenv("BQ_DATASET")
BQ_RUNS_TABLE = f"{GCP_PROJECT_ID}.{BQ_DATASET}.runs"
BQ_RESULTS_TABLE = f"{GCP_PROJECT_ID}.{BQ_DATASET}.results"

_bq_client = None

def get_bq_client():
    global _bq_client
    if _bq_client is None:
        try:
            from google.cloud import bigquery
            _bq_client = bigquery.Client(project=GCP_PROJECT_ID)
        except Exception as e:
            print(f"[BIG QUERY] Could not initialize BigQuery client: {e}")
            _bq_client = None
    return _bq_client


def get_connection():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)


def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            run_id TEXT PRIMARY KEY,
            run_timestamp TEXT,
            mode TEXT,
            total_prompts INTEGER,
            models_evaluated TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT,
            prompt_id TEXT,
            category TEXT,
            difficulty TEXT,
            model_id TEXT,
            display_name TEXT,
            response TEXT,
            latency_seconds REAL,
            score_accuracy REAL,
            score_clarity REAL,
            score_completeness REAL,
            aggregate_score REAL,
            score_reasons TEXT,
            run_timestamp TEXT,
            error TEXT,
            FOREIGN KEY (run_id) REFERENCES runs(run_id)
        )
    """)

    conn.commit()
    conn.close()
    print("SQLite initialized at", DB_PATH)


def save_run_metadata(run_id: str, mode: str, total_prompts: int, model_ids: list):
    timestamp = datetime.now(timezone.utc).isoformat()

    # Save to SQLite
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO runs
        (run_id, run_timestamp, mode, total_prompts, models_evaluated)
        VALUES (?, ?, ?, ?, ?)
    """, (run_id, timestamp, mode, total_prompts, json.dumps(model_ids)))
    conn.commit()
    conn.close()

    # Save to BigQuery
    bq = get_bq_client()
    if bq:
        try:
            row = {
                "run_id": run_id,
                "run_timestamp": timestamp,
                "mode": mode,
                "total_prompts": total_prompts,
                "models_evaluated": json.dumps(model_ids)
            }
            errors = bq.insert_rows_json(BQ_RUNS_TABLE, [row])
            if errors:
                print(f"BIG QUERY: Run metadata insert errors: {errors}")
            else:
                print(f"BIG QUERY: Run metadata saved to BigQuery")
        except Exception as e:
            print(f"BIG QUERY: Failed to save run metadata: {e}")


def save_result(run_id: str, prompt: dict, model_result: dict, score_result: dict):
    timestamp = datetime.now(timezone.utc).isoformat()
    dimensions = score_result.get("dimensions", {})
    score_reasons = {
        dim: data.get("reason")
        for dim, data in dimensions.items()
    }

    # Save to SQLite
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO results (
            run_id, prompt_id, category, difficulty,
            model_id, display_name, response, latency_seconds,
            score_accuracy, score_clarity, score_completeness,
            aggregate_score, score_reasons, run_timestamp, error
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        run_id,
        prompt["id"],
        prompt["category"],
        prompt["difficulty"],
        model_result.get("model_id"),
        model_result.get("display_name"),
        model_result.get("response"),
        model_result.get("latency_seconds"),
        dimensions.get("accuracy", {}).get("score"),
        dimensions.get("clarity", {}).get("score"),
        dimensions.get("completeness", {}).get("score"),
        score_result.get("aggregate_score"),
        json.dumps(score_reasons),
        timestamp,
        model_result.get("error") or score_result.get("error")
    ))
    conn.commit()
    conn.close()

    # Save to BigQuery
    bq = get_bq_client()
    if bq:
        try:
            row = {
                "run_id": run_id,
                "prompt_id": prompt["id"],
                "category": prompt["category"],
                "difficulty": prompt["difficulty"],
                "model_id": model_result.get("model_id"),
                "display_name": model_result.get("display_name"),
                "response": model_result.get("response"),
                "latency_seconds": model_result.get("latency_seconds"),
                "score_accuracy": dimensions.get("accuracy", {}).get("score"),
                "score_clarity": dimensions.get("clarity", {}).get("score"),
                "score_completeness": dimensions.get("completeness", {}).get("score"),
                "aggregate_score": score_result.get("aggregate_score"),
                "score_reasons": json.dumps(score_reasons),
                "run_timestamp": timestamp,
                "error": model_result.get("error") or score_result.get("error")
            }
            errors = bq.insert_rows_json(BQ_RESULTS_TABLE, [row])
            if errors:
                print(f"  BIG QUERY: Result insert errors: {errors}")
            else:
                print(f"  BIG QUERY: Result saved to BigQuery")
        except Exception as e:
            print(f"  BIG QUERY: Failed to save result: {e}")

# Methods to retrieve data for Dashboard

def fetch_all_results() -> list:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM results ORDER BY run_timestamp DESC")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def fetch_leaderboard() -> list:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            display_name,
            model_id,
            ROUND(AVG(aggregate_score), 2) as avg_score,
            ROUND(AVG(score_accuracy), 2) as avg_accuracy,
            ROUND(AVG(score_clarity), 2) as avg_clarity,
            ROUND(AVG(score_completeness), 2) as avg_completeness,
            ROUND(AVG(latency_seconds), 3) as avg_latency,
            COUNT(*) as total_evaluations
        FROM results
        WHERE aggregate_score IS NOT NULL
        GROUP BY model_id
        ORDER BY avg_score DESC
    """)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def fetch_results_by_category() -> list:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            display_name,
            category,
            ROUND(AVG(aggregate_score), 2) as avg_score,
            COUNT(*) as total
        FROM results
        WHERE aggregate_score IS NOT NULL
        GROUP BY model_id, category
        ORDER BY category, avg_score DESC
    """)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows