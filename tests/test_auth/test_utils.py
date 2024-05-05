from app.auth.utils import get_refresh_token_settings
from app.settings import app_settings, auth_settings


def test_get_refresh_token_settings():
    # Test with expired refresh token
    expired_refresh_token = "expired_token"
    result = get_refresh_token_settings(expired_refresh_token, expired=True)
    assert isinstance(result, dict)
    assert result["key"] == auth_settings.REFRESH_TOKEN_KEY
    assert result["httponly"] is True
    assert result["samesite"] == "none"
    assert result["secure"] == auth_settings.SECURE_COOKIES
    assert result["domain"] == app_settings.SITE_DOMAIN

    # Test with non-expired refresh token
    refresh_token = "valid_token"
    result = get_refresh_token_settings(refresh_token)
    assert isinstance(result, dict)
    assert result["key"] == auth_settings.REFRESH_TOKEN_KEY
    assert result["httponly"] is True
    assert result["samesite"] == "none"
    assert result["secure"] == auth_settings.SECURE_COOKIES
    assert result["domain"] == app_settings.SITE_DOMAIN
    assert result["value"] == refresh_token
    assert result["max_age"] == auth_settings.REFRESH_TOKEN_EXP
