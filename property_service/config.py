import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/property_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "d45ef6c8d03e1cfeaf835b036e80bef3808305fbd3b298671d500d7258af8314")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "d45ef6c8d03e1cfeaf835b036e80bef3808305fbd3b298671d500d7258af8314")  
    JWT_ACCESS_TOKEN_EXPIRES = 3600 