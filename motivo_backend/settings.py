"""
Django settings for motivo_backend project.
"""

from pathlib import Path

# 1) This is the base directory of your Django project.
BASE_DIR = Path(__file__).resolve().parent.parent

# 2) A secret key for Django (don’t share it publicly in real projects).
SECRET_KEY = 'django-insecure-your-secret-key-here'

# 3) Turn off debug mode for a production-like environment.
DEBUG = True

# 4) List of hosts or domains your Django site can serve.
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# 5) Django “apps” installed in your project.
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'motivo_core',
    # other apps...
    'chatty',  # <--- add this line
]

# 6) Middlewares are small components that process requests/responses globally.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 7) The main URL configuration file for your project.
ROOT_URLCONF = 'motivo_backend.urls'

# 8) Template settings: how Django finds and renders HTML templates.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Add template folders here if you have any
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

# 9) WSGI application entry point (for running the server).
WSGI_APPLICATION = 'motivo_backend.wsgi.application'

# 10) Database settings for PostgreSQL.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'motivo_db',
        'USER': 'postgres',
        'PASSWORD': 'Motivo1234$',  # <--- Put your PostgreSQL password here
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# 11) Password validation rules (for user sign-ups, etc.).
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

# 12) General settings: language, timezone, static files, etc.
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 13) URL for static files (CSS, JS, images).
STATIC_URL = '/static/'

# 14) Default primary key field type for new models.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 15) Your Smartsheet API token (used by the script that connects to SmartSheets).
SMARTSHEET_ACCESS_TOKEN = '4rJ6r2YBZ5ZUbHgw4QVGuybX6rBEiQ8c16O2S'


SLACK_BOT_TOKEN = '2uA2yTnhLdgLpRCd62MDbwh0Gby_6s3NnvCgUwLJn7oGX66zR'
