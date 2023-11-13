from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

import os

env_path = Path('.') / ".env"
load_dotenv(dotenv_path=env_path, override=True)

class Settings(BaseSettings):

    # App
    APP_NAME:  str = os.environ.get("APP_NAME", "FastAPI")
    DEBUG: bool = bool(os.environ.get("DEBUG", False))

    # FrontEnd Application
    FRONTEND_HOST: str = os.environ.get("FRONTEND_HOST", "http://localhost:5500")

    # Postgres Database settings
    ENGINE: str = os.getenv('ENGINE')
    NAME: str = os.getenv('NAME')
    USER: str = os.getenv('USER')
    PASSWORD: str = os.getenv('PASSWORD')
    HOST: str = os.getenv('HOST')
    PORT: str = os.getenv('PORT')
    DATABASE_URL: str  = os.getenv('DATABASE_URL')

    # JWT Secret Key
    JWT_SECRET: str = os.environ.get("JWT_SECRET", "649fb93ef34e4fdf4187709c84d643dd61ce730d91856418fdcf563f895ea40f")
    JWT_ALGORITHM: str = os.environ.get("ACCESS_TOKEN_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 3))
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES", 1440))

    # App Secret Key
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "8deadce9449770680910741063cd0a3fe0acb62a8978661f421bbcbb66dc41f1")

    # Email Context
    USER_VERIFY_ACCOUNT: str = os.environ.get("USER_VERIFY_ACCOUNT", "verify-account")
    FORGOT_PASSWORD: str = os.environ.get("USER_VERIFY_ACCOUNT", "password-reset")

    EMAIL_TEMPLATE_FOLDER: str = os.environ.get("EMAIL_TEMPLATE_FOLDER", "templates")


@lru_cache()
def get_settings() -> Settings:
    return Settings()