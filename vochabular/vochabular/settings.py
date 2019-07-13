"""
Django settings for vochabular project.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/
"""

import os
from vochabular.auth import get_key, user_handler
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=7p4(ni8+te(y@d)f9o)x^!30cb7i+)d=_eej1wa@eowin7o#3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'graphene_django',
    'api',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]

ROOT_URLCONF = 'vochabular.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'vochabular.wsgi.application'

sentry_sdk.init(
    dsn="https://" + os.environ['SENTRY'],
    integrations=[DjangoIntegration()]
)

GRAPHENE = {
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}

GRAPHQL_JWT = {
    'JWT_SECRET_KEY': get_key(b"""-----BEGIN CERTIFICATE-----
MIIDFTCCAf2gAwIBAgIJPfoA7M4Opdl5MA0GCSqGSIb3DQEBCwUAMCgxJjAkBgNVBAMTHXZvY2hhYnVsYXItYWRtaW4uZXUuYXV0aDAuY29tMB4XDTE5MDExNTIyNTUwNFoXDTMyMDkyMzIyNTUwNFowKDEmMCQGA1UEAxMddm9jaGFidWxhci1hZG1pbi5ldS5hdXRoMC5jb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCfE+zsqqpZcsEOqTPCFnPDsQzJqF04y5dOmxe7Z1pJA14WtcqYe+3dOcFQ2avuB/qROBDZ2LOMRS3W/T9tyCuj0L3b1lCeNm8F7vptPU+pzURmz5Gj6lDK5BXdpBUIoj8D172iM2Xd1QycnIWmVCAyG+Hwx7h8W1cCMNhOBGozRooNilWOXvxIard7Cxib3NDmHn37X9lCNws/nP3Pi9bnOSVJ+htP/J6zlTxZDyZ/zU2ZGMgEUFf6BSXooPJFoIbffusvn17IGVieuJfBSWgsLyw2vZUEDbsQZCtXI1c1lJwdHtZ2VQZEAKSBU5CcAMSg7ynZqp0eTkMIeNGOdFfjAgMBAAGjQjBAMA8GA1UdEwEB/wQFMAMBAf8wHQYDVR0OBBYEFEs4OTeXKUQHe4BSEA5NmCLfGxGYMA4GA1UdDwEB/wQEAwIChDANBgkqhkiG9w0BAQsFAAOCAQEAKCi2SdX6eYAmrIXtPCYVUzZAzVvSFL4+1ZIRHTCa6Og/2pfYZejyaUUzxgi3Po2PmZtRih42z7vPzYG14g3v3sm9RhguwyYymvpMnKvT5jBq3szMXyRF9gmoElttqEcCHdDOta758JpI2Zkh+kkJwnaLHMk560sYyQc1PHi7+k/7vf+pf7n4jVZHPqRUWggXdZ7fF55Lt/POo9aDCQ3u7hjQaNypdM7hzbrWcxPVFo8f/l136ZsQ8bph1UUK3oF0l1UsJW8bM05Wre1aqjwegQaYRgOHORk+Iwql5T6YpFrZ5gqytqRdEp0IsOkadEvykWjW8PgnatbZVG7p1kwjTg==
-----END CERTIFICATE-----"""),
    'JWT_ALGORITHM': 'RS256',
    'JWT_AUDIENCE': 'uDYqwYL0v0lMobZ24ywbkbWTLxiynUj7', # client ID
    'JWT_PAYLOAD_GET_USERNAME_HANDLER': user_handler
}

AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# TODO(worxli): use this in docker
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',
#         'USER': 'postgres',
#         'HOST': 'db',
#         'PORT': 5432,
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# CORS: Should later be a whitelist and not ALLOW-ALL
CORS_ORIGIN_ALLOW_ALL = True
