from .base import *
import dj_database_url


env = environ.Env(
    # Set casting, default value
    DEBUG=(bool, False)
)

environ.Env.read_env(env_file=BASE_DIR / ".env.docker")

QUEUE_URL = env("QUEUE_URL")

DEBUG = env("DEBUG")

SECRET_KEY = "django-insecure-^%qy5-jwhrwm$o0-lh2pg#z7@8ax26e(po5+(akcrg7hzlx4wb"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    "SLIDING_TOKEN_LIFETIME": timedelta(days=30),
    "SLIDING_TOKEN_REFRESH_LIFETIME_LATE_USER": timedelta(days=1),
    "SLIDING_TOKEN_LIFETIME_LATE_USER": timedelta(days=30),
}

DATABASE_URL = env('DATABASE_URL')
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.parse(DATABASE_URL)