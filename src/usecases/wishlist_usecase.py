from src.models import Wish
from src.interfaces import IDataRepository


class ManageWishlistUsecase:
  def __init__(self, wishlist_repository: IDataRepository):
    self._wishlist_repository = wishlist_repository
  
  def get_wishlist_by_user_and_event(self, user_id: int, event_id: int) -> list[Wish]:
    filter = {"user_id": user_id, "event_id": event_id}
    return self._wishlist_repository.get(filters=filter)
  
  def create_wishes(self, user_id: int, data: dict) -> tuple[list[Wish]|None, str|None]:
    event_id = data["event_id"]
    wishes = data["wishes"]
    try:
      for element in wishes:
        element["user_id"] = user_id
        element["event_id"] = event_id
        wish = Wish.from_dict(element)
        self._wishlist_repository.insert(wish)
      
      return self.get_wishlist_by_user_and_event(user_id, event_id), None
    except Exception as e:
      return None, str(e)