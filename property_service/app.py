from flask import Flask
from config import Config
from models.db import db
from routes.property_routes import property_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(property_bp, url_prefix="/properties")

if __name__ == "__main__":
    app.run(debug=True, port=5003)
