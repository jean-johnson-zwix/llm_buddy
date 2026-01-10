import mlflow
import os
from dotenv import load_dotenv

load_dotenv()

EXPERIMENT_NAME = "llm-benchmarker"
mlflow.set_tracking_uri("./mlruns")
mlflow.set_experiment(EXPERIMENT_NAME)


def add_to_mlflow(
    run_id: str,
    mode: str,
    prompt: dict,
    model_result: dict,
    score_result: dict
):
    dimensions = score_result.get("dimensions", {})

    with mlflow.start_run(run_name=f"{model_result.get('display_name')}_{prompt['id']}"):

        # Tags
        mlflow.set_tags({
            "benchmark_run_id": run_id,
            "mode": mode,
            "model_id": model_result.get("model_id"),
            "display_name": model_result.get("display_name"),
            "prompt_id": prompt["id"],
            "category": prompt["category"],
            "difficulty": prompt["difficulty"]
        })

        # Parameters for evaluation
        mlflow.log_params({
            "model_id": model_result.get("model_id"),
            "prompt_id": prompt["id"],
            "category": prompt["category"],
            "difficulty": prompt["difficulty"],
            "mode": mode
        })

        # Metrics
        metrics = {}
        if model_result.get("latency_seconds"):
            metrics["latency_seconds"] = model_result["latency_seconds"]
        if score_result.get("aggregate_score"):
            metrics["aggregate_score"] = score_result["aggregate_score"]
        for dim, data in dimensions.items():
            if data.get("score") is not None:
                metrics[f"score_{dim}"] = data["score"]

        if metrics:
            mlflow.log_metrics(metrics)

        # Artifacts: text outputs
        if model_result.get("response"):
            artifact_path = f"response_{prompt['id']}_{model_result.get('model_id', 'unknown').replace('/', '_')}.txt"
            with open(artifact_path, "w", encoding="utf-8") as f:
                f.write(f"PROMPT:\n{prompt['prompt']}\n\n")
                f.write(f"RESPONSE:\n{model_result['response']}\n\n")
                f.write(f"AGGREGATE SCORE: {score_result.get('aggregate_score')}\n\n")
                for dim, data in dimensions.items():
                    f.write(f"{dim.upper()}: {data.get('score')} — {data.get('reason')}\n")
            mlflow.log_artifact(artifact_path)
            os.remove(artifact_path)