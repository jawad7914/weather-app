import jwt
import os
from functools import wraps
from flask import request, jsonify

# Load from environment (never hardcode secrets)
SECRET_KEY = os.getenv("JWT_SECRET", "dev_secret_key")  # fallback for dev
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

def generate_jwt(payload):
    """
    Generate a JWT token.
    """
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_jwt(token):
    """
    Verify a JWT token and return (decoded_payload, error_message).
    """
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded, None
    except jwt.ExpiredSignatureError:
        return None, "Token expired"
    except jwt.InvalidTokenError:
        return None, "Invalid token"

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

        decoded, error = verify_jwt(token)
        if error:
            return jsonify({"error": error}), 401

        request.user = decoded  # attach decoded payload (e.g., username, id)
        return f(*args, **kwargs)
    return decorated
