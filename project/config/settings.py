import os
from pathlib import Path
from django.urls import reverse_lazy


# Get non-empty variables
def get_env_variable(key, default=None):
    value = os.environ.get(key)
    if value is None or len(value) == 0:
        value = default
    return value


# Debug Toolbar disable INTERNAL_IPS
def show_toolbar(request):
    return DEBUG


_SERVICE_TYPE_WSGI = 'WSGI'
_SERVICE_TYPE_ASGI = 'ASGI'
_SERVICE_TYPE_CELERY = 'CELERY'


APPLICATION_NAME = get_env_variable('APP_NAME', 'Project')
APPLICATION_CODE = get_env_variable('APP_CODE', 'project')

SERVICE_TYPE = get_env_variable('SERVICE_TYPE', _SERVICE_TYPE_WSGI).upper()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = get_env_variable('APP_SECRET_KEY')

DEBUG = int(get_env_variable('DEBUG', 0))

ALLOWED_HOSTS = get_env_variable('APP_ALLOWED_HOSTS', '127.0.0.1 localhost').split(' ')

INSTALLED_APPS = [
    'accounts',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # custom
    'config',
    'home',
]

if SERVICE_TYPE == _SERVICE_TYPE_ASGI:
    INSTALLED_APPS.insert(0, 'daphne')
    ASGI_APPLICATION = 'config.asgi.application'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            'home.context_processors.get_project_info',
        ],
    },
}]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.{}'.format(get_env_variable('DATABASE_ENGINE', 'postgresql')),
        'HOST': get_env_variable('DATABASE_HOST', 'database'),
        'PORT': get_env_variable('DATABASE_PORT', 5432),
        'NAME': get_env_variable('DATABASE_NAME', 'postgres'),
        'USER': get_env_variable('DATABASE_USER', 'postgres'),
        'PASSWORD': get_env_variable('DATABASE_PASSWORD', 'postgres'),
    }
}

# Redis
_REDIS_URL_TEMPLATE = 'redis://{}/{}'
REDIS_HOST = get_env_variable('REDIS_HOST', 'redis')
REDIS_PORT = get_env_variable('REDIS_PORT', 6379)

# Cache
_CACHE_BACKEND_REDIS = 'redis.RedisCache'
_CACHE_BACKEND = get_env_variable('CACHE_BACKEND', _CACHE_BACKEND_REDIS)

_CACHE_LOCATION = '{}:{}'.format(
    get_env_variable('CACHE_HOST', REDIS_HOST),
    get_env_variable('CACHE_PORT', REDIS_PORT),
)
if _CACHE_BACKEND == _CACHE_BACKEND_REDIS:
    _CACHE_LOCATION = _REDIS_URL_TEMPLATE.format(_CACHE_LOCATION, 0)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.{}'.format(_CACHE_BACKEND),
        'LOCATION': _CACHE_LOCATION,
        'KEY_PREFIX': get_env_variable('CACHE_KEY_PREFIX', APPLICATION_CODE),
        'TIMEOUT': get_env_variable('CACHE_TIMEOUT', 60),
    }
}

# Celery
CELERY_BROKER_URL = '{}:{}'.format(
    get_env_variable('CELERY_HOST', REDIS_HOST),
    get_env_variable('CELERY_PORT', REDIS_PORT)
)

if get_env_variable('CELERY_BACKEND', 'redis'):
    CELERY_BROKER_URL = _REDIS_URL_TEMPLATE.format(CELERY_BROKER_URL, 1)

# Channels
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(REDIS_HOST, REDIS_PORT)],
        }
    }
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

TIME_ZONE = 'Europe/Minsk'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Debug Toolbar
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': show_toolbar,
    }

LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = reverse_lazy('home')
LOGOUT_REDIRECT_URL = LOGIN_URL
