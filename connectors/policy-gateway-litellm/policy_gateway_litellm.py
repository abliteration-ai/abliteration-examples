import os
from typing import Any, Dict, List

import litellm

DEFAULT_BASE_URL = "https://api.abliteration.ai/policy"


def policy_completion(
    messages: List[Dict[str, str]],
    policy_id: str = "policy-gateway",
    policy_user: str = "user-12345",
    policy_project_id: str = "support-bot",
    policy_target: str | None = None,
    model: str = "abliterated-model",
    **kwargs: Any,
):
    """Call Policy Gateway through LiteLLM with policy metadata."""
    base_url = os.getenv("POLICY_GATEWAY_BASE_URL", DEFAULT_BASE_URL)
    api_key = os.environ["POLICY_GATEWAY_KEY"]

    headers = {
        "X-Policy-User": policy_user,
        "X-Policy-Project": policy_project_id,
    }
    if policy_target:
        headers["X-Policy-Target"] = policy_target

    return litellm.completion(
        model=model,
        messages=messages,
        api_base=base_url,
        api_key=api_key,
        extra_headers=headers,
        extra_body={"policy_id": policy_id},
        **kwargs,
    )
