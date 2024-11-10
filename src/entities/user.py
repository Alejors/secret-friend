from dataclasses import dataclass
from datetime import datetime

from src.entities.base_entity import BaseEntity


@dataclass
class User(BaseEntity):
  id: int | None = None
  name: str = None
  email: str = None
  password: str | None = None
  created_at: datetime = None
  updated_at: datetime = None
  deleted_at: datetime | None = None
  
  @classmethod
  def from_dict(cls, _dict: dict):
    return User(
      id=_dict.get("id"),
      name=_dict.get("name"),
      email=_dict.get("email"),
      password=_dict.get("password")
    )
    
  def serialize_user(self) -> dict:
    data = self.serialize()
    del data["password"]
    
    return data
