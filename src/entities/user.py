from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class User:
    id: int
    name: str
    email: str
    password: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    @classmethod
    def from_model(cls, model: "UserModel") -> "User":
        """Crea una instancia de User a partir de un UserModel."""
        return cls(
            id=model.id,
            name=model.name,
            email=model.email,
            password=model.password,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
        )
