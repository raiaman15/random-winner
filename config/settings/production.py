from config.settings.base import *
from config.settings.base import env

# Production specific settings

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

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

# django-allauth config
# FIX-URGENT: Change to production specific email backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Cache config
CACHE_MIDDLEWARE_ALIAS = 'default'
# TODO-NORMAL: Update to 7 days once working properly
CACHE_MIDDLEWARE_SECONDS = 3600
CACHE_MIDDLEWARE_KEY_PREFIX = ''

# Security config
if env.bool("MIMIC_PRODUCTION_LOCALLY", False):
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
EMAIL_BACKEND = env.int(
    "EMAIL_BACKEND", default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = env.int("EMAIL_HOST", default='smtp.gmail.com')
EMAIL_HOST_USER = env.int(
    "EMAIL_HOST_USER", default='yoorusername@yourdomain.com')
EMAIL_HOST_PASSWORD = env.int("EMAIL_HOST_PASSWORD", default='app key or pass')
EMAIL_PORT = env.int("EMAIL_HOST_PASSWORD", default=587)
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = env.int(
    "EMAIL_HOST_PASSWORD", default='no-reply@yourdomain.com')

# Admin Honeypot config
ADMIN_HONEYPOT_EMAIL_ADMINS = True
