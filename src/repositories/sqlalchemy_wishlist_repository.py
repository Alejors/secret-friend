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
            special_filters.append(WishModel.price.between(min_price, max_price))
        elif min_price:
            special_filters.append(WishModel.price >= min_price)
        elif max_price:
            special_filters.append(WishModel.price <= max_price)
        return self.get(filters=filter, special_filters=special_filters)
