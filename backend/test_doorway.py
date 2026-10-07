from governance.contract import RevealAuthorizationRequest
from governance.doorway import authorize_reveal

request = RevealAuthorizationRequest(
    requester_id="alice",
    asset_id="demo"
)

request.governance_context.update({
    "identity_id": "alice",
    "owner_id": "alice",
    "expires_at": "2030-01-01T00:00:00",
    "execution_time": "2026-10-06T17:00:00",
    "constraint_profile": "default",
    "temporal_rule_profile": "default"
})

result = authorize_reveal(request)

print(result.model_dump())
