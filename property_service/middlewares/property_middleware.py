from flask import request, jsonify
from functools import wraps

def jwt_required_middleware(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization").split()[1]
        if not token:
            return jsonify({"error": "JWT token is required"}), 401
        return func(*args, **kwargs)
    return wrapper