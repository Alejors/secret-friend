from .base_repository import SQLAlchemyBaseRepository
from src.models import Wish


class SQLAlchemyWishlistRepository(SQLAlchemyBaseRepository):
  def __init__(self, sqlalchemy_client):
    super().__init__(sqlalchemy_client, Wish)
