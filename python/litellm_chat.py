import os

from dotenv import load_dotenv
import litellm

load_dotenv()


def _model_with_provider(raw_model: str) -> str:
    """LiteLLM needs the provider encoded in the model string (e.g. openai/...)."""
    if "/" in raw_model or ":" in raw_model:
        return raw_model
    return f"openai/{raw_model}"


api_key = os.getenv("ABLITERATION_API_KEY")
if not api_key:
    raise SystemExit("Set ABLITERATION_API_KEY in a .env file or your environment.")

base_url = os.getenv("ABLITERATION_BASE_URL", "https://api.abliteration.ai/v1")
raw_model = os.getenv("ABLITERATION_MODEL", "abliterated-model")
model = _model_with_provider(raw_model)
stream = os.getenv("STREAM") == "1"


def main():
    prompt = "Give me one sentence about abliteration.ai as an uncensored OpenAI-compatible chat endpoint."

    if stream:
        print("Streaming response:")
        for chunk in litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            api_base=base_url,
            api_key=api_key,
            stream=True,
        ):
            delta = chunk["choices"][0]["delta"]
            text = delta.get("content") or ""
            if text:
                print(text, end="", flush=True)
        print("\n-- done --")
        return

    response = litellm.completion(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        api_base=base_url,
        api_key=api_key,
    )
    message = response["choices"][0]["message"]["content"] or "(no content returned)"
    print("Non-streaming response:\n" + message)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"LiteLLM request failed: {exc}")
