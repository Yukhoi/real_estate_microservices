from flask import Flask
from config import Config
from models.db import db
from routes.property_routes import property_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(property_bp, url_prefix='/properties')

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    print("Starting the Flask server on http://127.0.0.1:5003...")
    app.run(host="0.0.0.0",port=5003, debug=True)
