import os
import json
import requests
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

# ======================================================
# Hugging Face Router Configuration
# ======================================================

ROUTER_URL = "https://router.huggingface.co/v1/chat/completions"

# Only include models you KNOW are enabled
MODELS_TO_TRY = [
    "Qwen/Qwen2.5-7B-Instruct"
]

# ======================================================
# Auth
# ======================================================

def get_headers() -> Dict[str, str]:
    token = os.getenv("HF_API_TOKEN")
    if not token:
        raise RuntimeError("HF_API_TOKEN not set in environment")
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

# ======================================================
# STRICT JSON EXTRACTION
# ======================================================

def extract_json(text: str, expected_type: str) -> str:
    """
    STRICT JSON extraction.
    - No regex
    - No partial objects
    - No nested fallback
    """

    text = text.strip()

    if expected_type == "object":
        if not (text.startswith("{") and text.endswith("}")):
            raise ValueError("Truncated JSON object detected")

    if expected_type == "array":
        if not (text.startswith("[") and text.endswith("]")):
            raise ValueError("Truncated JSON array detected")

    try:
        json.loads(text)
        return text
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON structure")

# ======================================================
# CORE QUERY FUNCTION
# ======================================================

def query_llm(
    system_prompt: str,
    user_prompt: str,
    expected_type: str = "object",
    max_retries: int = 3
) -> Any:

    headers = get_headers()

    system_guard = (
        f"You are a strict JSON generator.\n"
        f"Return ONLY a valid JSON {expected_type.upper()}.\n"
        f"No markdown.\n"
        f"No explanations.\n"
        f"No trailing commas.\n"
        f"No comments.\n"
    )

    for model_id in MODELS_TO_TRY:
        for attempt in range(1, max_retries + 1):

            payload = {
                "model": model_id,
                "messages": [
                    {
                        "role": "system",
                        "content": system_guard + "\n" + system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                "max_tokens": 1500,   # 🔥 prevents truncation
                "temperature": 0.0,
                "stream": False
            }

            try:
                print(f"Trying {model_id} (attempt {attempt})")

                response = requests.post(
                    ROUTER_URL,
                    headers=headers,
                    json=payload,
                    timeout=30
                )

                if response.status_code != 200:
                    raise RuntimeError(response.text)

                data = response.json()
                content = data["choices"][0]["message"]["content"].strip()

                print(f"Raw output:\n{content[:300]}")

                json_str = extract_json(content, expected_type)
                parsed = json.loads(json_str)

                # Final type check
                if expected_type == "object" and not isinstance(parsed, dict):
                    raise ValueError("Expected JSON object")

                if expected_type == "array" and not isinstance(parsed, list):
                    raise ValueError("Expected JSON array")

                print(f"✅ Success with {model_id}")
                return parsed

            except Exception as e:
                print(f"Retrying due to: {e}")
                continue

    raise RuntimeError("All models failed after retries")

# ======================================================
# LOCAL TEST
# ======================================================

if __name__ == "__main__":
    try:
        result = query_llm(
            system_prompt="Generate a simple project profile.",
            user_prompt="Create a JSON object with name and budget.",
            expected_type="object"
        )

        print("\nParsed JSON:")
        print(json.dumps(result, indent=2))

    except Exception as err:
        print(f"ERROR: {err}")
