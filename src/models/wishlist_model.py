from sqlalchemy import Column, Integer, String, ForeignKey

from src.frameworks.db.sqlalchemy.sqlalchemy_client import Base
from src.models.base_model import SQLAlchemyBaseModel


class WishModel(SQLAlchemyBaseModel, Base):
    __tablename__ = "wishlist"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    element = Column(String(50), nullable=False)
    price = Column(Integer, nullable=True)
    url = Column(String(250), nullable=True)

    @classmethod
    def from_dict(cls, _dict: dict):
        return WishModel(
            id=_dict.get("id"),
            user_id=_dict.get("user_id"),
            element=_dict.get("element"),
            price=_dict.get("price"),
            url=_dict.get("url"),
        )
