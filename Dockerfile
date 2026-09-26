FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT="/opt/venv" \
    PATH="/opt/venv/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc nodejs npm \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

WORKDIR /app

# Создаем группу, пользователя и явно создаем домашнюю директорию для Gunicorn
RUN addgroup --system djangogroup && \
    adduser --system --ingroup djangogroup djangouser && \
    mkdir -p /app/staticfiles /app/media /home/djangouser && \
    chown -R djangouser:djangogroup /app /home/djangouser

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY . .

# Применяем права финально после копирования всего кода
RUN chown -R djangouser:djangogroup /app /home/djangouser

# Явно задаем домашнюю директорию на папку, к которой у пользователя 100% есть доступ
ENV HOME=/home/djangouser

USER djangouser
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--worker-tmp-dir", "/dev/shm", "config.wsgi:production"]
