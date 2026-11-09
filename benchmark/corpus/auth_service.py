"""
Authentication and session management module.
"""
import hmac
import hashlib

class AuthService:
    def __init__(self, secret_key: bytes):
        self.secret_key = secret_key

    # TODO(AUTH-101): remove deprecated sha1 fallback once migration completes
    def verify_token(self, token: str, signature: str) -> bool:
        expected = hmac.new(self.secret_key, token.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)

    def refresh_session(self, session_id: str):
        # TODO(SEC-606): rotate session key on refresh
        print(f"Refreshing session {session_id}")
