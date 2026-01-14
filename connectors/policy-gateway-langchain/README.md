# Policy Gateway LangChain connector

A tiny LangChain wrapper plus a callback handler for policy decision metadata.

## 5-minute quickstart
1) Copy `policy_gateway_langchain.py` into your project.
2) Install dependencies:

```bash
pip install langchain-openai
```

3) Build a Policy Gateway-aware ChatOpenAI client:

```python
from policy_gateway_langchain import build_policy_gateway_chat, PolicyGatewayAuditCallback

llm = build_policy_gateway_chat(
    api_key="YOUR_POLICY_KEY",
    policy_id="policy-gateway",
    policy_user="user-12345",
    policy_project_id="support-bot",
)

response = llm.invoke("Summarize our refund policy.", config={"callbacks": [PolicyGatewayAuditCallback()]})
print(response.content)
```

## Policy Gateway base URL (optional)
The helper defaults to the hosted Policy Gateway. Set this only if you need to override it:

```bash
export POLICY_GATEWAY_BASE_URL=https://api.abliteration.ai/policy
```

Then pass `base_url=os.environ["POLICY_GATEWAY_BASE_URL"]` into `build_policy_gateway_chat`.

## Note on headers
If your LangChain version does not support `default_headers`, pass headers via the underlying OpenAI client or use a lightweight HTTP wrapper instead.

## Sample log output
See `sample-logs.txt` for example audit lines you can feed into dashboards.
