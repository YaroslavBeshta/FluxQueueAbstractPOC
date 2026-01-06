import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


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

    # Validate that all required values are present
    if not all([_user, _password, _host, _port, _database]):
        missing = [
            k
            for k, v in {
                "POSTGRES_USER": _user,
                "POSTGRES_PASSWORD": _password,
                "POSTGRES_HOST": _host,
                "POSTGRES_PORT": _port,
                "POSTGRES_DB": _database,
            }.items()
            if not v
        ]
        raise ValueError(
            f"Missing required database environment variables: {', '.join(missing)}"
        )

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
