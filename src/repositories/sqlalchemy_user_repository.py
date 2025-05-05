from .base_repository import SQLAlchemyBaseRepository
from src.models import UserModel


class SQLAlchemyUsersRepository(SQLAlchemyBaseRepository):
    def __init__(self, sqlalchemy_client):
        super().__init__(sqlalchemy_client, UserModel)
