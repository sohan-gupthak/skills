# High-risk domain evidence

Use this reference only while building a high-risk evidence contract for one of these domains. It supplements the universal protocol; add any decision-relevant claim not listed here.

## Public API / contract changes

Establish the current contract, known consumers, compatibility policy, and tests that exercise the changed surface. A handler unit test does not establish that no consumer depends on a removed field.

## Authentication and authorization

Establish the current authentication/session flow and authorization boundary, failure behavior for invalid, expired, and missing credentials, token/session invalidation semantics when relevant, and the privilege-escalation surface.

## Payments and financial operations

Establish the transaction flow, provider semantics for idempotency, retries, and webhook delivery, duplicate-charge/double-processing prevention, and failed or partial-operation state with recovery.

## Schema migrations and destructive operations

Establish reversibility with an exercised rollback path, the data-loss and recovery surface, partial-failure safety, and blast radius for other systems using the resource.
