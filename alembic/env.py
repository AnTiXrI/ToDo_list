import sys
import os
from logging.config import fileConfig

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import sessionmaker

from alembic import context

# Определите путь к вашей модели
from models import Base  # Импортируйте Base из вашего модуля моделей

# This line sets up the Alembic configuration
config = context.config

# Setup logging configuration
fileConfig(config.config_file_name)

# Set the target metadata for autogenerate support
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode.
    This configures the context with a URL and doesn't connect
    to a database; instead it generates a .sql file with the
    SQL commands needed to apply the migrations.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode.
    In this mode, Alembic connects to the database and applies
    migrations directly.
    """
    engine = create_engine(config.get_main_option("sqlalchemy.url"))
    connection = engine.connect()
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()

    connection.close()

# Run migrations based on the command line argument
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
