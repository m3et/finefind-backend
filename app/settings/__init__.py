from app.settings.app_settings import AppSettings
from app.settings.auth_settings import AuthSettings
from app.settings.redis_settings import RedisSettings
from app.settings.sqlalchemy_settings import SQLAlchemySettings

sqlalchemy_settings = SQLAlchemySettings()
redis_settings = RedisSettings()
auth_settings = AuthSettings()
app_settings = AppSettings()
