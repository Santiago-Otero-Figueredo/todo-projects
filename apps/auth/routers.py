from fastapi import APIRouter, status, Depends, Header
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from config.database import get_session
