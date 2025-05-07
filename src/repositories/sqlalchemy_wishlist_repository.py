from sqlalchemy import or_

from .base_repository import SQLAlchemyBaseRepository
from src.models import WishModel
from src.entities import Wish


class SQLAlchemyWishlistRepository(SQLAlchemyBaseRepository):
    def __init__(self, sqlalchemy_client):
        super().__init__(sqlalchemy_client, WishModel, Wish)
        
    def get_wishlist_by_range(self, user_id: int, min_price: int|None, max_price: int|None) -> list[Wish]:
        filter = {"user_id": user_id, "deleted_at": None}
        special_filters = []
        if min_price and max_price:
            special_filters.append(or_(WishModel.price.between(min_price, max_price), WishModel.price == None, WishModel.price == 0))
        elif min_price:
            special_filters.append(or_(WishModel.price >= min_price, WishModel.price == None, WishModel.price == 0))
        elif max_price:
            special_filters.append(or_(WishModel.price <= max_price, WishModel.price == None, WishModel.price == 0))
        return self.get(filters=filter, special_filters=special_filters)
