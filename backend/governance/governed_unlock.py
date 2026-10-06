from __future__ import annotations

from typing import Any, Callable, Dict, List


def execute_governed_unlock(
    *,
    user: Dict[str, Any],
    photo: Dict[str, Any],
    unlocks_db: List[Dict[str, Any]],
    authorization: Dict[str, Any],
    unlock_id_factory: Callable[[], str],
    timestamp_factory: Callable[[], Any],
) -> Dict[str, Any]:

    if not authorization.get("allowed", False):
        raise PermissionError(
            authorization.get(
                "denial_reason",
                "Reveal authorization denied",
            )
        )

    price = photo["price_tokens"]

    if user["token_balance"] < price:
        raise ValueError("Not enough tokens")

    original_balance = user["token_balance"]
    original_length = len(unlocks_db)

    try:
        user["token_balance"] -= price

        unlocks_db.append(
            {
                "id": unlock_id_factory(),
                "user_id": user["id"],
                "photo_id": photo["id"],
                "tokens_spent": price,
                "created_at": timestamp_factory(),
                "governance_chain_hash": (
                    authorization.get("receipt") or {}
                ).get("governance_chain_hash"),
            }
        )

    except Exception:
        user["token_balance"] = original_balance
        del unlocks_db[original_length:]
        raise

    return {
        "detail": "Unlocked",
        "token_balance": user["token_balance"],
        "governance": authorization,
    }
