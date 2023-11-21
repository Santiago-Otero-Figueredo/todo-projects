from fastapi import APIRouter, status, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse

from sqlalchemy.orm import Session

from fastapi.templating import Jinja2Templates

from core.database import get_session

from apps.projects.schemas.states import CreateStateRequest
from apps.projects.models import State

templates = Jinja2Templates(directory='templates/')

router = APIRouter(
    prefix='/states',
    tags=['States'],
    responses= {404: {'description': 'Not Found'}}
)


@router.get('/list', status_code=status.HTTP_201_CREATED, response_class=HTMLResponse,  name='list-states')
async def register_state(request: Request, session: Session = Depends(get_session)):
    states = await State.get_all(session)
    return templates.TemplateResponse('states/register.html', {'request': request, 'states':states})


@router.post('/register', status_code=status.HTTP_201_CREATED, response_class=HTMLResponse, name='register-state')
async def register_state(request: Request,
                            name:str = Form(),
                            description:str = Form(default=''),
                            color:str = Form(),
                            session: Session = Depends(get_session)):
    new_state = CreateStateRequest(
        name=name,
        description=description,
        color=color
    )

    State.create(new_state, session)

    return RedirectResponse(url=request.url_for('list-states'),status_code=status.HTTP_303_SEE_OTHER)


@router.post('/update/{state_id}', status_code=status.HTTP_200_OK, response_class=HTMLResponse, name='update-state')
async def update_state(request: Request,
                        state_id: int,
                        name:str = Form(default=''),
                        description:str = Form(default=''),
                        color:str = Form(default=''),
                        session: Session = Depends(get_session)):

    existing_state = await State.get_by_id(state_id, session)

    if existing_state is None:
        raise HTTPException(status_code=404, detail="State not found")

    # Actualizar los campos
    updated_state = CreateStateRequest(
        name=name,
        description=description,
        color=color
    )
    existing_state.update(updated_state, session)

    return RedirectResponse(url=request.url_for('list-states'), status_code=status.HTTP_303_SEE_OTHER)


@router.post('/delete/{state_id}', status_code=status.HTTP_204_NO_CONTENT, name='delete-state')
async def delete_state(request: Request, state_id: int, session: Session = Depends(get_session)):
    existing_state = await State.get_by_id(state_id, session)

    if existing_state is None:
        raise HTTPException(status_code=404, detail="State not found")

    # Eliminar el registro
    session.delete(existing_state)
    session.commit()

    return RedirectResponse(url=request.url_for('list-states'), status_code=status.HTTP_303_SEE_OTHER)