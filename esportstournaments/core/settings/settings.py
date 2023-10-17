import os
from dotenv import load_dotenv
from .base_settings import *
import ast
load_dotenv()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('secret_key','%^-63(jwq!=kbfdg4#^f64btmd+izfnmjpr)1m13^&=39*tbm0')

if os.getenv('debug') == 'True':
    DEBUG = True
    PAYPAL_TEST = True
else:
    DEBUG = False
    PAYPAL_TEST = False

ALLOWED_HOSTS =('127.0.0.1', 'localhost') #os.getenv('allowed_hosts')

SITE_URL = os.getenv('site_url')

WSGI_APPLICATION = 'core.wsgi.application'

try:
    if os.getenv('user_verification') == 'True':
        USER_VERIFICATION = True
    else:
        USER_VERIFICATION = False
except KeyError:
    USER_VERIFICATION = False

try:
    if os.getenv('esports_mode') == 'False':
        ESPORTS_MODE = False
    else:
        ESPORTS_MODE = True
except KeyError:
    ESPORTS_MODE = True

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

if os.getenv('db_type') == 'postgres':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('db_name'),
            'USER': os.getenv('db_username'),
            'PASSWORD': os.getenv('db_password'),
            'HOST': os.getenv('db_host'),
            'PORT': os.getenv('db_port'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AWS_DEFAULT_ACL = 'public-read'
AWS_ACCESS_KEY_ID = os.getenv('storage_key_id')
AWS_SECRET_ACCESS_KEY = os.getenv('storage_secret_key')
AWS_S3_ENDPOINT_URL = os.getenv('storage_endpoint_url')
AWS_STORAGE_BUCKET_NAME = os.getenv('storage_bucket_name')
AWS_LOCATION = ''
AWS_QUERYSTRING_AUTH = False
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = "%s/%s/" % (AWS_S3_ENDPOINT_URL, AWS_STORAGE_BUCKET_NAME)

# Email stuff
EMAIL_USE_TLS = os.getenv('email_use_tls')
EMAIL_HOST = os.getenv('email_host')
EMAIL_HOST_USER = os.getenv('email_host_user')
EMAIL_HOST_PASSWORD = os.getenv('email_host_password')

try:
    FROM_EMAIL = os.getenv('from_email')
except IndexError:
    FROM_EMAIL = os.getenv('from_email')
except KeyError:
    FROM_EMAIL = "MySite <noreply@example.com>"

EMAIL_PORT = os.getenv('email_port')

try:
    PAYPAL_EMAIL = os.getenv('paypal_email')
except (KeyError, IndexError):
    PAYPAL_EMAIL = 'none@example.com'




# Captcha
GOOGLE_RECAPTCHA_SECRET_KEY = os.getenv('google_recaptcha_secret_key')
GOOGLE_RECAPTCHA_SITE_KEY = os.getenv('google_recaptcha_site_key')

# Site info
SITE_NAME = os.getenv('site_name')
SITE_SERVER = os.getenv('site_server')
RECAPTCHA_CREDENTIALS_JSON = ast.literal_eval(
    os.getenv("RECAPTCHA_CREDENTIALS_JSON", "{}",)
    .replace("\r", "\\r")
    .replace("\n", "\\n")
)

SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']