from fastapi import APIRouter, status, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse

from sqlalchemy.orm import Session

from fastapi.templating import Jinja2Templates

from core.database import get_session
from core.security import oauth2_scheme

from typing_extensions import Annotated

from apps.projects.schemas.priorities import CreatePriorityRequest
from apps.projects.models import Priority


templates = Jinja2Templates(directory='templates/')

router = APIRouter(
    prefix='/priorities',
    tags=['Priorities'],
    responses= {404: {'description': 'Not Found'}}
)

@router.get('/list', status_code=status.HTTP_201_CREATED, response_class=HTMLResponse,  name='list-priority')
async def register_priority(request: Request, session: Session = Depends(get_session)):
    priorities = await Priority.get_all(session)
    return templates.TemplateResponse('priorities/register.html', {'request': request, 'priorities':priorities})


@router.post('/register', status_code=status.HTTP_201_CREATED, response_class=HTMLResponse, name='register-priority')
async def register_priority(request: Request,
                            name:str = Form(),
                            description:str = Form(default=''),
                            level:int = Form(),
                            color:str = Form(),
                            session: Session = Depends(get_session)):
    new_priority = CreatePriorityRequest(
        name=name,
        description=description,
        level=level,
        color=color
    )

    Priority.create(new_priority, session)

    return RedirectResponse(url=request.url_for('list-priority'),status_code=status.HTTP_303_SEE_OTHER)


@router.post('/update/{priority_id}', status_code=status.HTTP_200_OK, response_class=HTMLResponse, name='update-priority')
async def update_priority(request: Request,
                        priority_id: int,
                        name:str = Form(default=''),
                        description:str = Form(default=''),
                        level:int = Form(default=1),
                        color:str = Form(default=''),
                        session: Session = Depends(get_session)):

    existing_priority = await Priority.get_by_id(priority_id, session)

    if existing_priority is None:
        raise HTTPException(status_code=404, detail="Priority not found")

    # Actualizar los campos
    updated_priority = CreatePriorityRequest(
        name=name,
        description=description,
        level=level,
        color=color
    )
    existing_priority.update(updated_priority, session)

    return RedirectResponse(url=request.url_for('list-priority'), status_code=status.HTTP_303_SEE_OTHER)