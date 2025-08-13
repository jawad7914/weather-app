import jwt
import os
from functools import wraps
from flask import request, jsonify
from datetime import datetime, timezone, timedelta

# Load from environment (never hardcode secrets)
SECRET_KEY = os.getenv("JWT_SECRET", "dev_secret_key")  # fallback for dev
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

def generate_jwt(payload, hours_valid=12):
    """
    Generate a JWT token with expiration.
    """
    payload_with_exp = {
        **payload,
        "exp": int((datetime.now(timezone.utc) + timedelta(hours=hours_valid)).timestamp())
    }
    token = jwt.encode(payload_with_exp, SECRET_KEY, algorithm=ALGORITHM)
    # Ensure we return a string
    if isinstance(token, bytes):
        token = token.decode("utf-8")

    return token

def verify_jwt(token):
    """
    Verify a JWT token and return the decoded payload if valid.
    """
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}

def token_required(f):
    """
    Decorator to protect routes with JWT authentication.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Authorization header is missing"}), 401

        try:
            token = auth_header.split(" ")[1]  # Expecting "Bearer <token>"
        except IndexError:
            return jsonify({"error": "Invalid Authorization header format"}), 401

        decoded = verify_jwt(token)
        if "error" in decoded:
            return jsonify(decoded), 401

        request.user = decoded  # attach decoded payload (e.g., username, id)
        return f(*args, **kwargs)
    return decorated
