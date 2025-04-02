from flask import jsonify, request
from services.auth_service import AuthService

class AuthController:

    @staticmethod
    def login():
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        print("email", email)
        user = AuthService.authenticate_user(email, password)
        if not user:
            return jsonify({"message": "Invalid credentials"}), 401
        
        token = AuthService.create_access_token(user)
        AuthService.store_token_in_redis(token, user)

        return jsonify({"access_token": token}), 200

    @staticmethod
    def verify_token():
        token = request.headers.get("Authorization").split()[1]
        user_data = AuthService.get_user_data_from_redis(token)

        if user_data:
            return jsonify({"message": "Token is valid", "user": user_data}), 200
        else:
            return jsonify({"message": "Invalid or expired token"}), 401
