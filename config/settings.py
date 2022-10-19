import string
from pathlib import Path

from django.conf.global_settings import STATICFILES_DIRS
from environ import Env

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = BASE_DIR.joinpath('.env')

env = Env()
env.read_env(str(ENV_FILE))

SECRET_KEY = env.str('DJANGO_SECRET_KEY')
DEBUG = env.bool('DEBUG')
DOMAIN = env.str('DOMAIN')

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'bootstrap5',

    'apps.core',
    'apps.accounts',
    'apps.shorter',
]

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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR.joinpath('templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3'
    },
    '_default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str('POSTGRES_DB'),
        'USER': env.str('POSTGRES_USER'),
        'PASSWORD': env.str('POSTGRES_PASSWORD'),
        'HOST': env.str('POSTGRES_HOST'),
        'PORT': env.str('POSTGRES_PORT'),
        'TEST': {
            'NAME': 'postgres_test'
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

AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = (
    'apps.accounts.backends.auth_backends.UserIdAndPasswordBackend',
    'apps.accounts.backends.auth_backends.CIUsernameAndPasswordBackend',
    'apps.accounts.backends.auth_backends.CIEmailAndPasswordBackend',
    'apps.accounts.backends.auth_backends.LoginAndPasswordBackend',
)
USERNAME_MIN_LENGTH = 3  # Влияет только на валидацию.
USERNAME_MAX_LENGTH = 16  # Влияет только на валидацию, реальную максимальную длинну смотреть в модели пользователя.
USERNAME_ALLOWED_CHARS_TO_FIRST_CHAR = string.ascii_letters + '_'
USERNAME_ALLOWED_CHARS = string.ascii_letters + string.digits + '_'

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = 'staticfiles/'
STATICFILES_DIRS = [
    BASE_DIR.joinpath('static'),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
REST_FRAMEWORK = {
    'DEFAULT_VERSION': '1.0.0',
    'ALLOWED_VERSIONS': [
        '1.0.0',
    ],
    'VERSION_PARAM': 'version',
    'DEFAULT_VERSIONING_CLASS': None,

    'DEFAULT_METADATA_CLASS': None,

    'DEFAULT_PAGINATION_CLASS': 'apps.core.api.pagination.CursorPagination',
    'PAGE_SIZE': 20,

    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    'DEFAULT_THROTTLE_CLASSES': [],
    'DEFAULT_THROTTLE_RATES': {
        'user': None,
        'anon': None,
    },
    'NUM_PROXIES': None,

    'SEARCH_PARAM': 'search',
    'ORDERING_PARAM': 'ordering',

    'DEFAULT_RENDERER_CLASSES': [
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer',
    ],

    'DEFAULT_PARSER_CLASSES': [
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
    ],

}
SPECTACULAR_SETTINGS = {
    'TITLE': 'Veenrok API',
    'DESCRIPTION': 'Veenrok API doc',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,

    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
    'POSTPROCESSING_HOOKS': (
        'drf_spectacular.contrib.djangorestframework_camel_case.camelize_serializer_fields',
    )
}
