# Profi Flow

Cервис онлайн-записи для бьюти-мастеров и небольших студий.

## Стек технологий

* **OS:** Linux/Debian
* **Инфраструктура:** Docker, Docker Compose (`v2`), Make
* **Язык:** Python `3.12+`
* **Менеджер пакетов:** `uv`
* **Фреймворк:** Django `6.1`
* **База данных:** PostgreSQL `18`
* **Кэш / Брокер:** Redis `8`
* **Веб-сервер:** Nginx `1.31`

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

3. **Сборка и запуск контейнеров:**

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

## Шпаргалка по командам (Make)

```bash
make                # Вызов `make help` - просмотр всех команд

## --- Управление контейнерами ---
make build    # Собрать/Пересобрать образы
make up       # Запустить проект в фоне
make down     # Остановить контейнеры (данные в БД сохраняются)
make destroy  # Остановить и полностью удалить контейнеры и данные БД
make logs     # Смотреть логи всех сервисов
make logs-web # Смотреть логи только Django
make logs-db  # Смотреть логи только Postgresql

## --- Работа с Django ---
make shell          # Зайти внутрь контейнера с Django (bash)
make db-shell       # Зайти внутрь контейнера с Postgresql
make makemigrations # Создать миграции БД
make migrate        # Применить миграции БД
make superuser      # Новый супер-пользователь

## --- Terminal workflow ---
# Зайти внутрь контейнера с Django
make shell
# -> команды внутри контейнера с Django
python manage.py shell          # Запустить интерактивную оболочку Django
python manage.py makemigrations # Создать миграции БД
python manage.py  migrate       # Применить миграции БД
```
