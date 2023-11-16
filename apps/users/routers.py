from fastapi import APIRouter, status, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .schemas import CreateUserRequest
from .models import User

from core.database import get_session
from core.security import oauth2_scheme



guest_router = APIRouter(
    prefix='/users',
    tags=['Users'],
    responses= {404: {'description': 'Not Found'}}
)

user_router = APIRouter(
    prefix='/users',
    tags=['Users'],
    responses= {404: {'description': 'Not Found'}},
    dependencies=[Depends(oauth2_scheme)]
)


@guest_router.post('', status_code=status.HTTP_201_CREATED)
async def register(data: CreateUserRequest, db: Session = Depends(get_session)):
    await User.register_account(data=data, db=db)
    payload = {"message": "User account has been successfully created."}
    return JSONResponse(content=payload)


@user_router.post('/me', status_code=status.HTTP_200_OK)
def get_user_detail(request: Request):
    return request.user