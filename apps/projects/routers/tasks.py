from fastapi import APIRouter, status, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse

from sqlalchemy.orm import Session

from fastapi.templating import Jinja2Templates

from core.database import get_session

from apps.projects.schemas.tasks import CreateTaskRequest, CompleteTaskRequest
from apps.projects.models import Task, Priority, Project


templates = Jinja2Templates(directory='templates/')

router = APIRouter(
    prefix='/tasks',
    tags=['tasks'],
    responses= {404: {'description': 'Not Found'}}
)


@router.get('/list', status_code=status.HTTP_201_CREATED, response_class=HTMLResponse,  name='list-tasks')
async def list_task(request: Request, session: Session = Depends(get_session)):
    tasks = await Task.get_all(session)
    priorities = await Priority.get_all(session)
    projects = await Project.get_all(session)

    return templates.TemplateResponse('tasks/register.html', {'request': request, 'tasks':tasks, 'priorities': priorities, 'projects': projects})


@router.post('/register', status_code=status.HTTP_201_CREATED, response_class=HTMLResponse, name='register-task')
async def register_task(request: Request,
                            name:str = Form(),
                            description:str = Form(default=''),
                            priority:int = Form(),
                            project:int = Form(),
                            session: Session = Depends(get_session)):
    new_priority = CreateTaskRequest(
        name=name,
        description=description,
        priority=priority,
        project=project
    )

    Task.create(new_priority, session)

    return RedirectResponse(url=request.url_for('list-tasks'),status_code=status.HTTP_303_SEE_OTHER)


@router.post('/update/{task_id}', status_code=status.HTTP_200_OK, response_class=HTMLResponse, name='update-task')
async def update_task(request: Request,
                        task_id: int,
                        name:str = Form(),
                        description:str = Form(default=''),
                        priority:int = Form(),
                        project:int = Form(),
                        session: Session = Depends(get_session)):

    existing_task = await Task.get_by_id(task_id, session)

    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    # Actualizar los campos
    updated_priority = CreateTaskRequest(
        name=name,
        description=description,
        priority=priority,
        project=project
    )
    existing_task.update(updated_priority, session)

    return RedirectResponse(url=request.url_for('list-tasks'), status_code=status.HTTP_303_SEE_OTHER)


@router.post('/delete/{task_id}', status_code=status.HTTP_204_NO_CONTENT, name='delete-task')
async def delete_task(request: Request, task_id: int, session: Session = Depends(get_session)):
    existing_task = await Task.get_by_id(task_id, session)

    if existing_task is None:
        raise HTTPException(status_code=404, detail="task not found")

    # Eliminar el registro
    session.delete(existing_task)
    session.commit()

    return RedirectResponse(url=request.url_for('list-tasks'), status_code=status.HTTP_303_SEE_OTHER)


@router.post('/complete/{task_id}', status_code=status.HTTP_204_NO_CONTENT, name='complete-task')
async def complete_task(request: Request, task_id: int, payload: CompleteTaskRequest, session: Session = Depends(get_session)):
    existing_task = await Task.get_by_id(task_id, session)
    print(payload)
    if existing_task is None:
        raise HTTPException(status_code=404, detail="task not found")

    # Eliminar el registro
    existing_task.complete(payload, session)

    return RedirectResponse(url=request.url_for('list-tasks'), status_code=status.HTTP_303_SEE_OTHER)