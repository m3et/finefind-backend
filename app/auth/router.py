import logging
from typing import Annotated, Any

from fastapi import APIRouter, BackgroundTasks, Depends, Response, status

from app.auth import jwt, service, utils
from app.auth.dependencies import (
    valid_refresh_token,
    valid_refresh_token_user,
    valid_user_create,
)
from app.auth.jwt import parse_jwt_user_data
from app.auth.models import AccessTokenResponse, AuthUser, JWTData, UserResponse

logger = logging.getLogger(__name__)

router = APIRouter()

OAuth2FormDep = Annotated[AuthUser.from_oauth_form, Depends()]


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(
    auth_data: AuthUser = Depends(valid_user_create),
) -> dict[str, str]:
    user = await service.create_user(auth_data)
    return {
        "email": user["email"],
    }


@router.get("/users/me", response_model=UserResponse)
async def get_my_account(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
) -> dict[str, str]:
    user = await service.get_user_by_id(jwt_data.user_id)

    return {
        "email": user["email"],
    }


@router.post("/users/tokens", response_model=AccessTokenResponse)
async def auth_user(
    response: Response, auth_form: AuthUser = Depends(AuthUser.from_oauth_form)
) -> AccessTokenResponse:
    logger.info(auth_form)
    logger.debug(
        "auth_user: username: %s, password: %s", auth_form.username, auth_form.password
    )

    user = await service.authenticate_user(auth_form)
    refresh_token_value = await service.create_refresh_token(user_id=user["id"])

    response.set_cookie(**utils.get_refresh_token_settings(refresh_token_value))

    return AccessTokenResponse(
        access_token=jwt.create_access_token(user=user),
        refresh_token=refresh_token_value,
    )


@router.put("/users/tokens", response_model=AccessTokenResponse)
async def refresh_tokens(
    worker: BackgroundTasks,
    response: Response,
    refresh_token: dict[str, Any] = Depends(valid_refresh_token),
    user: dict[str, Any] = Depends(valid_refresh_token_user),
) -> AccessTokenResponse:
    refresh_token_value = await service.create_refresh_token(
        user_id=refresh_token["user_id"]
    )
    response.set_cookie(**utils.get_refresh_token_settings(refresh_token_value))

    worker.add_task(service.expire_refresh_token, refresh_token["uuid"])
    return AccessTokenResponse(
        access_token=jwt.create_access_token(user=user),
        refresh_token=refresh_token_value,
    )


@router.delete("/users/tokens")
async def logout_user(
    response: Response,
    refresh_token: dict[str, Any] = Depends(valid_refresh_token),
) -> None:
    await service.expire_refresh_token(refresh_token["uuid"])

    response.delete_cookie(
        **utils.get_refresh_token_settings(refresh_token["refresh_token"], expired=True)
    )
