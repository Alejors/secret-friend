from src.models import Event, User
from src.interfaces import IDataRepository
from src.repositories import SQLAlchemyEventUsersRepository


class ManageEventsUsecase:
  def __init__(
    self, 
    events_repository: IDataRepository, 
    event_user_repository: SQLAlchemyEventUsersRepository
  ):
    self._event_users_repository = event_user_repository
    self._events_repository = events_repository
    
  def _get_event(self, filters: dict) -> Event|None:
    return self._events_repository.get(filters=filters, first_only=True)
  
  def _get_events(self, filters: dict) -> Event|None:
    return self._events_repository.get(filters=filters)
  
  def get_event_by_id(self, id: int) -> Event|None:
    filters = {"id": id}
    return self._get_event(filters)
  
  def get_events_by_owner_id(self, owner_id: int) -> Event|None:
    filters = {"owner_id": owner_id}
    return self._get_events(filters=filters)
  
  def create_event(self, data: dict) -> Event|None:
    event = Event.from_dict(data)
    event_created = self._events_repository.insert(event)
    
    return self.get_event_by_id(event_created.id)

  def get_pick_from_event(self, user_id: int, event_id: int) -> tuple[User|None, str|None]:
    pick_user = self._event_users_repository.get_pick(user_id, event_id)
    if pick_user:
      return pick_user, None
    return None, "Usuario No Encontrado"