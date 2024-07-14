from .base import *
import dj_database_url
import requests

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

ALLOWED_HOSTS = ['itsadeadh2.com', 'api.itsadeadh2.com']

METADATA_URI = env('ECS_CONTAINER_METADATA_URI')
print(f"METADATA URI: {METADATA_URI}")
if METADATA_URI:
    container_metadata = requests.get(METADATA_URI).json()
    print(f"Container Metadata: {container_metadata}")
    ALLOWED_HOSTS.append(container_metadata['Networks'][0]['IPv4Addresses'][0])

print(f'ALLOWED_HOSTS: {ALLOWED_HOSTS}')

DATABASE_URL = env('DATABASE_URL')
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.parse(DATABASE_URL)
