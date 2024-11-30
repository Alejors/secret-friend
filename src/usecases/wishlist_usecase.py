from datetime import datetime

from src.models import Wish, Event, User
from src.interfaces import IDataRepository
from src.frameworks.mail.client import MailingClient
from src.frameworks.bucket.client import BucketClient
from src.repositories import SQLAlchemyEventUsersRepository


class ManageWishlistUsecase:
  def __init__(
    self, 
    wishlist_repository: IDataRepository,
    events_repository: IDataRepository,
    event_users_repository: SQLAlchemyEventUsersRepository,
    bucket_client: BucketClient,
    mailing_client: MailingClient,
  ):
    self._wishlist_repository = wishlist_repository
    self._events_repository = events_repository
    self._event_users_repository = event_users_repository
    self._bucket_client = bucket_client
    self._mailing_client = mailing_client
  
  def get_wishlist_by_user_and_event(self, user_id: int, event_id: int) -> list[Wish]:
    filter = {"user_id": user_id, "event_id": event_id, "deleted_at": None}
    return self._wishlist_repository.get(filters=filter)
  
  def get_wish_by_user_element_and_event(self, user_id: int, event_id: int, element: str) -> Wish:
    filter = {"user_id": user_id, "element": element, "event_id": event_id}
    return self._wishlist_repository.get(filters=filter, first_only=True)
  
  def get_event_by_id(self, event_id: int) -> Event:
    filter = {"id": event_id}
    return self._events_repository.get(filters=filter, first_only=True)
  
  def get_who_picked(self, user_id: int, event_id: int) -> User:
    return self._event_users_repository.get_who_picked_id(user_id, event_id)
  
  def create_or_update_wishes(self, user_id: int, data: dict) -> tuple[list[Wish]|None, str|None]:
    event_id = data["event_id"]
    current_event = self.get_event_by_id(event_id)
    if not current_event:
      return None, "Event Not Found"
    wishes = data["wishes"]
    try:
      current_wishlist = self.get_wishlist_by_user_and_event(user_id, current_event.id)
      wish_names = [wish.element for wish in current_wishlist if wish]
      for element in wishes:
        if element["element"] is None or element["element"] == "":
          continue
        element["user_id"] = user_id
        element["event_id"] = current_event.id
        image_file = element.pop("image", None)
        if image_file:
          url = self._bucket_client.upload_file(image_file, user_id, str(current_event.id))
          if url:
            element["url"] = url
          else:
            raise FileExistsError("Unable to Upload File")
        wish = Wish.from_dict(element)
        wish_exists = self.get_wish_by_user_element_and_event(user_id, current_event.id, wish.element)
        if wish.element not in wish_names:
          if wish_exists and wish_exists.deleted_at is not None:
            renewal = element.update({"deleted_at": None})
            self._wishlist_repository.update(wish_exists.id, renewal)
          else:
            self._wishlist_repository.insert(wish)
        else:
          self._wishlist_repository.update(wish_exists.id, element)
      new_wishes_names = list(map(lambda wish: wish["element"], wishes))
      wishes_to_remove = list(filter(lambda wish: wish.element not in new_wishes_names, current_wishlist))
      for wish_to_remove in wishes_to_remove:
        removal = {"deleted_at": datetime.now()}
        self._wishlist_repository.update(wish_to_remove.id, removal)
      
      updated_wishlist = self.get_wishlist_by_user_and_event(user_id, current_event.id)
      if current_event.drawn:
        # MANDAR MAIL DE QUE SE ACTUALIZO LISTA DE DESEOS
        user_who_picked = self.get_who_picked(user_id, current_event.id)
        wishlist_elements = ''.join([f'<li><a href={item.url}>{item.element}</a></li>' for item in updated_wishlist if item.element is not None])
        body = f"""
        <html>
          <body>
            <h1>Hola, {user_who_picked.name}!</h1>
            <p>Tu amigo secreto actualizó su <b>lista de deseos</b>!</p>
            <p>Aquí tienes ideas para regalarle:</p> 
            <ul>{wishlist_elements}</ul>
            <br/>
            <p>saludos!</p>
          </body>
        </html>"""
        self._mailing_client.login()
        self._mailing_client.send_mail(user_who_picked.email, "Lista de Deseos Actualizada!", body)
        self._mailing_client.logout()
      return updated_wishlist, None
    except Exception as e:
      return None, str(e)