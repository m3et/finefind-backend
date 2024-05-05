# This is here so that those schema will be initialize
# when using alembic to autogenreate from metadata
# I'm not sure this is the right way, bit it works
from app.auth.schemas import auth_user, refresh_tokens  # noqa
from app.tasks.schemas import tasks  # noqa
