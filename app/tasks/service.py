import logging
from typing import Any, Dict, List, Optional

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import SQLAlchemyError

from app.services.sqlalchemy import fetch_all, fetch_one
from app.tasks.models import TaskInput, TaskUpdate
from app.tasks.schemas import tasks

logger = logging.getLogger(__name__)


async def get_tasks(user_id: int) -> List[Dict[str, Any]]:
    try:
        select_query = select(tasks).where(tasks.c.user_id == user_id)
        return await fetch_all(select_query)
    except SQLAlchemyError as e:
        logger.error(f"Error fetching tasks: {e}")
        raise


async def get_task(task_id: int, user_id: int) -> Optional[Dict[str, Any]]:
    try:
        select_query = (
            select(tasks).where(tasks.c.user_id == user_id).where(tasks.c.id == task_id)
        )
        return await fetch_one(select_query)
    except SQLAlchemyError as e:
        logger.error(f"Error fetching task: {e}")
        raise


async def create_task(task: TaskInput, user_id: int) -> Optional[Dict[str, Any]]:
    try:
        task_model = task.model_dump() | {"user_id": user_id}
        insert_query = insert(tasks).values(task_model).returning(tasks)
        return await fetch_one(insert_query)
    except SQLAlchemyError as e:
        logger.error(f"Error creating task: {e}")
        raise


async def update_task(
    task_update: TaskUpdate, user_id: int
) -> Optional[Dict[str, Any]]:
    try:
        update_query = (
            update(tasks)
            .where(tasks.c.id == task_update.id)
            .where(tasks.c.user_id == user_id)
            .values(task_update.model_dump(exclude_unset=True))
            .returning(tasks)
        )
        return await fetch_one(update_query)
    except SQLAlchemyError as e:
        logger.error(f"Error updating task: {e}")
        raise


async def delete_task(task_id: int, user_id: int) -> Optional[Dict[str, Any]]:
    try:
        delete_query = (
            delete(tasks)
            .where(tasks.c.id == task_id)
            .where(tasks.c.user_id == user_id)
            .returning(tasks)
        )
        return await fetch_one(delete_query) or []
    except SQLAlchemyError as e:
        logger.error(f"Error deleting task: {e}")
        raise
