import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = None #Setup very secure very secret key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'your-pg-db-name',
        'USER': 'yout-pg-username',
        'PASSWORD': 'your-pg-password',
        'HOST': 'your-pg-db-host',
        # 'PORT': 'your-pg-db-port', #If required
    }
}

SESSION_REDIS = {
    'host': None,
    'unix_domain_socket_path': '/var/run/redis/redis.sock',
    'db': 15,
    'password': 'password',
    'prefix': 'unilot-pre-ico-session',
    'socket_timeout': 1
}

COINBASE_CONFIG = {
    'API_KEY': 'coinbase-api-key',
    'API_SECRET': 'coinbase-secret',
    'API_VERSION': '2017-09-12'
}

MANDRILL_API_KEY='mandrill-api-key'

TOKEN_ADDRESS='token-address'
