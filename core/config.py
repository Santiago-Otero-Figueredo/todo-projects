from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

import os

env_path = Path('.') / ".env"
load_dotenv(dotenv_path=env_path, override=True)

class Settings(BaseSettings):
    ENGINE: str = os.getenv('ENGINE')
    NAME: str = os.getenv('NAME')
    USER: str = os.getenv('USER')
    PASSWORD: str = os.getenv('PASSWORD')
    HOST: str = os.getenv('HOST')
    PORT: str = os.getenv('PORT')
    DATABASE_URL: str  = os.getenv('DATABASE_URL')

    #JWT
    JWT_SECRET: str = os.getenv('JWT_SECRET', 'kdkawuihi3j78278f8990i9cvi29i883498238fuffuiajkjdlwj')
    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM', 'HS256')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv('JWT_TOKEN_EXPIRE_MINUTES', 60)



def get_settings() -> Settings:
    return Settings()
