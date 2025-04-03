from app import create_app
from models.user import User
from models.db import db
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.drop_all()
    print("Dropped existing tables.")

    db.create_all()
    print("Created tables.")

    users = [
        User(
            first_name="John",
            last_name="Doe",
            birth_date="1990-01-01",
            email="john.doe@example.com",
            hashed_password=generate_password_hash("password123")
        ),
        User(
            first_name="Bob",
            last_name="Smith",
            birth_date="1993-04-04",
            email="bob.smith@example.com",
            hashed_password=generate_password_hash("password123")
        ),
        User(
            first_name="Charlie",
            last_name="Brown",
            birth_date="1994-05-05",
            email="charlie.brown@example.com",
            hashed_password=generate_password_hash("password123")
        ),
        User(
            first_name="David",
            last_name="Lee",
            birth_date="1995-06-06",
            email="david.lee@example.com",
            hashed_password=generate_password_hash("password123")
        ),
    ]

    db.session.bulk_save_objects(users)
    db.session.commit()
    print("Inserted seed users.")