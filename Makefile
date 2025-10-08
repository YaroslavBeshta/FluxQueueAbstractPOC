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