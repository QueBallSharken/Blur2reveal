from governance.contract import RevealAuthorizationRequest
from governance.doorway import authorize_reveal

request = RevealAuthorizationRequest(
    requester_id="test-user",
    asset_id="test-asset",
)

result = authorize_reveal(request)

print(result.model_dump())
