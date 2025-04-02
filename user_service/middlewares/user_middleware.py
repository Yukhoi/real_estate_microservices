from functools import wraps
from flask import request, jsonify
from datetime import datetime
import re

def validate_body(required_fields):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                return jsonify({"error": "Invalid Content-Type. Expected application/json"}), 400

            data = request.get_json()
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
            
            if "birth_date" in data:
              try:
                  datetime.strptime(data["birth_date"], "%Y-%m-%d")
              except ValueError:
                  return jsonify({"error": "Invalid date format for 'birth_date'. Expected format: YYYY-MM-DD"}), 400
              
            if "email" in data:
                email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_regex, data["email"]):
                    return jsonify({"error": "Invalid email format"}), 400            

            return func(*args, **kwargs)
        return wrapper
    return decorator