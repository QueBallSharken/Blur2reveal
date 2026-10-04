from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class RevealAuthorizationRequest(BaseModel):
    requester_id: str
    asset_id: str
    action: str = "reveal"

    governance_context: Dict[str, Any] = Field(default_factory=dict)


class RevealAuthorizationResult(BaseModel):
    allowed: bool

    governance_result: Dict[str, Any] = Field(default_factory=dict)

    receipt: Optional[Dict[str, Any]] = None

    denial_reason: Optional[str] = None

    crypto_profile: Optional[str] = None
    policy_version: Optional[str] = None
    policy_state_hash: Optional[str] = None