from .base_repository import SQLAlchemyBaseRepository
from src.models import WishModel
from src.entities import Wish


class SQLAlchemyWishlistRepository(SQLAlchemyBaseRepository):
    def __init__(self, sqlalchemy_client):
        super().__init__(sqlalchemy_client, WishModel, Wish)
        
    def get_wishlist_by_range(self, user_id: int, min_price: int|None, max_price: int|None) -> list[Wish]:
        filter = {"user_id": user_id, "deleted_at": None}
        if min_price and max_price:
            filter["price"] = {"$gte": min_price, "$lte": max_price}
        elif min_price:
            filter["price"] = {"$gte": min_price}
        elif max_price:
            filter["price"] = {"$lte": max_price}
        return self.get(filters=filter)
