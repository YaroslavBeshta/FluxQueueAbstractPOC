# Use a stable, small base
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# System deps you may need for wheels like psycopg, lxml, etc.
# Add or remove libs as needed.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 1) Copy only dependency metadata first for better Docker caching
COPY pyproject.toml pyproject.toml
COPY requirements.txt requirements.txt

# 2) Upgrade pip and basic build tools
RUN pip install --upgrade pip wheel setuptools

# 3) Install requirements (if you actually use requirements.txt)
#    If you manage deps only with pyproject, you can delete this line.
RUN pip install -r requirements.txt

# 4) Now copy your importable packages and install your project
#    This assumes your real code lives in /packages per your layout
COPY packages/ packages/
RUN pip install -e .

# 5) Copy the rest of the app code and configs
COPY apps/ apps/
COPY alembic.ini ./alembic.ini
# If your alembic folder lives under apps/alembic, bring it in to /app/alembic
# Adjust or remove this if your project uses another path
COPY apps/alembic/ ./alembic/

# Do not bake secrets into the image in production. Prefer env vars.
# Kept here because your original had it.
COPY .env .env

ENV PYTHONPATH=/app

COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
