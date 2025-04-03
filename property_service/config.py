import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/property_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
