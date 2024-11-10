from .base_repository import SQLAlchemyBaseRepository
from src.entities import User
from src.models import map_user


class SQLAlchemyUsersRepository(SQLAlchemyBaseRepository):
  def __init__(self, sqlalchemy_client):
    super().__init__(sqlalchemy_client, User)
    map_user(sqlalchemy_client)
