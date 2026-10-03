from django.core.exceptions import ImproperlyConfigured
from .base import *

DEBUG = False

if not SECRET_KEY or SECRET_KEY.startswith("django-insecure"):
    raise ImproperlyConfigured("SECRET_KEY не задан или небезопасен")
if not ALLOWED_HOSTS:
    raise ImproperlyConfigured("ALLOWED_HOSTS пуст")

# nginx завершает TLS и передаёт X-Forwarded-Proto
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS отдаёт nginx — в Django не дублируем
SILENCED_SYSTEM_CHECKS = ["security.W004"]

# Хэш в именах статики → после деплоя браузер сразу берёт новый CSS
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"},
}
