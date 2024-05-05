from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional

from pydantic import Field, StringConstraints
from typing_extensions import Annotated

from app.models import CustomModel


class StatusEnum(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"


class TaskBase(CustomModel):
    title: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    description: Optional[str]
    status: StatusEnum = StatusEnum.pending
    priority: Optional[str]
    due_date: Optional[datetime]
    assigned_to: Optional[int]
    tags: List[str] = Field(default_factory=list)
    estimated_time: Optional[timedelta]
    actual_time: Optional[timedelta]
    parent_task_id: Optional[int]
    recurrence_rule: Optional[str]


class TaskInput(TaskBase):
    pass


class TaskUpdate(TaskBase):
    id: int


class TaskOutput(TaskBase):
    id: int
    user_id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]


class TaskComment(CustomModel):
    id: int
    task_id: int
    user_id: int
    comment: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
