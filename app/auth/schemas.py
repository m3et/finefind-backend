from sqlalchemy import (
    TIMESTAMP,
    UUID,
    Boolean,
    Column,
    ForeignKey,
    Identity,
    Integer,
    LargeBinary,
    String,
    Table,
    func,
)

from app.services.sqlalchemy import metadata

auth_user = Table(
    "auth_user",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("email", String, nullable=False),
    Column("password", LargeBinary, nullable=False),
    Column("is_admin", Boolean, server_default="false", nullable=False),
    Column("created_at", TIMESTAMP, server_default=func.now(), nullable=False),
    Column("updated_at", TIMESTAMP, onupdate=func.now()),
)
refresh_tokens = Table(
    "auth_refresh_token",
    metadata,
    Column("uuid", UUID, primary_key=True),
    Column("user_id", ForeignKey("auth_user.id", ondelete="CASCADE"), nullable=False),
    Column("refresh_token", String, nullable=False),
    Column("expires_at", TIMESTAMP, nullable=False),
    Column("created_at", TIMESTAMP, server_default=func.now(), nullable=False),
    Column("updated_at", TIMESTAMP, onupdate=func.now()),
)
