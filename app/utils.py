# app/utils.py
from jose import jwt, JWTError
from functools import wraps
from flask import request, jsonify
from datetime import datetime, timezone, timedelta

SECRET_KEY = "your-secret-key"  # change this to something strong

def encode_token(customer_id):
    payload = {
        "sub": str(customer_id),
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.customer_id = int(data["sub"])
        except JWTError:
            return jsonify({"error": "Invalid or expired token"}), 401

        return f(*args, **kwargs)
    return decorated
