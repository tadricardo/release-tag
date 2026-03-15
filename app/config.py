import os
from datetime import timedelta


# from loadotenv import load_env
# load_env()
class Config:
    USER = os.getenv("USER")
    PASSWORD = os.getenv("PASSWORD")
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_CSRF_PROTECT = True
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{USER}:{PASSWORD}@localhost:3307/db_test"
    )
