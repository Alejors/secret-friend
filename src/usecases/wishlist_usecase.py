from datetime import datetime

from src.entities import Wish, Event, User
from src.interfaces import IDataRepository, IWishlistRepository
from src.repositories import SQLAlchemyEventUsersRepository


class ManageWishlistUsecase:
    def __init__(
        self,
        wishlist_repository: IWishlistRepository,
        events_repository: IDataRepository,
        event_users_repository: SQLAlchemyEventUsersRepository,
    ):
        self._wishlist_repository = wishlist_repository
        self._events_repository = events_repository
        self._event_users_repository = event_users_repository

     
    def get_wishlist_by_user(self, user_id: int) -> list[Wish]:
        filter = {"user_id": user_id, "deleted_at": None}
        return self._wishlist_repository.get(filters=filter)

    def get_wish_by_user_and_id(
        self, user_id: int, element_id: int
    ) -> Wish:
        filter = {"user_id": user_id, "id": element_id}
        return self._wishlist_repository.get(filters=filter, first_only=True)

    def get_event_by_id(self, event_id: int) -> Event:
        filter = {"id": event_id}
        return self._events_repository.get(filters=filter, first_only=True)

    def get_who_picked(self, user_id: int, event_id: int) -> User:
        return self._event_users_repository.get_who_picked_id(user_id, event_id)

    def create(
        self, user_id: int, data: list[dict]
    ) -> tuple[list[Wish] | None, str | None]:
        try:
            wishes = []
            for element in data:
                if element["element"] is None or element["element"] == "":
                    continue
                element["user_id"] = user_id
                wish_inserted = self._wishlist_repository.insert(element)
                wishes.append(wish_inserted)
            return wishes, None
        except Exception as e:
            print(e)
            return None, str(e)
        
    def update(self, wish_id: int, data: dict) -> tuple[Wish | None, str | None]:
        try:
            wish = self._wishlist_repository.update(wish_id, data)
            return wish, None
        except Exception as e:
            print(e)
            return None, str(e)
        
    def delete(self, wish_id: int) -> tuple[None, str | None]:
        data = {"deleted_at": datetime.now()}
        try:
            self.update(wish_id, data)
            return None, None
        except Exception as e:
            print(e)
            return None, str(e)

    def get_wishlist_by_range(self, event: Event, user: User) -> tuple[list[Wish], str | None]:
        try:
            return self._wishlist_repository.get_wishlist_by_range(
                user_id=user.id,
                min_price=event.min_price,
                max_price=event.max_price,
            ), None
        except Exception as e:
            print(e)
            return [], str(e)
