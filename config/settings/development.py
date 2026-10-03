import socket
from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]
SECRET_KEY = SECRET_KEY or "django-insecure-local-only"

INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

# В Docker запрос приходит с IP шлюза сети (x.x.x.1), а не с 127.0.0.1
_, _, _ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = ["127.0.0.1"] + [ip.rsplit(".", 1)[0] + ".1" for ip in _ips]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
