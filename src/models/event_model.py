from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.entities import Event


def map_event(sqlalchemy_client):
  
  event_users = Table(
    'event_users',
    sqlalchemy_client.mapper_registry.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
    Column('event_id', Integer, ForeignKey('events.id'), nullable=False),
    Column('pick_id', Integer, ForeignKey('users.id'), nullable=True)
  )
  
  sqlalchemy_client.map_entity_to_table(
    Event,
    "events",
    [
      Column("id", Integer, primary_key=True),
      Column("name", String(50), nullable=False),
      Column("owner_id", ForeignKey("users.id"), nullable=False),
      Column("min_amount", Integer),
      Column("max_amount", Integer),
    ],
    properties={
      "owner": relationship(
        "User",
        innerjoin=True,
        viewonly=True,
        lazy="joined"
      ),
      "users": relationship(
        "User",
        secondary=event_users,
        back_populates="events",
        lazy="joined",
        primaryjoin="events.id == event_users.c.event_id"
      )
    }
  )
