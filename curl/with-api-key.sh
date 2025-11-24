#!/usr/bin/env bash
set -euo pipefail

BASE_URL=${ABLITERATION_BASE_URL:-https://api.abliteration.ai}
API_KEY=${ABLITERATION_API_KEY:-}

if [[ -z "$API_KEY" ]]; then
  echo "Set ABLITERATION_API_KEY before running." >&2
  exit 1
fi

echo "Calling abliteration.ai with your API key..."
curl -sS -X POST "$BASE_URL/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${API_KEY}" \
  -d '{
    "model": "abliterated-model",
    "messages": [
      {"role": "user", "content": "Summarize abliteration.ai in one upbeat sentence."}
    ]
  }'
echo
