from typing import Any

from app.settings import app_settings, auth_settings


def get_refresh_token_settings(
    refresh_token: str,
    expired: bool = False,
) -> dict[str, Any]:
    base_cookie = {
        "key": auth_settings.REFRESH_TOKEN_KEY,
        "httponly": True,
        "samesite": "none",
        "secure": auth_settings.SECURE_COOKIES,
        "domain": app_settings.SITE_DOMAIN,
    }
    if expired:
        return base_cookie

    return {
        **base_cookie,
        "value": refresh_token,
        "max_age": auth_settings.REFRESH_TOKEN_EXP,
    }
