# ProfiFlow

Cервис онлайн-записи для бьюти-мастеров и студий.

## Стек технологий

<p align="left">
  <img src="https://img.shields.io/badge/python-3.14-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/django-6.x-092E20?logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/postgres-18-316192?logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/redis-8-DC382D?logo=redis&logoColor=white" alt="Redis">
  <img src="https://img.shields.io/badge/docker--compose-2496ED?logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/tailwindcss-38B2AC?logo=tailwind-css&logoColor=white" alt="TailwindCSS">
  <img src="https://img.shields.io/badge/uv-manager-8A2BE2?logo=python&logoColor=white" alt="uv">
</p>

## Быстрый старт

1. **Клонирование репозитория:**

```bash
git clone git@github.com:ivanitch/profiflow.git profiflow
cd profiflow
```

2. **Настройка окружения:**

```bsah
cp .env.example .env
```

3. **Запуск проекта (Make):**

```bash
make up
```

This builds images, starts the database, and launches Django + Tailwind watcher.

4. **Миграции и `superuser`:**

```bash
make migrate
make bash
# Inside container:
python manage.py createsuperuser
````

5. **Логи:**

```bash
make logs

make logs db
```

Открыть в браузере `http://localhost/:8000`

---

## Дополнительно

- [Шпаргалка по командам Make](docs/make.md)
- [Шпаргалка: Tailwind + Django](docs/tailwind.md)
- [Настройка CI/CD (GitHub Actions)](docs/ci.md)

