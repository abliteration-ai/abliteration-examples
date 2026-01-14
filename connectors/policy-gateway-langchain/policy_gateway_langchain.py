from typing import Any, Dict, Optional

from langchain.callbacks.base import BaseCallbackHandler
from langchain_openai import ChatOpenAI

DEFAULT_BASE_URL = "https://api.abliteration.ai/policy"


class PolicyGatewayAuditCallback(BaseCallbackHandler):
    """Logs Policy Gateway decision metadata for dashboards."""

    def on_llm_end(self, response, **kwargs: Any) -> None:
        meta = (response.llm_output or {}).get("policy") or response.response_metadata or {}
        if meta:
            print("policy_gateway_event", meta)


def build_policy_gateway_chat(
    api_key: str,
    policy_id: str,
    policy_user: str,
    policy_project_id: Optional[str] = None,
    base_url: str = DEFAULT_BASE_URL,
) -> ChatOpenAI:
    headers: Dict[str, str] = {
        "X-Policy-User": policy_user,
    }
    if policy_project_id:
        headers["X-Policy-Project"] = policy_project_id

    return ChatOpenAI(
        model="abliterated-model",
        base_url=base_url,
        api_key=api_key,
        model_kwargs={"policy_id": policy_id},
        default_headers=headers,
    )
