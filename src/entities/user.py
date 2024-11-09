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
