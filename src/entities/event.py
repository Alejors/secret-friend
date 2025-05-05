from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
from src.entities.user import User


@dataclass
class Event:
    id: int
    name: str
    owner: User
    min_price: Optional[int]
    max_price: Optional[int]
    drawn: bool
    users: List[User]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    @classmethod
    def from_model(cls, model: "EventModel") -> "Event":
        """Crea una instancia de Event a partir de un EventModel."""
        return cls(
            id=model.id,
            name=model.name,
            owner=User.from_model(model.owner),
            min_price=model.min_price,
            max_price=model.max_price,
            drawn=model.drawn,
            users=[User.from_model(user) for user in model.users],
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
        )