from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .schemas import CreateUserRequest
from .models import User
from core.database import get_db


router = APIRouter(
    prefix='/users',
    tags=['Users'],
    responses= {404: {'description': 'Not Found'}}
)

@router.post('', status_code=status.HTTP_201_CREATED)
async def register(data: CreateUserRequest, db: Session = Depends(get_db)):
    await User.register_account(data=data, db=db)
    payload = {"message": "User account has been successfully created."}
    return JSONResponse(content=payload)