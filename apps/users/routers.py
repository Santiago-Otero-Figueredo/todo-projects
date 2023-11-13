from fastapi import APIRouter, status, Request, Form, Depends, Header, Query
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from fastapi.templating import Jinja2Templates

from config.database import get_session
from config.security import oauth2_scheme, get_current_user

from .schemas import CreateUserRequest, EmailRequest, ResetRequest
from .models import User
from .responses import UserResponse, LoginResponse
from .forms import UserCreateForm, UserLoginForm

templates = Jinja2Templates(directory='templates/auth/')


user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


auth_router = APIRouter(
    prefix='/users',
    tags=['Users'],
    responses= {404: {'description': 'Not Found'}},
    dependencies=[Depends(oauth2_scheme), Depends(get_current_user)]
)

guest_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description": "Not found"}},
)

@user_router.get('/register', response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse('register.html', {'request':request})

@user_router.post('/register', status_code=status.HTTP_201_CREATED, response_class=HTMLResponse)
async def register(request: Request, email: str = Form(...), password: str = Form(...), session: Session = Depends(get_session)):

    form = UserCreateForm(request)
    await form.load_data()
    data = CreateUserRequest(
        email=email,
        password=password
    )

    if await form.is_valid():
        errors = ["Save to database"]
        await User.create_account(data=data, session=session)
    else:
        errors = form.errors

    print(request.form)

    return templates.TemplateResponse('register.html', {'request': request, 'errors': errors})



    # await User.create_account(data=data, session=session)
    # payload = {"message": "User account has been successfully created."}
    # return JSONResponse(content=payload)

@user_router.get('/verify', status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def verify_user_account(request: Request,
                              token: str = Query (..., description="Token de verificación"),
                              email: str = Query (..., description="Correo electrónico"),
                              session: Session = Depends(get_session)):
    await User.active_user_account(email=email, token=token, session=session)
    return templates.TemplateResponse('account_verification.html', {'request': request})
    #return JSONResponse({"message": "Account is activated successfully."})

@guest_router.get("/login", response_class=HTMLResponse, name="user_login")
async def user_login(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@guest_router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse, name="user_login")
async def user_login(request: Request, email: str = Form(...), password: str = Form(...), session: Session = Depends(get_session)):
    form = UserLoginForm(request)
    await form.load_data()
    data = CreateUserRequest(
        email=email,
        password=password
    )

    if await form.is_valid():
        User.get_login_token(data, session)
        # Redireccionar a otra API después de que el formulario sea válido
        return RedirectResponse(url="/priorities", status_code=status.HTTP_303_SEE_OTHER)
    else:
        errors = form.errors


    return templates.TemplateResponse('login.html', {'request': request, 'errors': errors})

    #return await User.get_login_token(data, session)

@guest_router.post("/refresh", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def refresh_token(r_token = Header(), session: Session = Depends(get_session)):

    return await User.get_refresh_token(r_token, session)



@guest_router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(data: EmailRequest, session: Session = Depends(get_session)):
    await User.email_forgot_password_link(data, session)
    return JSONResponse({"message": "A email with password reset link has been sent to you."})

@guest_router.put("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(data: ResetRequest, session: Session = Depends(get_session)):
    await User.reset_user_password(data, session)
    return JSONResponse({"message": "Your password has been updated."})


@auth_router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def fetch_user(user = Depends(get_current_user)):
    return user
