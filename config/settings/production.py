from config.settings.base import *
from config.settings.base import env

# Production specific settings

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: don't run with MIMIC_PRODUCTION_LOCALLY turned on in production!
# This setting is only for testing the actual production setup locally (Without SSL)
# It is recommended to use SSL based container (dc-ssl-production) is you have SSL
MIMIC_PRODUCTION_LOCALLY = env.bool("MIMIC_PRODUCTION_LOCALLY", False)

# The URL on which the project is hosted (example 0.0.0.0)
ALLOWED_HOSTS = env.str("DJANGO_ALLOWED_HOSTS").split(" ")

# ADMINS = [
#     (
#         env.str("WEBMASTER_NAME", default="Webmaster"),
#         env.str("WEBMASTER_EMAIL", default="webmaster@test.infroid.com")
#     ),
#     (
#         env.str("ADMINISTRATOR_NAME", default="Administrator"),
#         env.str("ADMINISTRATOR_EMAIL", default="administrator@test.infroid.com")
#     )
# ]
# MANAGERS = ADMINS

# Add INSTALLED_APPS on top
INSTALLED_APPS = [] + INSTALLED_APPS
# Add INSTALLED_APPS at bottom
INSTALLED_APPS += ['admin_honeypot', ]

# Add MIDDLEWARE on top
MIDDLEWARE = ['django.middleware.cache.UpdateCacheMiddleware', ] + MIDDLEWARE
# Add MIDDLEWARE at bottom
MIDDLEWARE += ['django.middleware.cache.FetchFromCacheMiddleware', ]

ROOT_URLCONF = 'config.urls.production'

WSGI_APPLICATION = 'config.wsgi.application'

# Cache config
CACHE_MIDDLEWARE_ALIAS = 'default'
# TODO-NORMAL: Update to 7 days once working properly
CACHE_MIDDLEWARE_SECONDS = 3600
CACHE_MIDDLEWARE_KEY_PREFIX = ''

# Security config
if MIMIC_PRODUCTION_LOCALLY:
    pass
else:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    # TODO-NORMAL: Update to 7 days or 30 days once working properly
    SECURE_HSTS_SECONDS = env.int("DJANGO_SECURE_HSTS_SECONDS", default=3600)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    CSRF_COOKIE_SECURE = True

# Email Settings
# GMAIL SMTP: https://dev.to/abderrahmanemustapha/how-to-send-email-with-django-and-gmail-in-production-the-right-way-24ab
EMAIL_BACKEND = env.str(
    "EMAIL_BACKEND", default='django.core.mail.backends.smtp.EmailBackend')
DEFAULT_FROM_EMAIL = env.str(
    "DEFAULT_FROM_EMAIL", default='no-reply@yourdomain.com')
EMAIL_HOST = env.str("EMAIL_HOST", default='smtp.gmail.com')
EMAIL_HOST_USER = env.str(
    "EMAIL_HOST_USER", default='yoorusername@yourdomain.com')
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default='app key or pass')
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_USE_TLS = True

# Admin Honeypot config
ADMIN_HONEYPOT_EMAIL_ADMINS = True
