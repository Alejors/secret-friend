from .base_repository import SQLAlchemyBaseRepository
from src.models import WishModel
from src.entities import Wish


class SQLAlchemyWishlistRepository(SQLAlchemyBaseRepository):
    def __init__(self, sqlalchemy_client):
        super().__init__(sqlalchemy_client, WishModel, Wish)
