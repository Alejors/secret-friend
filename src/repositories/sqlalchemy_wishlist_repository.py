from .base_repository import SQLAlchemyBaseRepository
from src.entities import Wish
from src.models import map_wishlist


class SQLAlchemyWishlistRepository(SQLAlchemyBaseRepository):
  def __init__(self, sqlalchemy_client):
    super().__init__(sqlalchemy_client, Wish)
    map_wishlist(sqlalchemy_client)
