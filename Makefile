# Variables
DC = docker compose
EXEC = $(DC) exec web
LOGS = $(DC) logs

# Default target
.DEFAULT_GOAL := help

# PHONY targets
.PHONY: build up down destroy restart ps logs logs-web shell db-shell migrate makemigrations superuser collectstatic help

build:
	$(DC) build

up:
	$(DC) up -d

down:
	$(DC) down

destroy:
	$(DC) down -v

restart:
	$(DC) restart

ps:
	$(DC) ps

logs:
	$(LOGS) -f

logs-web:
	$(LOGS) -f web

logs-db:
	$(LOGS) -f db

shell:
	$(EXEC) bash

db-shell:
	$(DC) exec db bash

# Django specific commands
migrate:
	$(EXEC) python manage.py migrate

makemigrations:
	$(EXEC) python manage.py makemigrations

superuser:
	$(EXEC) python manage.py createsuperuser

collectstatic:
	$(EXEC) python manage.py collectstatic --noinput

help:
	@echo "Available commands:"
	@echo "  make build           - Build docker images"
	@echo "  make up              - Start containers in background"
	@echo "  make down            - Stop containers (safe: keeps DB data)"
	@echo "  make destroy         - Stop containers and REMOVE volumes (DANGER: deletes DB data!)"
	@echo "  make restart         - Restart all containers"
	@echo "  make ps              - Show container status"
	@echo "  make logs            - Follow all logs"
	@echo "  make logs-web        - Follow Django logs"
	@echo "  make shell           - Enter Django container bash"
	@echo "  make db-shell        - Enter PostgreSQL container bash"
	@echo "  make migrate         - Apply Django migrations"
	@echo "  make makemigrations  - Create new Django migrations"
	@echo "  make superuser       - Create Django superuser"
	@echo "  make collectstatic   - Collect static files for Nginx"
