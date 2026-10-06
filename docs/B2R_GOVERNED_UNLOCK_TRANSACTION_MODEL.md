# B2R GOVERNED UNLOCK TRANSACTION MODEL

## Purpose

Define the governed transaction path for a photo reveal before
integrating the canonical DTPE execution runtime.

This document is an implementation contract, not a claim of completed
BBIS conformance.

---

## 1. Claimed Scope

The protected action is:

`authenticated requester obtains access to the original photo asset`

The scope includes:

`POST /unlock`
through
`GET /photos/{photo_id}`

---

## 2. Governing Invariant

The governing invariant must remain:

- live
- binding
- refusal-capable

through every mutation-capable boundary in the claimed path until the
true irreversible disclosure primitive.

The invariant must have a stable action-scoped identity.

---

## 3. Action Identity

The governed action must uniquely bind:

- requester identity
- asset identity
- action
- authorization context
- governing invariant identity

The B2R `asset_id` must not be treated as a DTPE sequence identifier.

---

## 4. Boundary Sequence

### Boundary 1 — Local Refusal

`governance.doorway.authorize_reveal`

Purpose:

Evaluate whether the requested reveal is eligible to proceed.

Refusal owner:

B2R governance doorway.

---

### Boundary 2 — System-Wide Refusal

Status:

TO BE IMPLEMENTED AND PROVEN.

This boundary must remain capable of refusing the governed action after
initial authorization but before irreversible mutation/release.

It must cover the complete controlled mutation path.

---

### Boundary 3 — Economic Mutation

Current primitive:

`user["token_balance"] -= price`

This changes economic state.

The governed action must not proceed past this point unless the
required refusal authority remains valid immediately beforehand.

---

### Boundary 4 — Unlock-State Mutation

Current primitive:

`unlocks_db.append(...)`

This establishes authorization state used by the later reveal path.

This is a mutation-capable boundary and must remain inside the governed
transaction scope.

---

### Boundary 5 — True Irreversible Disclosure

Current candidate:

`GET /photos/{photo_id}` returning `original_url`.

This is currently the strongest candidate for the true irreversible
primitive for the claimed information-disclosure scope.

The classification remains subject to implementation verification.

---

## 5. Atomicity Requirement

The economic mutation and unlock-state mutation must not create an
uncontrolled partial state.

The implementation must establish a transaction strategy such that:

- failure before mutation leaves state unchanged
- failure between mutation boundaries is detected and controlled
- unauthorized downstream execution cannot continue
- the governing action identity remains bound to the mutation

---

## 6. Refusal Requirement

A prior authorization result must not be treated as sufficient proof that
all later mutation boundaries are automatically governed.

The implementation must define how refusal remains mechanically
effective through the controlled path.

---

## 7. Evidence Requirement

The transaction should eventually produce a per-action trace containing:

- action identity
- claimed scope
- invariant identity
- local refusal result
- system-wide refusal result
- economic mutation result
- unlock mutation result
- disclosure authorization result
- final outcome
- ordering markers
- authoritative subsystem receipts where applicable

Evidence correlation must preserve subsystem meaning.

---

## 8. DTPE Boundary

Canonical DTPE execution evidence will eventually be integrated at the
appropriate governed execution boundary.

B2R must consume the canonical DTPE receipt.

B2R must not manufacture a replacement DTPE receipt.

No simulated PQC profile is a canonical cryptographic claim.

---

## 9. SPECTRE-FST Boundary

SPECTRE-FST remains bounded Fundamental Stress Testing evidence.

It is not the enforcement mechanism.

Its evidence may contribute to assurance decisions without replacing
live refusal authority.

---

## 10. BBIS Classification

Current state:

`PARTIAL / UNPROVEN`

This document defines the target transaction structure.

It does not establish strong BBIS conformance.

Strong BBIS requires mechanical demonstration that the governing
invariant remains live, binding, and refusal-capable across the complete
claimed path until the true irreversible primitive.

---

## 11. Implementation Rule

Do not add the real DTPE runtime until this transaction model has been
implemented and its mutation boundaries can be tested independently.

The doorway must become part of the actual `/unlock` control path.

The implementation must then prove that no uncontrolled path reaches the
claimed reveal primitive.

---

## 12. Final Rule

Govern the transaction, not merely the authorization decision.

The protected path is the entire path from governed request through
mutation to irreversible disclosure.
