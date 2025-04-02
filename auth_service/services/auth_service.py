import redis
import json
from datetime import timedelta
from flask_jwt_extended import create_access_token
from config import Config

# 初始化 Redis
redis_client = redis.StrictRedis.from_url(Config.REDIS_URL, decode_responses=True)

class AuthService:

    @staticmethod
    def authenticate_user(username, password):
        """模拟用户身份验证，实际应用中可以连接数据库"""
        # 假设用户名是 "admin" 且密码是 "password"
        if username == "admin" and password == "password":
            return {"username": username, "role": "admin"}
        return None

    @staticmethod
    def create_access_token(user_data):
        """根据用户信息生成 JWT Token"""
        return create_access_token(identity=user_data['username'], fresh=True)

    @staticmethod
    def store_token_in_redis(token, user_data):
        """将生成的 token 存储到 Redis 中"""
        redis_client.setex(token, timedelta(seconds=Config.JWT_ACCESS_TOKEN_EXPIRES), json.dumps(user_data))
        return True

    @staticmethod
    def get_user_data_from_redis(token):
        """从 Redis 获取用户信息"""
        user_data = redis_client.get(token)
        if user_data:
            return json.loads(user_data)
        return None
