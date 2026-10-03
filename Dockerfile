# syntax=docker/dockerfile:1

# ============ base: общее для dev и prod ============
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

# libpq5 — runtime-библиотека для psycopg 3 (gcc/libpq-dev не нужны)
RUN apt-get update \
 && apt-get install -y --no-install-recommends libpq5 \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

RUN groupadd --system djangogroup \
 && useradd --system --gid djangogroup \
      --home-dir /home/djangouser --create-home djangouser

WORKDIR /app
COPY pyproject.toml uv.lock ./

# ============ dev: локальная разработка ============
FROM base AS dev

RUN apt-get update \
 && apt-get install -y --no-install-recommends nodejs npm \
 && rm -rf /var/lib/apt/lists/*

# вместе с dev-группой (debug-toolbar, pytest, ipython...)
RUN uv sync --locked --no-install-project

# В local код приходит через bind mount; COPY — чтобы образ работал и без него
COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# ============ css: сборка Tailwind ============
FROM node:22-slim AS css
WORKDIR /app
# Tailwind сканирует шаблоны всего проекта, поэтому копируем проект целиком
COPY . .
# ⚠️ ПРОВЕРЬ ПУТЬ: стандарт django-tailwind — <app>/static_src (обычно theme/)
RUN cd theme/static_src && npm ci && npm run build

# ============ prod: итоговый образ ============
FROM base AS prod

RUN uv sync --locked --no-dev --no-install-project

# Код принадлежит root и доступен приложению только на чтение
COPY . .
COPY --from=css /app/theme/static/css/dist/ /app/theme/static/css/dist/

# Приложению доступны на запись только эти каталоги
RUN mkdir -p /app/staticfiles /app/media \
 && chown djangouser:djangogroup /app/staticfiles /app/media

USER djangouser

# Gunicorn сам читает WEB_CONCURRENCY; можно переопределить в compose
ENV WEB_CONCURRENCY=3

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--worker-tmp-dir", "/dev/shm", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--timeout", "30", \
     "--graceful-timeout", "30"]
