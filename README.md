<p align="center"><a href="https://profiflow.pro" target="_blank">
    <img src="docs/img/profiflow.jpeg" alt="ProfiFlow Logo">
</a></p>

Cервис онлайн-записи для бьюти-мастеров и небольших студий.

## Стек технологий

![Debian](https://img.shields.io/badge/Debian-OS-A81D33?logo=debian&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-v2-2496ED?logo=docker&logoColor=white) ![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white) ![uv](https://img.shields.io/badge/uv-Manager-8A2BE2) ![Django](https://img.shields.io/badge/Django-6.1-092E20?logo=django&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-4169E1?logo=postgresql&logoColor=white) ![Redis](https://img.shields.io/badge/Redis-8-DC382D?logo=redis&logoColor=white) ![Nginx](https://img.shields.io/badge/Nginx-1.31-009639?logo=nginx&logoColor=white)

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

3. **Сборка и запуск контейнеров (Make):**

```bash
make build
make up
```

4. **Настройка Django:**

```bash
make migrate        # Применение миграций БД
make collectstatic  # Сборка статики для Nginx
make superuser      # Создание панели администратора + cоздание суперпользователя
````

3. **Миграции:**

```bash
make makemigrations
make migrate
```

Открыть в браузере `http://localhost/` или `http://profiflow.loc/`

---

## Дополнительно

- [Шпаргалка по командам Make](docs/make.md)

