from fastapi import Request, BackgroundTasks, HTTPException, APIRouter
from fastapi.responses import StreamingResponse
import uuid

from src.services import BusinessLogic


router = APIRouter(prefix='/api/v1')


@router.post('/start-algorithm')
async def start_algorithm(background_tasks: BackgroundTasks):
    """
    Создание задачи на расчет
    """
    task_id = str(uuid.uuid4())
    BusinessLogic.progress_store[task_id] = 0
    background_tasks.add_task(BusinessLogic.long_running_task, task_id)
    return {
        "task_id": task_id
    }


@router.get('/progress/{task_id}')
async def progress_endpoint(request: Request, task_id: str):
    """
    Подписка на получение HTTP ивентов по задаче
    """
    if task_id not in BusinessLogic.progress_store:
        raise HTTPException(status_code=404, detail="Task not found")
    return StreamingResponse(BusinessLogic.cache_checker(request, task_id), media_type="text/event-stream")