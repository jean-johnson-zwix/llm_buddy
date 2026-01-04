import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from groq import Groq

load_dotenv()

MODELS = {
    "gemini-2.5-flash": {
        "provider": "gemini",
        "display_name": "Gemini 2.5 Flash"
    },
    "meta-llama/llama-4-scout-17b-16e-instruct": {
        "provider": "groq",
        "display_name": "LLaMA 4 Scout"
    },
    "llama-3.1-8b-instant": {
        "provider": "groq",
        "display_name": "LLaMA 3.1 8B"
    }
}

RATE_LIMIT_DELAY = {
    "gemini-2.5-flash": 2,
    "meta-llama/llama-4-scout-17b-16e-instruct": 3,
    "llama-3.1-8b-instant": 1,
}

gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def run_gemini(prompt: str, model_id: str) -> dict:
    start = time.time()
    try:
        response = gemini_client.models.generate_content(
            model=model_id,
            contents=prompt,
            config=types.GenerateContentConfig(max_output_tokens=2048)
        )
        latency = round(time.time() - start, 3)
        return {
            "response": response.text.strip(),
            "latency_seconds": latency,
            "error": None
        }
    except Exception as e:
        return {
            "response": None,
            "latency_seconds": None,
            "error": str(e)
        }


def run_groq(prompt: str, model_id: str) -> dict:
    start = time.time()
    try:
        response = groq_client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024
        )
        latency = round(time.time() - start, 3)
        return {
            "response": response.choices[0].message.content.strip(),
            "latency_seconds": latency,
            "error": None
        }
    except Exception as e:
        return {
            "response": None,
            "latency_seconds": None,
            "error": str(e)
        }


def run_model(model_id: str, prompt: str) -> dict:
    model_config = MODELS.get(model_id)
    if not model_config:
        return {
            "response": None,
            "latency_seconds": None,
            "error": f"Unknown model: {model_id}"
        }

    provider = model_config["provider"]
    if provider == "gemini":
        result = run_gemini(prompt, model_id)
    elif provider == "groq":
        result = run_groq(prompt, model_id)
    else:
        result = {
            "response": None,
            "latency_seconds": None,
            "error": f"Unknown provider: {provider}"
        }

    result["model_id"] = model_id
    result["display_name"] = model_config["display_name"]
    return result


def run_all_models(prompt: str, dev_mode: bool = True) -> list:
    results = []
    for model_id in MODELS:
        display = MODELS[model_id]['display_name']
        mode_tag = "[DEV]" if dev_mode else "[FULL]"
        print(f"  {mode_tag} Running {display}...")
        result = run_model(model_id, prompt)
        results.append(result)

        delay = RATE_LIMIT_DELAY.get(model_id, 2)
        print(f"  Waiting {delay}s before next call...")
        time.sleep(delay)

    return results