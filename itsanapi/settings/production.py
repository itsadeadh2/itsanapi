from .base import *
import dj_database_url


env = environ.Env(
    # Set casting, default value
    DEBUG=(bool, False)
)

QUEUE_URL = env("QUEUE_URL")

DEBUG = False

SECRET_KEY = env('JWT_SECRET_KEY')

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    "SLIDING_TOKEN_LIFETIME": timedelta(days=30),
    "SLIDING_TOKEN_REFRESH_LIFETIME_LATE_USER": timedelta(days=1),
    "SLIDING_TOKEN_LIFETIME_LATE_USER": timedelta(days=30),
}

DATABASE_URL = env('DATABASE_URL')
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.parse(DATABASE_URL)
