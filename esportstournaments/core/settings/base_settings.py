import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SESSION_COOKIE_AGE = 604800


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.forms',
    'captcha',
    'ckeditor',
    # ip package
    'ipware',

    # just regular pages
    'pages.apps.PagesConfig',
    'support.apps.SupportConfig',
    'news.apps.NewsConfig',
    'profiles.apps.PlayersConfig',
    'competitions.apps.CompetetitionsConfig',
    'teams.apps.TeamsConfig',
    'matches.apps.MatchesConfig',
    'staff.apps.StaffConfig'

]

try:
    if os.environ['enable_store'] == 'True':
        STORE_ENABLED = True
    else:
        STORE_ENABLED = False
except KeyError:
    STORE_ENABLED = False
try:
    if os.environ['enable_wagers'] == 'True':
        WAGERS_ENABLED = True
    else:
        WAGERS_ENABLED = False
except KeyError:
    WAGERS_ENABLED = False

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.ban_middleware',
]

ROOT_URLCONF = 'core.urls'
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                
                'core.context_processors.site_info',
            ],
        },
    },
]
WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR,'static/')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Where to redirect users after login
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

SITE_VERSION = "1.0.0"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CKEDITOR_BASEPATH = os.path.join(BASE_DIR,'static/ckeditor/ckeditor/')
CKEDITOR_UPLOAD_PATH = 'media/ckeditor/'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            {'name': 'codesnippet', 'items': ['CodeSnippet']},
        ],
    },
}

RECAPTCHA_ENTERPRISE_VERIFY_URLS = [
    'profiles:login'
]


