"""
Django settings for preico project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from .local_settings import *


VERSION = '0.0.1'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'cp.app.BackendConfig',
    'console.app.BackendConfig',
    'landing.apps.LandingConfig',
    'hvad',
    'martor',
    'rest_framework',
    'djrill',
    'django_countries',
    'corsheaders'
]

CORS_ORIGIN_WHITELIST = (
    '0.0.0.0:8030',
)
CORS_ALLOW_CREDENTIALS = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'preico.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR , 'cp', 'templates' ),
            os.path.join(BASE_DIR , 'landing', 'templates' )
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

WSGI_APPLICATION = 'preico.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators
MIN_PWD_LENGTH = 8

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': MIN_PWD_LENGTH
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

SESSION_ENGINE = 'redis_sessions.session'

EMAIL_BACKEND = 'djrill.mail.backends.djrill.DjrillBackend'

DEFAULT_FROM_EMAIL='noreply@unilot.io'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'preico.rest_framework.renderers.TemplateHTMLRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'preico.rest_framework.authentication.SessionAuthentication',
    ),
    'EXCEPTION_HANDLER': 'preico.rest_framework.views.exception_handler'
}

# Global martor settings
# Input: string boolean, `true/false`
MARTOR_ENABLE_CONFIGS = {
    'jquery': 'true',    # to include/revoke jquery (require for admin default django)
}

# Safe Mode
MARTOR_MARKDOWN_SAFE_MODE = True

# Markdownify
MARTOR_MARKDOWNIFY_FUNCTION = 'martor.utils.markdownify'
MARTOR_MARKDOWNIFY_URL = '/martor/markdownify/'

# Markdown extensions (default)
MARTOR_MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra',
    'markdown.extensions.nl2br',
    'markdown.extensions.smarty',
    'markdown.extensions.fenced_code',

    # Custom markdown extensions.
    'martor.extensions.urlize',
    'martor.extensions.del_ins', # ~~strikethrough~~ and ++underscores++
    'landing.martor.extensions.big_amount'
]

# Markdown urls
MARTOR_UPLOAD_URL = '/martor/uploader/' # default

# Markdown Extensions
MARTOR_MARKDOWN_BASE_EMOJI_URL = 'https://assets-cdn.github.com/images/icons/emoji/' # default

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    # ('ru-ru', 'Русский'),
    ('en-us', 'English'),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

FORMAT_MODULE_PATH = (
    'landing.formats',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ), '.static_storage')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'cp', 'assets'),
    os.path.join(BASE_DIR, 'landing', 'assets'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ), '.media')

SOCIAL_LINKS = {
    'FACEBOOK': 'https://www.facebook.com/unilot.io/',
    'TWITTER': 'https://twitter.com/unilot_platform',
    'REDDIT': 'https://www.reddit.com/user/unilot_platform',
    'MEDIUM': 'https://medium.com/@unilot',
    'TELEGRAM_RU_RU': 'https://t.me/unilot',
    'TELEGRAM_EN_US': 'https://t.me/Uniloteng',
    'LINKEDIN': 'https://www.linkedin.com/company/18284068/',
    'SLACK': 'https://join.slack.com/t/unilot/shared_invite/enQtMjkzMjc5NTE0NjczLTU2ODlmOGE1YjkwMzBlOTM4ZTg2MTAxMTUwZTdhYjRiZGUxYmFlMjc1YjQ5YzM2N2JhYzQ0MWNlZmZkMDQxNWU',
    'YOUTUBE': 'https://www.youtube.com/channel/UCNdn2maOQEbYwpNK4Yaoxqw',
    'GITHUB': 'https://github.com/unilot',
    'STEEMIT': 'https://steemit.com/@unilot',
    'BITCOINTALK': 'https://bitcointalk.org/index.php?topic=2695196.msg27539646#msg27539646'
}

COUNTRIES_EXCLUDED = (
    'US',
    'CA',
    'CN',
    'SG'
)
