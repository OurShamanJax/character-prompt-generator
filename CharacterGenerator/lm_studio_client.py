import requests
import json
import traceback
import re

LM_STUDIO_URL = "http://127.0.0.1:1234/v1"

class LMStudioClient:
    def list_models(self):
        try:
            r = requests.get(f"{LM_STUDIO_URL}/models", timeout=5)
            r.raise_for_status()
            data = r.json()
            print("[DEBUG] /models response:", data)
            models = [m.get("id") for m in data.get("data", []) if m.get("id")]
            return models
        except Exception:
            print("[ERROR] Failed to fetch models:")
            print(traceback.format_exc())
            return []

    def generate_character(self, model, system_prompt):
        """
        Generate a character using the specified model.
        Extracts JSON safely from LLM output even if it contains extra text.
        """
        try:
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": "Generate a complete character."}
                ],
                "temperature": 0.8
            }

            r = requests.post(f"{LM_STUDIO_URL}/chat/completions", json=payload, timeout=60)
            r.raise_for_status()
            response = r.json()
            print("[DEBUG] /chat/completions response:", response)

            raw_text = response["choices"][0]["message"]["content"]

            # Extract JSON block using regex
            json_match = re.search(r"\{.*\}", raw_text, re.DOTALL)
            if not json_match:
                raise ValueError("No JSON found in model output.")

            char_data = json.loads(json_match.group(0))
            return char_data

        except Exception:
            print("[ERROR] Character generation failed:")
            print(traceback.format_exc())
            return None
