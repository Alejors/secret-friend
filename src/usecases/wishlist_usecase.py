from datetime import datetime

from src.models import Wish
from src.interfaces import IDataRepository
from src.frameworks.bucket.bucket import BucketClient


class ManageWishlistUsecase:
  def __init__(
    self, 
    wishlist_repository: IDataRepository,
    bucket_client: BucketClient,
  ):
    self._wishlist_repository = wishlist_repository
    self._bucket_client = bucket_client
  
  def get_wishlist_by_user_and_event(self, user_id: int, event_id: int) -> list[Wish]:
    filter = {"user_id": user_id, "event_id": event_id, "deleted_at": None}
    return self._wishlist_repository.get(filters=filter)
  
  def get_wish_by_user_element_and_event(self, user_id: int, event_id: int, element: str) -> Wish:
    filter = {"user_id": user_id, "element": element, "event_id": event_id}
    return self._wishlist_repository.get(filters=filter, first_only=True)
  
  def create_or_update_wishes(self, user_id: int, data: dict) -> tuple[list[Wish]|None, str|None]:
    event_id = data["event_id"]
    wishes = data["wishes"]
    try:
      current_wishlist = self.get_wishlist_by_user_and_event(user_id, event_id)
      wish_names = [wish.element for wish in current_wishlist if wish]
      for element in wishes:
        element["user_id"] = user_id
        element["event_id"] = event_id
        if element["image"]:
          self._bucket_client.upload_file(element['image'], user_id)
        wish = Wish.from_dict(element)
        if wish.element not in wish_names:
          removed_wish = self.get_wish_by_user_element_and_event(user_id, event_id, wish.element)
          if removed_wish and removed_wish.deleted_at is not None:
            renewal = {"deleted_at": None}
            self._wishlist_repository.update(removed_wish.id, renewal)
          else:
            self._wishlist_repository.insert(wish)
      new_wishes_names = list(map(lambda wish: wish["element"], wishes))
      wishes_to_remove = list(filter(lambda wish: wish.element not in new_wishes_names, current_wishlist))
      for wish_to_remove in wishes_to_remove:
        removal = {"deleted_at": datetime.now()}
        self._wishlist_repository.update(wish_to_remove.id, removal)
      
      return self.get_wishlist_by_user_and_event(user_id, event_id), None
    except Exception as e:
      return None, str(e)