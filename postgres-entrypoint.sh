#!/bin/bash
set -e

# Execute the original postgres entrypoint in the background
/usr/local/bin/docker-entrypoint.sh "$@" &
POSTGRES_PID=$!

# Function to run migrations after postgres is ready
run_migrations() {
    echo "Waiting for PostgreSQL to be ready for migrations..."
    # Wait for postgres to accept connections (with timeout)
    local max_attempts=60
    local attempt=0
    
    until pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" -h 127.0.0.1 -p 5432 > /dev/null 2>&1; do
        attempt=$((attempt + 1))
        if [ $attempt -ge $max_attempts ]; then
            echo "ERROR: PostgreSQL did not become ready in time"
            exit 1
        fi
        sleep 1
    done

    # Give postgres a moment to fully initialize
    sleep 2

    echo "PostgreSQL is ready - running Alembic migrations..."
    cd /app
    alembic upgrade head
    echo "Migrations completed successfully!"
}

# Wait for postgres to be ready, then run migrations
run_migrations

# Wait for the postgres process (this keeps the container running)
wait $POSTGRES_PID

