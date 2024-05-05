import datetime
from typing import Any

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt  # type: ignore

from app.auth.exceptions import AuthorizationFailed, AuthRequired, InvalidToken
from app.auth.models import JWTData
from app.settings import auth_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/users/tokens", auto_error=False)


def create_access_token(
    *,
    user: dict[str, Any],
    expires_delta: datetime.timedelta = datetime.timedelta(
        minutes=auth_settings.JWT_EXP
    ),
) -> str:
    jwt_data = {
        "sub": str(user["id"]),
        "exp": datetime.datetime.now(datetime.timezone.utc) + expires_delta,
        "is_admin": user["is_admin"],
    }

    return jwt.encode(
        jwt_data, auth_settings.JWT_SECRET, algorithm=auth_settings.JWT_ALG
    )


async def parse_jwt_user_data_optional(
    token: str = Depends(oauth2_scheme),
) -> JWTData | None:
    if not token:
        return None

    try:
        payload = jwt.decode(
            token, auth_settings.JWT_SECRET, algorithms=[auth_settings.JWT_ALG]
        )
    except JWTError:
        raise InvalidToken()

    return JWTData(**payload)


async def parse_jwt_user_data(
    token: JWTData | None = Depends(parse_jwt_user_data_optional),
) -> JWTData:
    if not token:
        raise AuthRequired()

    return token


async def parse_jwt_admin_data(
    token: JWTData = Depends(parse_jwt_user_data),
) -> JWTData:
    if not token.is_admin:
        raise AuthorizationFailed()

    return token


async def validate_admin_access(
    token: JWTData | None = Depends(parse_jwt_user_data_optional),
) -> None:
    if token and token.is_admin:
        return

    raise AuthorizationFailed()
