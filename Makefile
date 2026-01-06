install:
	pip install -e .

migrate:
	alembic upgrade head

make-migration:
	alembic revision --autogenerate -m "Add migration"

run-tg:
	python apps/telegram_bot/main.py

run-notif:
	python apps/notifications/main.py

# Development commands
dev-up:
	docker compose -f docker-compose.dev.yml up -d --build

dev-down:
	docker compose -f docker-compose.dev.yml down

dev-logs:
	docker compose -f docker-compose.dev.yml logs -f

dev-stop:
	docker compose -f docker-compose.dev.yml stop

dev-restart:
	docker compose -f docker-compose.dev.yml restart

# Production commands
prod-up:
	docker compose -f docker-compose.prod.yml up -d --build

prod-down:
	docker compose -f docker-compose.prod.yml down

prod-logs:
	docker compose -f docker-compose.prod.yml logs -f

prod-stop:
	docker compose -f docker-compose.prod.yml stop

prod-restart:
	docker compose -f docker-compose.prod.yml restart

# Legacy aliases (for backward compatibility)
start: prod-up
stop: prod-stop