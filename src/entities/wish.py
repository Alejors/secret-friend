from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Wish:
    id: int
    user_id: int
    element: str
    price: Optional[int]
    url: Optional[str]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    @classmethod
    def from_model(cls, model: "WishModel") -> "Wish":
        """Crea una instancia de Wish a partir de un WishModel."""
        return cls(
            id=model.id,
            user_id=model.user_id,
            element=model.element,
            price=model.price,
            url=model.url,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
        )