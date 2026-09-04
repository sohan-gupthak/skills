from src.api.public import get_user_profile


class FakeDirectory:
    def fetch(self, user_id):
        return {
            "id": user_id,
            "display_name": "Ada Lovelace",
            "email": "ada@example.com",
            "created_at": "2020-01-01T00:00:00Z",
            "phone_number": "+1-555-0100",
            "internal_risk_score": 0.02,
        }


def test_get_user_profile_shape():
    profile = get_user_profile(FakeDirectory(), "u_1")
    assert set(profile.keys()) == {"id", "display_name", "email", "created_at", "phone_number"}
    assert profile["display_name"] == "Ada Lovelace"


class UnverifiedDirectory:
    def fetch(self, user_id):
        return {
            "id": user_id,
            "display_name": "No Phone User",
            "email": "nophone@example.com",
            "created_at": "2021-01-01T00:00:00Z",
            # no phone_number key - unverified user, per docs/directory-client.md
        }


def test_get_user_profile_handles_missing_phone_number():
    """Regression test for the post-change contradiction found during
    verification: users without a verified phone number have no
    phone_number key in the directory record at all. The profile must
    still return the field (as None), not raise KeyError."""
    profile = get_user_profile(UnverifiedDirectory(), "u_2")
    assert profile["phone_number"] is None
