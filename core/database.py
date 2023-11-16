
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from typing import Generator
from core.config import get_settings


settings = get_settings()

# Configuración de la base de datos (PostgreSQL)
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=0
)

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine, checkfirst=True)

def get_session() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()