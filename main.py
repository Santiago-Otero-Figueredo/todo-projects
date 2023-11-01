from config.db import Base, SessionLocal, engine, session

from models.base import ModeloBase, ModeloDetalle
from models.projects.projects import Project



Base.metadata.create_all(bind=engine, checkfirst=True)

# Crear una sesión
db = SessionLocal()