from typing import Optional

from pydantic import Field, RedisDsn
from pydantic_settings import BaseSettings


class RedisSettings(BaseSettings):
    REDIS_URL: Optional[RedisDsn] = Field(
        alias="REDIS_URL", default="redis://:password@redis:6379/0"
    )
