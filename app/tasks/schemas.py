from sqlalchemy import (
    ARRAY,
    TIMESTAMP,
    Column,
    ForeignKey,
    Identity,
    Integer,
    Interval,
    String,
    Table,
    func,
)

from app.services.sqlalchemy import metadata

tasks = Table(
    "tasks",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("user_id", ForeignKey("auth_user.id", ondelete="CASCADE"), nullable=False),
    Column("title", String, nullable=False),
    Column("description", String, nullable=False),
    Column(
        "created_at",
        TIMESTAMP,
        server_default=func.now(),
    ),
    Column(
        "updated_at",
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
    ),
    Column("status", String, nullable=False),
    Column("priority", String),
    Column("due_date", TIMESTAMP(timezone=True)),
    Column("assigned_to", Integer),  # TODO: use ForeignKey
    Column("estimated_time", Interval),
    Column("actual_time", Interval),
    Column("parent_task_id", Integer),  # TODO: use ForeignKey
    Column("recurrence_rule", String),
    Column("tags", ARRAY(String)),
)
