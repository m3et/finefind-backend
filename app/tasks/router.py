import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends

from app.auth.jwt import parse_jwt_user_data
from app.auth.models import JWTData
from app.tasks import service as task_service
from app.tasks.dependencies import get_task_or_404
from app.tasks.exceptions import TaskNotFound

# Importing tasks database and dependencies
from app.tasks.models import TaskInput, TaskOutput, TaskUpdate

logger = logging.getLogger(__name__)

# Creating an API router instance
router = APIRouter()

# TODO: Should use depencies for valid_task, maybe use redis for that?


# Endpoint to get all tasks
@router.get("/", response_model=List[TaskOutput])
async def get_tasks(jwt_data: JWTData = Depends(parse_jwt_user_data)):
    task_list = await task_service.get_tasks(user_id=jwt_data.user_id)
    return task_list


# Endpoint to get a specific task by ID
@router.get("/{task_id}", response_model=TaskOutput)
async def get_task(task: Annotated[TaskOutput, Depends(get_task_or_404)]):
    """Get a specific task by its ID.

    Args:
        task_id (int): The ID of the task to retrieve.

    Returns:
        Task: The task object corresponding to the given ID.
    """
    return task


# Endpoint to add a new task
@router.post("/", response_model=TaskOutput)
async def post_task(task: TaskInput, jwt_data: JWTData = Depends(parse_jwt_user_data)):
    """Add a new task.

    Args:
        task (Task): The task object to add.

    Returns:
        Task: The added task object.
    """
    task = await task_service.create_task(task, jwt_data.user_id)
    return task


# TODO: use get_task_404
@router.put("/{task_id}", response_model=TaskOutput)
async def update_task(
    task: TaskUpdate, jwt_data: JWTData = Depends(parse_jwt_user_data)
):
    task = await task_service.update_task(task_update=task, user_id=jwt_data.user_id)
    if task:
        return task
    raise TaskNotFound()


# Endpoint to delete a task by ID
@router.delete("/{task_id}", response_model=TaskOutput)
async def delete_task(task: Annotated[TaskOutput, Depends(get_task_or_404)]):
    """Delete a task by its ID.

    Args:
        task_id (int): The ID of the task to delete.

    Returns:
        Task: The deleted task object.
    """

    return await task_service.delete_task(task_id=task.id, user_id=task.user_id)
