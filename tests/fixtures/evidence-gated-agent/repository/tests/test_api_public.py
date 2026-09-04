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
    assert set(profile) == {"id", "display_name", "email", "created_at"}
    assert "phone_number" not in profile