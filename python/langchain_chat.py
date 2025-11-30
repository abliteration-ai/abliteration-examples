import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

api_key = os.getenv("ABLITERATION_API_KEY")
if not api_key:
    raise SystemExit("Set ABLITERATION_API_KEY in a .env file or your environment.")

base_url = os.getenv("ABLITERATION_BASE_URL", "https://api.abliteration.ai/v1")
model = os.getenv("ABLITERATION_MODEL", "abliterated-model")
stream = os.getenv("STREAM") == "1"

# LangChain reads OpenAI-style env vars; set them so base_url is honored everywhere.
os.environ["OPENAI_API_KEY"] = api_key
os.environ["OPENAI_BASE_URL"] = base_url

llm = ChatOpenAI(
    model=model,
    temperature=0.6,
)


def to_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            part.get("text", "") if isinstance(part, dict) else str(part) for part in content
        )
    return str(content or "")


def main():
    prompt = "Give me one sentence on why abliteration.ai is an uncensored, OpenAI-compatible endpoint."

    if stream:
        print("Streaming response:")
        for chunk in llm.stream(prompt):
            text = to_text(getattr(chunk, "content", None) or getattr(chunk.message, "content", None))
            if text:
                print(text, end="", flush=True)
        print("\n-- done --")
        return

    message = llm.invoke(prompt)
    print("Non-streaming response:\n" + to_text(message.content))


if __name__ == "__main__":
  try:
    main()
  except Exception as exc:  # noqa: BLE001
    raise SystemExit(f"LangChain request failed: {exc}")
