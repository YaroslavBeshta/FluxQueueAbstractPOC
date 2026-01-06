# Infrastructure Dockerfiles

This directory contains Dockerfiles for each service in the application.

## Dockerfiles

### `Dockerfile.postgres`
PostgreSQL database container with:
- PostgreSQL 14
- Python 3 runtime for running Alembic migrations
- Custom entrypoint that runs migrations on startup
- All application dependencies installed

**Usage:** Used by the `db` service in docker-compose files.

### `Dockerfile.telegram_bot`
Telegram bot service container with:
- Python 3.13-slim base image
- All application dependencies
- Telegram bot application code
- Entrypoint configured to run `apps/telegram_bot/main.py`

**Usage:** Used by the `telegram_bot` service in docker-compose files.

### `Dockerfile.notifier`
Notifications service container with:
- Python 3.13-slim base image
- All application dependencies
- Notifications application code
- Entrypoint configured to run `apps/notifications/main.py`

**Usage:** Used by the `notifier` service in docker-compose files.

## Building Images

Images are automatically built by docker-compose when you run:
```bash
make dev-up    # Development environment
make prod-up   # Production environment
```

To build a specific image manually:
```bash
# PostgreSQL
docker build -f infrastructure/Dockerfile.postgres -t fluxqueue-postgres .

# Telegram Bot
docker build -f infrastructure/Dockerfile.telegram_bot -t fluxqueue-telegram-bot .

# Notifier
docker build -f infrastructure/Dockerfile.notifier -t fluxqueue-notifier .
```

## Notes

- All Dockerfiles use the project root as the build context (`.`)
- Environment variables are passed via `.env.dev` or `.env.prod` files
- Secrets should never be baked into images - always use environment variables
- The postgres Dockerfile includes migration support that runs automatically on container startup

