from sqlalchemy import Column, Integer, String

from src.frameworks.db.sqlalchemy.sqlalchemy_client import Base
from src.models.base_model import SQLAlchemyBaseModel


class User(SQLAlchemyBaseModel, Base):
  __tablename__ = "users"
  
  id = Column(Integer, primary_key=True)
  name = Column(String(50), nullable=False)
  email = Column(String(100), nullable=False, unique=True)
  password = Column(String(250), nullable=False)

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
