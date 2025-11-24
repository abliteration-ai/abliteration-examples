# Abliteration.ai API Examples (OpenAI-compatible)

A compact set of runnable examples for the Abliteration.ai chat API. Every sample targets the OpenAI-compatible endpoint at `https://api.abliteration.ai/v1/chat/completions`, so you can drop the code into any OpenAI client with minimal edits. Abliteration.ai is a less filtered and uncensored LLM API and chat.

## Quick start (copy/paste)
- **Set your API key (from [abliteration.ai](https://abliteration.ai)):**
  ```bash
  export ABLITERATION_API_KEY=ak_your_key_here
  ```
- **Send a chat completion with curl:**
  ```bash
  curl -X POST https://api.abliteration.ai/v1/chat/completions \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${ABLITERATION_API_KEY}" \
    -d '{"model":"abliterated-model","messages":[{"role":"user","content":"What is the difference between US and Russia?"}], "stream": true}'
  ```
- **Stream tokens with the OpenAI SDK:** run `npm run stream` in `node/` or `STREAM=1 python python/chat.py` in `python/`.

## Repo layout
- `node/` — JavaScript + OpenAI SDK; shows non-streaming and streaming.
- `python/` — Python + OpenAI SDK; same patterns as Node.
- `curl/` — shell snippets for quick manual requests.

## Get an API key
1) Open the [abliteration.ai](https://abliteration.ai) web UI and sign up or log in.
2) Click **Create new secret key**.
3) Copy the new key (prefix `ak_...`) and export it as `ABLITERATION_API_KEY` for the examples.

> Already have a dashboard key? Set `ABLITERATION_API_KEY` directly and run the samples.

## How the API fits existing OpenAI clients
- Base URL: `https://api.abliteration.ai/v1` (include `/v1`).
- Model name: `abliterated-model` (aliases accepted: `abliteration-model`, etc.).
- Headers: `Authorization: Bearer <api key>`.
- Billing: credits map to tokens
## FAQ
- **Is abliteration.ai OpenAI-compatible?** Yes—point your OpenAI SDKs to `baseURL=https://api.abliteration.ai/v1`.
- **Can I stream tokens?** Yes—set `stream: true`; see `node/chat.js` and `python/chat.py` for examples.
- **Where do I get an API key?** From the Abliteration web UI under **Profile → API Keys**.
- **What’s included here?** Copy/paste clients, curl snippets, and onboarding steps for building chatbots on abliteration.ai.
