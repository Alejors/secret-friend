from dataclasses import dataclass
from datetime import datetime

from src.entities.base_entity import BaseEntity


@dataclass
class Event(BaseEntity):
  id: int | None = None
  name: str = None
  owner_id: int = None
  min_amount: int | None = None
  max_amount: int | None = None
  created_at: datetime = None
  updated_at: datetime = None
  deleted_at: datetime | None = None
  
  @classmethod
  def from_dict(cls, _dict: dict):
    return Event(
      id=_dict.get("id"),
      name=_dict.get("name"),
      owner_id=_dict.get("owner_id"),
      min_amount=_dict.get("min_amount"),
      max_amount=_dict.get("max_amount")
    )