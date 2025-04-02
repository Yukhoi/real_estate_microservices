from flask import jsonify, request
from services.auth_service import AuthService

class AuthController:

    @staticmethod
    def login():
        """处理用户登录请求"""
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        user = AuthService.authenticate_user(username, password)
        if not user:
            return jsonify({"message": "Invalid credentials"}), 401
        
        token = AuthService.create_access_token(user)
        AuthService.store_token_in_redis(token, user)

        return jsonify({"access_token": token}), 200

    @staticmethod
    def verify_token():
        """验证 Token 是否有效"""
        token = request.headers.get("Authorization").split()[1]
        user_data = AuthService.get_user_data_from_redis(token)

        if user_data:
            return jsonify({"message": "Token is valid", "user": user_data}), 200
        else:
            return jsonify({"message": "Invalid or expired token"}), 401
