"""Public-facing API handlers. Endpoints here are documented in docs/api.md
and consumed by the mobile app and the partner integration (see docs/api.md).
"""

from src.utils import with_retry


def get_user_profile(directory_client, user_id):
    """GET /v1/users/{id}

    Returns the public user profile contract documented in docs/api.md.
    """

    def _fetch():
        return directory_client.fetch(user_id)

    record = with_retry(_fetch, max_attempts=2)
    return {
        "id": record["id"],
        "display_name": record["display_name"],
        "email": record["email"],
        "created_at": record["created_at"],
        "phone_number": record.get("phone_number"),
    }
