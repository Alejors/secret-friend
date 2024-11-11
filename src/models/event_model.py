from sqlalchemy import Column, Integer, String, ForeignKey, Table, UniqueConstraint, TIMESTAMP, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.frameworks.db.sqlalchemy.sqlalchemy_client import Base
from src.models.base_model import SQLAlchemyBaseModel


class Event(SQLAlchemyBaseModel, Base):
  __tablename__ = 'events'
  
  id = Column(Integer, primary_key=True)
  name = Column(String(50), nullable=False)
  owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  min_price = Column(Integer)
  max_price = Column(Integer)
  drawn = Column(Boolean, default=False)
  
  event_users = Table(
    'event_users',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True, nullable=False),
    Column('event_id', Integer, ForeignKey('events.id'), primary_key=True, nullable=False),
    Column('pick_id', Integer, ForeignKey('users.id'), nullable=True),
    Column('created_at', TIMESTAMP, server_default=func.now(), nullable=False),
    Column('updated_at', TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp(), nullable=False),
    Column('deleted_at', TIMESTAMP),
    UniqueConstraint('user_id', 'event_id', name='uix_user_event')
  )
  
  owner = relationship("User", foreign_keys=[owner_id], viewonly=True, lazy="joined")
  users = relationship(
    "User", 
    secondary=event_users, 
    backref="events", 
    lazy="joined", 
    primaryjoin="Event.id == event_users.c.event_id", 
    secondaryjoin="and_(User.id == event_users.c.user_id, event_users.c.deleted_at == None)"
  )
  
  __table_args__ = (
    UniqueConstraint('name', 'owner_id', name='uix_name_owner'),
  )

  @classmethod
  def from_dict(cls, _dict: dict):
    return Event(
      id=_dict.get("id"),
      name=_dict.get("name"),
      owner_id=_dict.get("owner_id"),
      min_price=_dict.get("min_price"),
      max_price=_dict.get("max_price"),
      drawn=_dict.get("drawn")
    )
    
  def serialize_event(self) -> dict:
    event_users = self.users
    event_owner = self.owner
    event_data = self.serialize()
    event_data["owner"] = event_owner.serialize_user()
    del event_data["owner_id"]
    event_data["users"] = [user.serialize_user() for user in event_users]
    return event_data