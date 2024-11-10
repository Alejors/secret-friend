from dataclasses import dataclass
from datetime import datetime

from src.entities.base_entity import BaseEntity


@dataclass
class Wish(BaseEntity):
  id: int | None = None
  user_id: int = None
  event_id: int = None
  element: str | None = None
  url: str | None = None
  created_at: datetime = None
  updated_at: datetime = None
  deleted_at: datetime | None = None
  
  @classmethod
  def from_dict(cls, _dict: dict):
    return Wish(
      id=_dict.get("id"),
      user_id=_dict.get("user_id"),
      event_id=_dict.get("event_id"),
      element=_dict.get("element"),
      url=_dict.get("url")
    )