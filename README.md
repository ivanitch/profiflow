# ProfiFlow

Cервис онлайн-записи для бьюти-мастеров и студий.

## Технологический стек

- **Ядро:** Python 3.14, Django 6.x
- **База данных и кэш:** PostgreSQL 18, Redis 8
- **Инфраструктура:** Docker Compose, Gunicorn + Nginx
- **Фронтенд:** TailwindCSS, DaisyUI
- **Инструменты:** `uv` (управление пакетами), pytest, ruff, mypy
- **CI/CD:** GitHub Actions, строгое разделение локального и продакшен-окружения (`django-environ`)

## Возможности

- **Строгое разделение окружений:** Изолированная логика для локальной разработки и продакшена.
- **Безупречный Docker:** Никаких конфликтов прав root на Linux/Mac. `uv` для молниеносного управления пакетами.
- **Fail-Fast безопасность:** Продакшен-сервер отказывается запускаться при неверной конфигурации `.env`.
- **Готовность к Nginx и HTTPS:** Самодостаточный прокси, кэш-бастинг статики и лёгкое продление сертификатов через Certbot.
- **Hot-Reload Tailwind:** Нативная интеграция внутри локального контейнера, без лишних локальных зависимостей.

---

## 💻 Локальная разработка

1. **Клонируйте репозиторий:**

```bash
git clone https://github.com/ivanitch/profiflow.git profiflow
cd profiflow
```

2. **Настройте переменные окружения:**

```shell
cp .env.example .env
```

3. **Запустите проект с помощью Makefile:**

```bash
make up
```

Эта команда соберёт образы, запустит базу данных и запустит Django + наблюдатель Tailwind.

4. **Примените миграции и создайте суперпользователя:**

```bash
make migrate
make bash
# Внутри контейнера:
python manage.py createsuperuser
````

5. **Просмотр локальных логов:**

```bash
make logs

make logs db
```

Приложение доступно по адресу: http://localhost:8000

---

## 🌍 Продакшен-развёртывание (VPS)

Продакшен работает в строгой изоляции. Он не зависит от локального docker-compose.yml. Node.js и dev-пакеты
удалены из финального образа.

1. **Клонируйте на ваш VPS:**

```bash
git clone https://github.com/ivanitch/profiflow.git profiflow
cd profiflow
````

2. **Настройте продакшен-параметры:**

```bash
cp .env.prod.example .env.prod
nano .env.prod
````

Убедитесь, что сгенерирован надёжный `SECRET_KEY`, установлен `DEBUG=False`, обновлён `ALLOWED_HOSTS` и указан точный `URL` в
`CSRF_TRUSTED_ORIGINS`. Добавьте ваши домены (`DOMAIN`, `WWW_DOMAIN`), `CERTBOT_EMAIL`, настройте учётные данные PostgreSQL (
`POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`) и настройте переменные SMTP-почты.

3. **🔒 SSL через Certbot (первоначальная настройка):**

```bash
make prod-init-ssl
```

Эта команда соберёт продакшен-образ, применит миграции, выполнит collectstatic в Docker-том и безопасно перезапустит
контейнеры web и nginx

4. **Деплой (без простоя)**

```bash
make prod-deploy
````

Эта команда соберёт `prod-образ`, применит `миграции`, выполнит `collectstatic` в Docker-том и безопасно
перезапустит контейнеры `web` и `nginx`.

5. **Просмотр продакшен-логов:**

```bash
make prod-logs
```
[Подробная инструкции по развёртыванию в продакшене](docs/production.md)

---

## Настройка CI/CD (GitHub Actions)

[Подробная информация о настройках CI/CD](docs/ci-cd.md)

---

## Дополнительно

- [Шпаргалка по командам Make](docs/make.md)
- [Шпаргалка: Tailwind + Django (uv)](docs/tailwind.md)
- [Подробная инструкции по развёртыванию в продакшене](docs/production.md)
- [Подробная информация о настройках CI/CD](docs/ci-cd.md)
