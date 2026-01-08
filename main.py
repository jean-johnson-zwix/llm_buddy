import uuid
from datetime import datetime
from prompts.prompt_suite import PROMPT_SUITE, DEV_SUITE
from runner import run_all_models, MODELS
from scorer import score_response
from storage import initialize_db, save_run_metadata, save_result
from datetime import datetime, timezone


def run_benchmark(mode: str = "dev"):

    initialize_db()
    run_id = f"run_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
    suite = DEV_SUITE if mode == "dev" else PROMPT_SUITE
    model_ids = list(MODELS.keys())

    print("=" * 60)
    print("LLM Benchmarker")
    print("=" * 60)
    print(f"Run ID    : {run_id}")

    save_run_metadata(
        run_id=run_id,
        mode=mode,
        total_prompts=len(suite),
        model_ids=model_ids
    )

    total = len(suite)
    for i, prompt in enumerate(suite):
        print(f"\n[{i+1}/{total}] Prompt: {prompt['id']} | Category: {prompt['category']} | Difficulty: {prompt['difficulty']}")
        print(f"  Question: {prompt['prompt'][:80]}...")

        # Step 1: Run all models with prompt
        model_results = run_all_models(prompt["prompt"], dev_mode=(mode == "dev"))

        # Step 2: Score each model response
        for model_result in model_results:
            display = model_result["display_name"]

            if model_result["error"]:
                print(f"  Skipping scoring for {display} — inference error: {model_result['error']}")
                save_result(
                    run_id=run_id,
                    prompt=prompt,
                    model_result=model_result,
                    score_result={"dimensions": {}, "aggregate_score": None, "error": model_result["error"]}
                )
                continue

            print(f"  Scoring {display} response...")
            score_result = score_response(
                original_prompt=prompt["prompt"],
                model_response=model_result["response"],
                evaluation_criteria=prompt["evaluation_criteria"]
            )

            save_result(
                run_id=run_id,
                prompt=prompt,
                model_result=model_result,
                score_result=score_result
            )

            agg = score_result.get("aggregate_score")
            print(f"{display}: aggregate score = {agg}")

    print("\n" + "=" * 60)
    print("RUN COMPLETE")
    print("=" * 60)

    return run_id


if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "dev"
    if mode not in ("dev", "full"):
        print("Usage: python main.py [dev|full]")
        sys.exit(1)
    run_benchmark(mode=mode)