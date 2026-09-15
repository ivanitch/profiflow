FROM python:3.12-slim

# Настройки Python и uv
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT="/opt/venv" \
    PATH="/opt/venv/bin:$PATH"

# Системные зависимости (gcc, libpq-dev, плюс nodejs и npm для Tailwind)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc nodejs npm \
    && rm -rf /var/lib/apt/lists/*

# Ставим uv через pip (надежнее, чем тянуть образ с ghcr.io)
RUN pip install --no-cache-dir uv

WORKDIR /app

# Сначала копируем только файлы зависимостей
COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости. uv сам создаст папку .venv
RUN uv sync --frozen --no-dev --no-install-project

# Копируем остальной код проекта
COPY . .

# Команда по умолчанию (для продакшена, локально переопределяется в compose)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
