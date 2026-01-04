import os
from dotenv import load_dotenv
import google.generativeai as genai
from groq import Groq

load_dotenv()

TEST_PROMPT = "Classify the current LLM models based on their performance in coding, reasoning, summarization, rag?"

def test_gemini():
    print("\nTesting Gemini 2.0 Flash")
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(TEST_PROMPT)
        print(f"Gemini SUCCESS: {response.text.strip()}")
        return True
    except Exception as e:
        print(f"Gemini FAILED: {e}")
        return False

def test_groq(model_id, label):
    print(f"\nTesting {label}")
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": TEST_PROMPT}],
            max_tokens=100
        )
        print(f"{label} SUCCESS: {response.choices[0].message.content.strip()}")
        return True
    except Exception as e:
        print(f"{label} FAILED: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("LLM Buddy — API Validation")
    print("=" * 50)

    results = {
        "Gemini 2.0 Flash": test_gemini(),
        "LLaMA 4 Scout": test_groq("meta-llama/llama-4-scout-17b-16e-instruct", "LLaMA 4 Scout"),
        "LLaMA 3.1 8B": test_groq("llama-3.1-8b-instant", "LLaMA 3.1 8B"),
    }

    print("\n" + "=" * 50)
    print("RESULTS SUMMARY")
    print("=" * 50)
    for model, status in results.items():
        print(f"{model}: {status}")