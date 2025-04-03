import os

class Config:
    RABBITMQ_HOST = "rabbitmq" 
    REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")  
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "d45ef6c8d03e1cfeaf835b036e80bef3808305fbd3b298671d500d7258af8314")  
    JWT_ACCESS_TOKEN_EXPIRES = 3600  
