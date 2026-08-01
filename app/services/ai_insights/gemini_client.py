import json
import re
import time
from google import genai
from google.genai import errors as genai_errors
from app.core.config import settings

_client = genai.Client(api_key=settings.gemini_api_key)


def _extract_json(raw_text: str) -> dict:
    text = raw_text.strip()
    match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    if match:
        text = match.group(1)
    return json.loads(text)


def generate_recommendation(prompt: str, max_retries: int = 2) -> dict:
    """
    Sends the prompt to Gemini and returns the parsed JSON response.
    Retries on transient API errors; raises ValueError on unrecoverable failures.
    """
    last_error = None

    for attempt in range(max_retries + 1):
        try:
            response = _client.models.generate_content(
                model="gemini-flash-latest",
                contents=prompt,
            )
            return _extract_json(response.text)

        except genai_errors.ClientError as e:
            # 4xx errors (bad request, invalid key, etc.) — don't retry, these won't fix themselves
            raise ValueError(f"Gemini API client error: {e}") from e

        except genai_errors.ServerError as e:
            # 5xx errors — transient, worth retrying
            last_error = e
            if attempt < max_retries:
                time.sleep(2 ** attempt)  # exponential backoff: 1s, 2s, 4s...
                continue

        except (json.JSONDecodeError, AttributeError) as e:
            last_error = e
            if attempt < max_retries:
                time.sleep(1)
                continue

    raise ValueError(f"Failed to get valid response from Gemini after {max_retries + 1} attempts: {last_error}")