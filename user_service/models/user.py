from models.db import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.String(10), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    hashed_password = db.Column(db.String(256), nullable=False) 