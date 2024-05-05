import re
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr, Field, field_validator

from app.models import CustomModel

STRONG_PASSWORD_PATTERN = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d!@#$%^&*]{6,128}$"
)


class AuthUser(CustomModel):
    username: EmailStr
    password: str = Field(min_length=6, max_length=128)

    @field_validator("password", mode="after")
    @classmethod
    def valid_password(cls, password: str) -> str:
        if not 6 <= len(password) <= 128:
            raise ValueError(
                "Password must be at least of 6\
                      character and shorter then 128 characters"
            )
        if not re.match(STRONG_PASSWORD_PATTERN, password):
            raise ValueError(
                "Password must contain at least "
                "one lower character, "
                "one upper character, "
                "one digit"
            )

        return password

    @classmethod
    def from_oauth_form(
        cls, auth_form: Annotated[OAuth2PasswordRequestForm, Depends()]
    ) -> "AuthUser":
        return cls(username=auth_form.username, password=auth_form.password)


class JWTData(CustomModel):
    user_id: int = Field(alias="sub")
    is_admin: bool = False


class AccessTokenResponse(CustomModel):
    access_token: str
    refresh_token: str


class UserResponse(CustomModel):
    email: EmailStr
