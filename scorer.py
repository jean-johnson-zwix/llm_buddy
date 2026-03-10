import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from groq import Groq

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
JUDGE_MODEL = "moonshotai/kimi-k2-instruct"

SCORING_DIMENSIONS = {
    "accuracy":    "Is the response factually correct and does it fully answer the question?",
    "clarity":     "Is the response clear, well-structured, and easy to understand?",
    "completeness":"Does the response cover all aspects of the question without missing key points?",
}


def build_judge_prompt(
    original_prompt: str,
    model_response: str,
    evaluation_criteria: str,
    dimension: str,
    dimension_description: str
) -> str:
    return f"""You are an expert LLM evaluator. Your job is to score an AI model's response on a specific dimension.

ORIGINAL QUESTION:
{original_prompt}

MODEL RESPONSE:
{model_response}

EVALUATION CRITERIA FOR THIS QUESTION:
{evaluation_criteria}

SCORING DIMENSION: {dimension}
DIMENSION DESCRIPTION: {dimension_description}

INSTRUCTIONS:
- Score the response on {dimension} from 1 to 10.
- 1 = completely fails, 10 = perfect.
- Be strict and objective.
- Your entire response must be in this exact format, nothing else:

SCORE: <number>
REASON: <one sentence explaining the score>
"""


def parse_judge_response(raw: str) -> dict:
    try:
        lines = raw.strip().split("\n")
        score_line = next(l for l in lines if l.startswith("SCORE:"))
        reason_line = next(l for l in lines if l.startswith("REASON:"))
        score = float(score_line.replace("SCORE:", "").strip())
        reason = reason_line.replace("REASON:", "").strip()
        return {"score": score, "reason": reason, "parse_error": None}
    except Exception as e:
        return {"score": None, "reason": None, "parse_error": str(e)}


def score_response(
    original_prompt: str,
    model_response: str,
    evaluation_criteria: str
) -> dict:
    if not model_response:
        return {
            "dimensions": {},
            "aggregate_score": None,
            "error": "No model response to score"
        }

    dimension_scores = {}
    for dimension, description in SCORING_DIMENSIONS.items():
        prompt = build_judge_prompt(
            original_prompt=original_prompt,
            model_response=model_response,
            evaluation_criteria=evaluation_criteria,
            dimension=dimension,
            dimension_description=description
        )
        try:
            response = groq_client.chat.completions.create(
                model=JUDGE_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200
            )
            raw = response.choices[0].message.content
            parsed = parse_judge_response(raw)
            dimension_scores[dimension] = parsed
        except Exception as e:
            dimension_scores[dimension] = {
                "score": None,
                "reason": None,
                "parse_error": str(e)
            }

        time.sleep(2)


    valid_scores = [
        v["score"] for v in dimension_scores.values()
        if v["score"] is not None
    ]
    aggregate = round(sum(valid_scores) / len(valid_scores), 2) if valid_scores else None

    return {
        "dimensions": dimension_scores,
        "aggregate_score": aggregate,
        "error": None
    }