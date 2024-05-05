from pydantic import Field
from pydantic_settings import BaseSettings


class AuthSettings(BaseSettings):
    JWT_ALG: str = Field(default="HS256", alias="JWT_ALG")
    JWT_SECRET: str = Field(default="SECRET", alias="JWT_SECRET")
    JWT_EXP: int = Field(default=5, alias="JWT_EXP")  # minutes

    REFRESH_TOKEN_KEY: str = "refreshToken"
    REFRESH_TOKEN_EXP: int = 60 * 60 * 24 * 21  # 21 days

    SECURE_COOKIES: bool = True
