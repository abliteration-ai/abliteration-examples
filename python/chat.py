import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("ABLITERATION_API_KEY")
if not api_key:
    raise SystemExit("Set ABLITERATION_API_KEY in a .env file or your environment.")

client = OpenAI(
    api_key=api_key,
    base_url=os.getenv("ABLITERATION_BASE_URL", "https://api.abliteration.ai/v1"),
)

model = os.getenv("ABLITERATION_MODEL", "abliterated-model")
stream = os.getenv("STREAM") == "1"

def main():
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are abliteration.ai, concise and direct."},
            {"role": "user", "content": "Give me one sentence on why abliteration.ai is an uncensored OpenAI-compatible API."},
        ],
        "temperature": 0.6,
    }

    if stream:
        print("Streaming response:")
        for chunk in client.chat.completions.create(**payload, stream=True):
            delta = chunk.choices[0].delta
            text = delta.content or ""
            print(text, end="", flush=True)
        print("\n-- done --")
        return

    completion = client.chat.completions.create(**payload)
    message = completion.choices[0].message.content or "(no content returned)"
    print("Non-streaming response:\n" + message)

    if hasattr(completion, "estimated_credits_used"):
        print(f"Estimated credits used: {completion.estimated_credits_used}")
    if hasattr(completion, "estimated_cost_usd"):
        print(f"Estimated cost (USD): {completion.estimated_cost_usd}")
    if hasattr(completion, "remaining_credits"):
        print(f"Remaining credits: {completion.remaining_credits}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"Request failed: {exc}")
