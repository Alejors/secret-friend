from src.interfaces import IUser
from .base_repository import SQLAlchemyBaseRepository
from src.entities import User
from src.models import map_user


class SQLAlchemyUsersRepository(IUser, SQLAlchemyBaseRepository):
  def __init__(self, sqlalchemy_client):
    IUser.__init__(self, sqlalchemy_client)
    SQLAlchemyBaseRepository.__init__(self, sqlalchemy_client, User)
    map_user(sqlalchemy_client)