#!/usr/bin/env bash
set -euo pipefail

BASE_URL=${ABLITERATION_BASE_URL:-https://api.abliteration.ai}

echo "Calling the anonymous free tier..."
curl -sS -X POST "$BASE_URL/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "X-Free-Tier: true" \
  -d '{
    "model": "abliterated-model",
    "messages": [
      {"role": "user", "content": "Say hi from the free tier example script."}
    ]
  }'
echo
