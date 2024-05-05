from enum import Enum

from pydantic import model_validator
from pydantic_settings import BaseSettings


class Environment(str, Enum):
    LOCAL = "LOCAL"
    TESTING = "TESTING"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"

    @property
    def is_debug(self):
        return self in (self.LOCAL, self.STAGING, self.TESTING)

    @property
    def is_testing(self):
        return self == self.TESTING

    @property
    def is_deployed(self) -> bool:
        return self in (self.STAGING, self.PRODUCTION)


class AppSettings(BaseSettings):
    SITE_DOMAIN: str = "myapp.com"

    ENVIRONMENT: Environment = Environment.LOCAL

    SENTRY_DSN: str | None = None

    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str] = ["*"]

    APP_VERSION: str = "1"

    @model_validator(mode="after")
    def validate_sentry_non_local(self) -> "AppSettings":
        if self.ENVIRONMENT.is_deployed and not self.SENTRY_DSN:
            raise ValueError("Sentry is not set")

        return self
