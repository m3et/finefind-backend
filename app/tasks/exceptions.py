from app.exceptions import NotFound


class TaskNotFound(NotFound):
    DETAIL = "Task was not found"
