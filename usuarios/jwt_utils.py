import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings


def generate_jwt(user_id):
    payload = {
        "user_id": user_id,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc)
        + timedelta(hours=getattr(settings, "JWT_EXPIRATION_HOURS", 2)),
    }
    return jwt.encode(
        payload, getattr(settings, "JWT_SECRET_KEY", ""), algorithm="HS256"
    )


def decode_jwt(token):
    try:
        payload = jwt.decode(
            token, getattr(settings, "JWT_SECRET_KEY", ""), algorithms=["HS256"]
        )
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
