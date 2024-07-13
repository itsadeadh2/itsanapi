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

ALLOWED_HOSTS = ['itsadeadh2.com']

EC2_PRIVATE_IP = None
try:
    EC2_PRIVATE_IP = requests.get('http://169.254.169.254/latest/meta-data/local-ipv4', timeout=0.01).text
except requests.exceptions.RequestException:
    pass

if EC2_PRIVATE_IP:
    ALLOWED_HOSTS.append(EC2_PRIVATE_IP)

DATABASE_URL = env('DATABASE_URL')
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.parse(DATABASE_URL)
