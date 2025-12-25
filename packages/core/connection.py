import os
from contextlib import contextmanager
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Try loading .env.prod first, fallback to .env
env_prod_path = Path('.env.prod')
if env_prod_path.exists():
    load_dotenv('.env.prod')
else:
    load_dotenv()


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()


def create_connection_string():
    _user = os.getenv("POSTGRES_USER")
    _password = os.getenv("POSTGRES_PASSWORD")
    _host = os.getenv("POSTGRES_HOST")
    _port = os.getenv("POSTGRES_PORT")
    _database = os.getenv("POSTGRES_DB")
    _driver = os.getenv("DB_DRIVER") or "postgresql"

    connection_string = f"{_driver}://{_user}:{_password}@{_host}:{_port}/{_database}"
    return connection_string


SQLALCHEMY_DATABASE_URL = create_connection_string()
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_recycle=3600,
    pool_pre_ping=True,
)
Session = sessionmaker(bind=engine)
session = Session()
