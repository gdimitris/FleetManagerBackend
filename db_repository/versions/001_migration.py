from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
Researchers = Table('Researchers', post_meta,
    Column('phone_id', String(length=80), primary_key=True, nullable=False),
    Column('name', String(length=80), nullable=False),
    Column('surname', String(length=80), nullable=False),
    Column('last_updated', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['Researchers'].columns['last_updated'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['Researchers'].columns['last_updated'].drop()
