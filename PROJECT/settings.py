import os
import dj_database_url
import dj_email_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    release=os.environ.get("GIT_REV"),
    dsn="https://4861ae1cb9ed4859bae2c0f0cd1f2f53@o397405.ingest.sentry.io/5251824",
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '#(@r9^xj-8cdt&7h-vozzzh-mm18s2k5g500x3q^zy#_@z=a#e'

DEBUG = True
ALLOWED_HOSTS = []

if os.environ.get("ENVIRONMENT") == "PRODUCTION":
    DEBUG = False
    ALLOWED_HOSTS = ['hospitalaid.org', 'hospitalaid.apps.flagzeta.org', 'localhost']

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    "django.forms",
    "django_extensions",
    "debug_toolbar",
    "django_filters",
    "main.apps.MainConfig",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'sesame.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'PROJECT.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "main.context_processors.globals",
            ],
        },
    },
]
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

WSGI_APPLICATION = 'PROJECT.wsgi.application'


DATABASES = {
    'default': dj_database_url.config(conn_max_age=600)
}

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


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

email_config = dj_email_url.config()
vars().update(email_config)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "%(levelname)s %(message)s"}
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        }
    },
    "loggers": {
        "main": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

LOGIN_REDIRECT_URL = "/"
INTERNAL_IPS = ["127.0.0.1"]
EMAIL_SUBJECT_PREFIX = "[PROJECT] "
AUTH_USER_MODEL = "main.User"

AUTHENTICATION_BACKENDS = [
        'django.contrib.auth.backends.ModelBackend',
        'sesame.backends.ModelBackend']
