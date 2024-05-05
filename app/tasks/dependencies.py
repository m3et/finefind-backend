from typing import Annotated

from fastapi import Depends

from app.auth.jwt import parse_jwt_user_data
from app.auth.models import JWTData
from app.tasks import service
from app.tasks.exceptions import TaskNotFound
from app.tasks.models import TaskOutput


async def get_task_or_404(
    task_id: int, jwt_data: Annotated[JWTData, Depends(parse_jwt_user_data)]
) -> TaskOutput:
    task = await service.get_task(task_id=task_id, user_id=jwt_data.user_id)
    if not task:
        raise TaskNotFound()
    return TaskOutput.model_validate(task)
