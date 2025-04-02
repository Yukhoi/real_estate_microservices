from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from routes.user_routes import user_bp
    app.register_blueprint(user_bp, url_prefix='/users')

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    print("Starting the Flask server on http://127.0.0.1:5001...")
    app.run(host="0.0.0.0",port=5001, debug=True)