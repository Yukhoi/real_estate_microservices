import os

class Config:
    REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")  
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret-key")  
    JWT_ACCESS_TOKEN_EXPIRES = 3600  
