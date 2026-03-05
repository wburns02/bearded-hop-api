import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base
# Import all models so Base.metadata knows about them
from app.models import user, beer, recipe, detailed_recipe, batch, gravity_reading
from app.models import tap_line, keg, keg_event, customer, visit_record, customer_note
from app.models import event, performer, reservation, open_tab, tab_item
from app.models import pos_transaction, transaction_item, floor_table, service_alert
from app.models import order_timeline, menu_item, inventory_item, purchase_order
from app.models import staff_member, staff_certification, schedule_shift
from app.models import wholesale_account, wholesale_order, mug_club_member
from app.models import email_campaign, daily_sales, monthly_financial, ttb_report
from app.models import compliance_item, social_metrics, content_calendar
from app.models import customer_segment, business_settings
from app.config import settings

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_url():
    return settings.async_database_url


def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
