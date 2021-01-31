from config.settings.base import *
from config.settings.base import env


# Development specific settings

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = env.str("DJANGO_ALLOWED_HOSTS").split(" ")

# Add INSTALLED_APPS on top
INSTALLED_APPS = [] + INSTALLED_APPS
# Add INSTALLED_APPS at bottom
INSTALLED_APPS += ['django_extensions', ]

# Add MIDDLEWARE on top
MIDDLEWARE = [] + MIDDLEWARE
# Add MIDDLEWARE at bottom
MIDDLEWARE += []

ROOT_URLCONF = 'config.urls.local'

WSGI_APPLICATION = 'config.wsgi.application'

# django-extensions
# runserver_plus
RUNSERVERPLUS_SERVER_ADDRESS_PORT = '0.0.0.0:8000'
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console", "mail_admins"],
            "propagate": True,
        },
    },
}
# Truncate printing of SQL queries to this many characters (None means no truncation)
RUNSERVER_PLUS_PRINT_SQL_TRUNCATE = None
# After how many seconds auto-reload should scan for updates in poller-mode
RUNSERVERPLUS_POLLER_RELOADER_INTERVAL = 5
# Werkzeug reloader type [auto, watchdog, or stat]
RUNSERVERPLUS_POLLER_RELOADER_TYPE = 'auto'
# Add extra files to watch
RUNSERVER_PLUS_EXTRA_FILES = []

# Email Settings
# Allows to see the email output in the console window
EMAIL_BACKEND = env.int(
    "EMAIL_BACKEND", default='django.core.mail.backends.console.EmailBackend')
DEFAULT_FROM_EMAIL = env.int(
    "EMAIL_HOST_PASSWORD", default='no-reply@yourdomain.com')
