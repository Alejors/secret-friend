from sqlalchemy import Column, Integer, String, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import relationship

from src.frameworks.db.sqlalchemy import Base
from src.models.base_model import SQLAlchemyBaseModel


class Event(SQLAlchemyBaseModel, Base):
  
  event_users = Table(
    'event_users',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True, nullable=False),
    Column('event_id', Integer, ForeignKey('events.id'), primary_key=True, nullable=False),
    Column('pick_id', Integer, ForeignKey('users.id'), nullable=True),
    UniqueConstraint('user_id', 'event_id', name='uix_user_event')
  )
  
  __tablename__ = 'events'
  
  id = Column(Integer, primary_key=True)
  name = Column(String(50), nullable=False)
  owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  min_price = Column(Integer)
  max_price = Column(Integer)
  
  owner = relationship("User", foreign_keys=[owner_id], viewonly=True, lazy="joined")
  users = relationship(
    "User", 
    secondary=event_users, 
    backref="events", 
    lazy="joined", 
    primaryjoin="Event.id == event_users.c.event_id", 
    secondaryjoin="User.id == event_users.c.user_id"
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
      max_price=_dict.get("max_price")
    )