from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings


class SQLAlchemySettings(BaseSettings):
    POSTGRES_DATABASE_URL: PostgresDsn = Field(
        validation_alias="POSTGRES_URL",
        default="postgresql+asyncpg://app:app@app_db:5432/app",
    )
