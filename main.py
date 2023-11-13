from fastapi import FastAPI, Request, Depends, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session


from starlette.middleware.authentication import AuthenticationMiddleware

from apps.users.routers import guest_router as guest_router
from apps.users.routers import user_router as user_router
from apps.users.routers import auth_router as auth_router


from config.security import get_current_user

from config.database import get_session


# from routers import auth

from apps.projects.priorities import Priority
# from tables.users.user import User


# create_tables()



app = FastAPI()
app.include_router(guest_router)
app.include_router(user_router)
app.include_router(auth_router)


templates = Jinja2Templates(directory='templates')

# Add Middleware

# app.mount("/static", StaticFiles(directory="static"), name="static")

# app.include_router(auth.router)

# templates = Jinja2Templates(directory='templates')

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')








@app.get('/priorities', status_code=status.HTTP_200_OK)
async def prioridades(request: Request, user = Depends(get_current_user), session: Session = Depends(get_session)):
    prioridades = Priority.get_all(session)
    return templates.TemplateResponse('projects/home.html', {'request':request, 'prioridades': prioridades, 'user': user})



# # Crear una sesión
# if False:
#     User.registro(username='admin', email='admin@gmail.com', password='contrasena123')

# # Crear una sesión
# if False:
#     Priority.registro(name='Alta', level=1, color='#FF0000')
#     Priority.registro(name='Media', level=2, color='#FFFF00')
#     Priority.registro(name='Baja', level=3, color='#0000FF')