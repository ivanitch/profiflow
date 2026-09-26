# ================= VARIABLES =================
include .env
export

DC = UID=$$(id -u) GID=$$(id -g) docker compose
DC_PROD = docker compose -f docker-compose.yml -f docker-compose.prod.yml
EXEC = $(DC) exec web
LOGS = $(DC) logs

# ================= SETTINGS =================
.DEFAULT_GOAL := help

.PHONY: build up down destroy restart ps \
        logs logs-web logs-db shell db-shell \
        migrate makemigrations superuser collectstatic startapp \
        db-backup db-restore \
        prod-build prod-up prod-down prod-logs prod-deploy help

# ================= LOCAL ENVIRONMENT =================
build:
	$(DC) build

up:
	mkdir -p media staticfiles # Превентивно создаем папки, чтобы Docker не создал их от root
	$(DC) up -d

down:
	$(DC) down

restart:
	$(DC) restart

ps:
	$(DC) ps

destroy:
	@if [ "$${ENVIRONMENT}" = "production" ] || [ "$${ENVIRONMENT}" = "prod" ]; then \
		echo "Ошибка! Команда 'destroy' заблокирована в production."; \
		exit 1; \
	fi
	@echo "Внимание! Это действие удалит все контейнеры и ТОМА (включая БД)."
	@read -p "Вы уверены, что хотите продолжить? [y/N] " ans && if [ "$${ans:-N}" = "y" ] || [ "$${ans:-N}" = "Y" ]; then \
		$(DC) down -v; \
	else \
		echo "Отменено."; \
	fi

# ================= BACKUPS =================
db-backup:
	@echo "Создание бэкапа базы данных..."
	mkdir -p backups
	$(DC) exec -T db pg_dump -U $(DB_USER) -d $(DB_NAME) -F c > backups/backup_$$(date +%Y%m%d_%H%M%S).dump
	@echo "Бэкап успешно сохранен в папку backups/"

db-restore:
	@if [ -z "$(file)" ]; then \
		echo "Укажите файл (например: make db-restore file=backups/backup_name.dump)"; \
		exit 1; \
	fi
	@echo "Восстановление из $(file)..."
	$(DC) exec -T db pg_restore -U $(DB_USER) -d $(DB_NAME) -c -1 < $(file)
	@echo "Восстановление завершено."

# ================= LOGS =================
logs:
	$(LOGS) -f

logs-web:
	$(LOGS) -f web

logs-db:
	$(LOGS) -f db

# ================= SHELL ACCESS =================
shell:
	$(EXEC) bash

db-shell:
	$(DC) exec db bash

# ================= DJANGO COMMANDS =================
migrate:
	$(EXEC) python manage.py migrate

makemigrations:
	$(EXEC) python manage.py makemigrations

superuser:
	$(EXEC) python manage.py createsuperuser

collectstatic:
	$(EXEC) python manage.py collectstatic --noinput

startapp:
	@if [ -z "$(name)" ]; then \
		echo "Использование: make startapp name=<app_name>"; \
		exit 1; \
	fi
	$(EXEC) python manage.py startapp $(name) apps/$(name)

# ================= PRODUCTION COMMANDS =================
prod-build:
	$(DC_PROD) build

prod-up:
	$(DC_PROD) up -d

prod-down:
	$(DC_PROD) down

prod-logs:
	$(DC_PROD) logs -f

prod-deploy:
	git pull
	$(DC_PROD) build
	$(DC_PROD) up -d
	$(DC_PROD) exec web python manage.py migrate
	$(DC_PROD) exec web python manage.py collectstatic --noinput

# ================= HELP =================
help:
	@echo "Доступные команды:"
	@echo ""
	@echo "--- Локальная разработка ---"
	@echo "  make build           - Собрать docker образы"
	@echo "  make up              - Запустить контейнеры в фоне"
	@echo "  make down            - Остановить контейнеры (безопасно: БД сохраняется)"
	@echo "  make restart         - Перезапустить все контейнеры"
	@echo "  make destroy         - Удалить контейнеры и ТОМА (ОПАСНО: удаляет данные БД!)"
	@echo "  make ps              - Показать статус контейнеров"
	@echo ""
	@echo "--- Бэкапы БД ---"
	@echo "  make db-backup       - Создать дамп базы данных"
	@echo "  make db-restore file=X - Восстановить базу из файла"
	@echo ""
	@echo "--- Логи и консоль ---"
	@echo "  make logs            - Читать все логи"
	@echo "  make logs-web        - Читать логи Django (web)"
	@echo "  make logs-db         - Читать логи БД (Postgres)"
	@echo "  make shell           - Войти в bash контейнера Django"
	@echo "  make db-shell        - Войти в bash контейнера БД"
	@echo ""
	@echo "--- Команды Django ---"
	@echo "  make migrate         - Применить миграции БД"
	@echo "  make makemigrations  - Создать новые миграции"
	@echo "  make superuser       - Создать суперпользователя"
	@echo "  make collectstatic   - Собрать статику"
	@echo "  make startapp name=X - Создать новое приложение в папке apps/"
	@echo ""
	@echo "--- Продакшен ---"
	@echo "  make prod-build      - Собрать образы для продакшена"
	@echo "  make prod-up         - Запустить продакшен контейнеры"
	@echo "  make prod-down       - Остановить продакшен контейнеры"
	@echo "  make prod-logs       - Читать логи продакшена"
	@echo "  make prod-deploy     - Полный цикл деплоя (pull, build, up, migrate, static)"
