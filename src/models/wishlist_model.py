from sqlalchemy import Column, Integer, String, ForeignKey

from src.frameworks.db.sqlalchemy import Base
from src.models.base_model import SQLAlchemyBaseModel


class Wish(SQLAlchemyBaseModel, Base):
  __tablename__ = "wishlist"
  
  id = Column(Integer, primary_key=True)
  user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
  element = Column(String(50), nullable=False)
  url = Column(String(250), nullable=True)
  
  @classmethod
  def from_dict(cls, _dict: dict):
    return Wish(
      id=_dict.get("id"),
      user_id=_dict.get("user_id"),
      event_id=_dict.get("event_id"),
      element=_dict.get("element"),
      url=_dict.get("url")
    )