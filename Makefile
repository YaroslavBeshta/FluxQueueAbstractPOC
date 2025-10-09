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


run:
	docker compose -f prod-postgres-docker-compose.yml up -d --build

stop:
	docker compose -f prod-postgres-docker-compose.yml stop