from fastapi import APIRouter, status, Depends, Header
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from core.database import get_session

from apps.users.models import User

router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
    responses= {404: {'description': 'Not Found'}}
)

@router.post('/register', status_code=status.HTTP_201_CREATED, name='register-user')
async def authenticate_user(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    pass

@router.get('/login', status_code=status.HTTP_200_OK, name='login')
async def authenticate_user(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    pass

@router.post('/forgot-password', status_code=status.HTTP_200_OK, name='forgot-password')
async def refresh_access_token(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    pass

@router.post('/reset-password', status_code=status.HTTP_200_OK, name='reset-password')
async def refresh_access_token(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    pass