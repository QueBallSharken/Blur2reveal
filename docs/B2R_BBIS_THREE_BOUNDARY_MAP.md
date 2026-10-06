# B2R BBIS THREE-BOUNDARY MAP

## Status

PARTIAL / UNPROVEN

This document maps the current Blur2reveal implementation against the
BBIS Three-Boundary Refinement.

It does not claim strong BBIS conformance.

---

## 1. Claimed Action

Primary action:

`photo reveal / unlock`

Current application path:

`POST /unlock`
-> governance authorization
-> token balance mutation
-> unlock authorization mutation
-> subsequent `/photos/{photo_id}` request may expose `original_url`

---

## 2. Local Refusal Boundary

### Identified

Boundary:

`backend/governance/doorway.py::authorize_reveal`

The doorway evaluates:

- GDP governance validity
- AIC invariant lineage
- BEAF boundary evidence
- DTPE authorization result
- governance evidence-chain validity

Current refusal points include:

- governance validation failure
- invariant lineage failure
- critical boundary evidence
- DTPE authorization failure
- governance evidence-chain failure

### Actor

B2R governance doorway.

### Current assessment

LOCAL REFUSAL BOUNDARY: IDENTIFIED

The doorway is a concrete refusal-capable decision point before the
current `/unlock` mutation sequence.

---

## 3. System-Wide Refusal Boundary

### Status

NOT PROVEN

Current `/unlock` does not call the governance doorway.

After authorization, the application performs:

`user["token_balance"] -= price`

followed by:

`unlocks_db.append(...)`

There is currently no demonstrated re-evaluation of the governing
invariant at these downstream mutation-capable boundaries.

There is also no demonstrated mechanism showing that an already-approved
request can still be refused if authority, identity, state, or governing
conditions change before the mutation completes.

### Current assessment

SYSTEM-WIDE REFUSAL BOUNDARY: UNPROVEN

Therefore strong BBIS continuity must not be claimed.

---

## 4. True Irreversible Mutation Authority

### Status

UNRESOLVED

The current `/unlock` path contains at least two mutation-capable
operations:

1. `user["token_balance"] -= price`
2. `unlocks_db.append(...)`

The claimed reveal scope also depends on the downstream behavior of:

`GET /photos/{photo_id}`

which returns `original_url` when an unlock record exists.

Therefore the implementation must distinguish:

- economic mutation authority
- unlock-state mutation authority
- actual reveal/release authority

The system must not assume that the doorway authorization itself is
the true irreversible mutation authority.

### Current assessment

TRUE IRREVERSIBLE MUTATION AUTHORITY: TBD

---

## 5. Governing Invariant

Current candidate evidence stack:

- GDP: structural governance sufficiency
- AIC: invariant lineage
- BEAF: boundary evidence
- DTPE: governed execution proof
- SPECTRE-FST: bounded Fundamental Stress Testing evidence

These systems remain distinct.

FST is evidence/hardening, not enforcement.

DTPE receipts remain authoritative DTPE receipts.

B2R may correlate subsystem evidence but must not semantically fuse
independent receipt meanings.

---

## 6. Required BBIS Trace

B2R must eventually produce a per-action trace containing:

### Point 1 — Local Refusal Boundary

- actor
- boundary identifier
- invariant identity
- invariant evaluation
- refusal capability
- ordering/timing marker

### Point 2 — System-Wide Refusal Boundary

- actor
- boundary identifier
- invariant identity
- invariant evaluation
- refusal capability
- ordering/timing marker

### Point 3 — True Irreversible Mutation Authority

- actor or primitive identifier
- boundary identifier
- whether mutation remained preventable immediately beforehand
- whether the governing invariant remained live
- final allow/deny/downgrade/unverifiable result
- ordering/timing marker

---

## 7. Current BBIS Classification

### LOCAL

Identified.

### SYSTEM-WIDE

Not proven.

### TRUE MUTATION AUTHORITY

Not resolved.

### OVERALL

PARTIAL / UNPROVEN

No strong BBIS claim is permitted at this stage.

---

## 8. Immediate Design Rule

Do not integrate the real DTPE execution path yet.

First resolve:

1. what exactly is being claimed as the protected reveal scope
2. every mutation-capable boundary in that scope
3. the system-wide refusal point
4. the true irreversible mutation authority
5. how the governing invariant remains live and refusal-capable through
   those boundaries

Only after those are mechanically defined should DTPE execution
integration be completed.

---

## 9. Non-Claim

B2R currently has a governance doorway.

It does NOT yet demonstrate full BBIS continuity through the complete
unlock/reveal mutation path.

The correct claim is:

`BBIS partial / boundary analysis in progress`

not:

`BBIS holds`

---

## 10. Final Rule

The doorway is not automatically the end of governance.

The same governing invariant must remain live, binding, and
refusal-capable across every mutation-capable boundary in the claimed
path until the true irreversible primitive for that scope.

If that cannot be demonstrated, the stronger continuity claim does not
survive.

---

## 11. REVEAL PATH RECONNAISSANCE — 2026-10-04

The current implementation exposes a compound path:

`POST /unlock`
-> token balance mutation
-> unlock authorization-state mutation
-> `GET /photos/{photo_id}`
-> original asset URL disclosure

### Mutation-Capable Boundary 1

`user["token_balance"] -= price`

This mutates economic/account state.

### Mutation-Capable Boundary 2

`unlocks_db.append(...)`

This mutates authorization state and establishes the condition used by
the later photo retrieval path.

### Reveal / Disclosure Primitive

`GET /photos/{photo_id}` returns:

`original_url`

when the requester has a matching unlock record.

For the claimed scope of protecting the actual asset reveal, this
response is the current candidate for the true irreversible disclosure
primitive because disclosure of the original asset location cannot be
reliably undone after the recipient receives it.

The unlock record itself is therefore treated as authorization-state
mutation, not automatically as the final irreversible reveal primitive.

### Critical Finding

`POST /unlock` currently does NOT invoke:

`governance.doorway.authorize_reveal(...)`

Therefore the current governance doorway is not yet mechanically placed
in the actual mutation/reveal path.

### BBIS Consequence

The current implementation does not demonstrate that the same governing
invariant remains live, binding, and refusal-capable across:

1. token balance mutation
2. unlock authorization-state mutation
3. final original-asset disclosure

The system-wide refusal boundary therefore remains unproven.

### Required Future Architecture

The governance decision must become part of the actual controlled path,
and the governing invariant must remain enforceable through every
mutation-capable boundary before the true disclosure primitive.

No strong BBIS claim is permitted until that continuity is mechanically
demonstrated.

### Important Scope Distinction

B2R must distinguish:

- economic mutation
- authorization-state mutation
- actual information disclosure

These may have different irreversible characteristics and must not be
collapsed into one generic "unlock" event.
