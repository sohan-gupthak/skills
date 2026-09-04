"""Login and session handling."""

import hashlib
import secrets
import time

SESSION_TTL_SECONDS = 3600


def login(user_store, session_store, username, password):
    user = user_store.get_by_username(username)
    if user is None:
        return None
    if hashlib.sha256(password.encode()).hexdigest() != user["password_hash"]:
        return None
    token = secrets.token_hex(32)
    session_store.set(token, {"user_id": user["id"], "expires_at": time.time() + SESSION_TTL_SECONDS})
    return token


def get_current_user(session_store, token):
    session = session_store.get(token)
    if session is None:
        return None
    if session["expires_at"] < time.time():
        return None
    return session["user_id"]
