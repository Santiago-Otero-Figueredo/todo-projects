from fastapi import FastAPI, Request, Depends
from jinja2 import Environment, FileSystemLoader
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


from starlette.middleware.authentication import AuthenticationMiddleware

from apps.users.routers import guest_router as guest_router
from apps.users.routers import user_router as user_router

from apps.auth.routers import router as auth_router

from apps.projects.routers.priorities import router as priority_router

import os
# from core.db import get_new_session, create_tables


# from routers import auth

# from tables.projects.priorities import Priority
# from tables.users.user import User

# create_tables()

app = FastAPI()
app.include_router(guest_router)
app.include_router(user_router)
app.include_router(auth_router)

app.include_router(priority_router)

app.mount("/static", StaticFiles(directory="static"), name="static")

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
env = Environment(loader=FileSystemLoader(template_dir), auto_reload=True)

templates = Jinja2Templates(directory='templates')
# Add Middleware

# app.mount("/static", StaticFiles(directory="static"), name="static")

# app.include_router(auth.router)


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')








# @app.get('/')
# async def name(request: Request, token: str = Depends(oauth2_scheme)):
#     prioridades = []
#     with get_new_session() as session:
#         prioridades = session.query(Priority).all()
#     return templates.TemplateResponse('projects/registro.html', {'request':request, 'prioridades': prioridades})



# # Crear una sesión
# if False:
#     User.registro(username='admin', email='admin@gmail.com', password='contrasena123')

# # Crear una sesión
# if False:
#     Priority.registro(name='Alta', level=1, color='#FF0000')
#     Priority.registro(name='Media', level=2, color='#FFFF00')
#     Priority.registro(name='Baja', level=3, color='#0000FF')