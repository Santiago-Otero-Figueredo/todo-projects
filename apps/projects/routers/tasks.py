from fastapi import APIRouter, status, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from core.database import get_session
from core.security import oauth2_scheme

from apps.projects.models import Task

guest_router = APIRouter(
    prefix='/tasks',
    tags=['tasks'],
    responses= {404: {'description': 'Not Found'}}
)

