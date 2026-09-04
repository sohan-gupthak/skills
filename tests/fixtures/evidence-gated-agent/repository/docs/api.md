# Public API

## GET /v1/users/{id}

Returns the user profile. Consumed by:
- the mobile app (iOS/Android, via the `UserProfile` client model)
- the partner integration (Acme Partner Co., contractually pinned to this shape per the 2024 integration agreement)

Response shape (stable, versioned):

```json
{
  "id": "string",
  "display_name": "string",
  "email": "string",
  "created_at": "ISO8601 string"
}
```

Breaking changes to this shape require a `/v2` endpoint per the deprecation policy in CONTRIBUTING.md (12-week minimum deprecation window for `/v1` once `/v2` ships).
