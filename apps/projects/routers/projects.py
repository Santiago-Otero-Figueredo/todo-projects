from fastapi import APIRouter, status, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse

from sqlalchemy.orm import Session

from fastapi.templating import Jinja2Templates

from core.database import get_session

from apps.projects.schemas.projects import CreateProjectRequest
from apps.projects.models import Project

templates = Jinja2Templates(directory='templates/')

router = APIRouter(
    prefix='/projects',
    tags=['projects'],
    responses= {404: {'description': 'Not Found'}}
)



@router.get('/list', status_code=status.HTTP_201_CREATED, response_class=HTMLResponse,  name='list-projects')
async def list_project(request: Request, session: Session = Depends(get_session)):
    projects = await Project.get_all(session)
    return templates.TemplateResponse('projects/register.html', {'request': request, 'projects':projects})


@router.post('/register', status_code=status.HTTP_201_CREATED, response_class=HTMLResponse, name='register-project')
async def register_project(request: Request,
                            name:str = Form(),
                            description:str = Form(default=''),
                            session: Session = Depends(get_session)):
    new_priority = CreateProjectRequest(
        name=name,
        description=description,
    )

    Project.create(new_priority, session)

    return RedirectResponse(url=request.url_for('list-projects'),status_code=status.HTTP_303_SEE_OTHER)


@router.post('/update/{project_id}', status_code=status.HTTP_200_OK, response_class=HTMLResponse, name='update-project')
async def update_project(request: Request,
                        project_id: int,
                        name:str = Form(default=''),
                        description:str = Form(default=''),
                        session: Session = Depends(get_session)):

    existing_project = await Project.get_by_id(project_id, session)

    if existing_project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    # Actualizar los campos
    updated_priority = CreateProjectRequest(
        name=name,
        description=description,
    )
    existing_project.update(updated_priority, session)

    return RedirectResponse(url=request.url_for('list-projects'), status_code=status.HTTP_303_SEE_OTHER)


@router.post('/delete/{project_id}', status_code=status.HTTP_204_NO_CONTENT, name='delete-project')
async def delete_project(request: Request, project_id: int, session: Session = Depends(get_session)):
    existing_project = await Project.get_by_id(project_id, session)

    if existing_project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    # Eliminar el registro
    session.delete(existing_project)
    session.commit()

    return RedirectResponse(url=request.url_for('list-projects'), status_code=status.HTTP_303_SEE_OTHER)