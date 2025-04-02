from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from routes.auth_routes import auth_bp

app = Flask(__name__)
app.config.from_object(Config)

# 初始化 JWT 管理器
jwt = JWTManager(app)

# 注册路由
app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True, port=5002)
