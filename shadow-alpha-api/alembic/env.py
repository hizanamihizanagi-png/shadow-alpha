"""
Alembic env.py - async migration support.
"""

import asyncio
import os
import sys
from logging.config import fileConfig

# Add the parent directory to sys.path so 'app' can be resolved
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import settings
from app.db.base import Base

# Import ALL models so they register with Base.metadata
from app.models.user import User  # noqa
from app.models.position import Position  # noqa
from app.models.order import Order, Trade  # noqa
from app.models.tontine import TontineGroup, TontineMember, TontineContribution  # noqa
from app.models.loan import Loan  # noqa
from app.models.subscription import Subscription  # noqa
from app.models.vault import VaultDeposit, VaultYield  # noqa
from app.models.shield import ShieldContract, ShieldClaim  # noqa
from app.models.gratitude import GratitudeTip  # noqa
from app.models.position_loan import PositionLoan  # noqa

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in 'online' mode with async engine."""
    connectable = create_async_engine(settings.DATABASE_URL)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

