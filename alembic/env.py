from __future__ import annotations

from logging.config import fileConfig
from pathlib import Path
import os
import sys

from alembic import context
from sqlalchemy import engine_from_config, pool

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Ensure the services/backend package root is on sys.path so imports resolve.
BASE_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = BASE_DIR / "services" / "backend"
# Add backend directory FIRST to prioritize local imports
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# Import metadata for 'autogenerate' support.
from database import Base  # type: ignore  # noqa: E402
from Database.Models import *  # noqa: E402,F401,F403

target_metadata = Base.metadata


def get_sqlalchemy_url() -> str:
    """Determine the SQLAlchemy database URL for migrations."""
    url = config.get_main_option("sqlalchemy.url")
    if url and url != "sqlite://":
        return url

    env_url = os.getenv("SQLALCHEMY_DATABASE_URL")
    if env_url:
        return env_url

    if os.getenv("TESTING", "0") == "1":
        return "sqlite:///./test.db"

    user = os.getenv("DATABASE_USER", "")
    password = os.getenv("DATABASE_PASSWORD", "")
    host = os.getenv("DATABASE_HOST", "localhost")
    port = os.getenv("DATABASE_PORT", "5432")
    name = os.getenv("DATABASE_NAME", "")
    return f"postgresql://{user}:{password}@{host}:{port}/{name}"


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_sqlalchemy_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    config.set_main_option("sqlalchemy.url", get_sqlalchemy_url())
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
