from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*'] 

SECRET_KEY = "  nqtefdctyuuerad8767"

DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "postgres",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "HOST": "postgres",
            "PORT": "5432"
        }
}
try:
    from .local import *
except ImportError:
    pass
