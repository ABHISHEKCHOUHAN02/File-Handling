import os
from datetime import datetime, timedelta, timezone

import jwt


JWT_SECRET = os.getenv("JWT_SECRET", "change-this-jwt-secret")
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = 1


def create_login_token(emp_id, email):
    issued_at = datetime.now(timezone.utc)
    payload = {
        "sub": emp_id,
        "email": email,
        "iat": issued_at,
        "exp": issued_at + timedelta(hours=JWT_EXPIRY_HOURS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_login_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError:
        return None
