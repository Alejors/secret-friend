from sqlalchemy import Table, Column, Integer, ForeignKey, UniqueConstraint

from src.frameworks.db.sqlalchemy import Base


event_users = Table(
    'event_users',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True, nullable=False),
    Column('event_id', Integer, ForeignKey('events.id'), primary_key=True, nullable=False),
    Column('pick_id', Integer, ForeignKey('users.id'), nullable=True),
    UniqueConstraint('user_id', 'event_id', name='uix_user_event')
)
