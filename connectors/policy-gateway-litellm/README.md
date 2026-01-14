# Policy Gateway LiteLLM connector

LiteLLM helper that routes traffic through Policy Gateway with policy metadata.

## 5-minute quickstart
1) Copy `policy_gateway_litellm.py` into your project.
2) Install dependencies:

```bash
pip install litellm
```

3) Call Policy Gateway with LiteLLM:

```python
from policy_gateway_litellm import policy_completion

response = policy_completion(
    messages=[{"role": "user", "content": "Summarize our refund policy."}],
    policy_id="policy-gateway",
    policy_user="user-12345",
    policy_project_id="support-bot",
)

print(response["choices"][0]["message"]["content"])
```

## Policy Gateway base URL (optional)
The helper defaults to the hosted Policy Gateway. Set this only if you need to override it:

```bash
export POLICY_GATEWAY_BASE_URL=https://api.abliteration.ai/policy
```

## Sample log output
See `sample-logs.txt` for example audit lines you can feed into dashboards.
