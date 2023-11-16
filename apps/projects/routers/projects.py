from fastapi import APIRouter, status, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from core.database import get_session
from core.security import oauth2_scheme

from apps.projects.models import Project

guest_router = APIRouter(
    prefix='/projects',
    tags=['projects'],
    responses= {404: {'description': 'Not Found'}}
)

