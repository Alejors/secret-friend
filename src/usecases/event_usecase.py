from src.models import Event, User
from src.interfaces import IDataRepository
from src.usecases import ManageUsersUsecase
from src.repositories import SQLAlchemyEventUsersRepository


class ManageEventsUsecase:
  def __init__(
    self, 
    events_repository: IDataRepository, 
    event_user_repository: SQLAlchemyEventUsersRepository,
    users_usecase: ManageUsersUsecase,
  ):
    self._event_users_repository = event_user_repository
    self._events_repository = events_repository
    self._users_usecase = users_usecase
    
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
  
  def get_event_by_name_and_owner(self, owner_id: int, name: str) -> Event|None:
    filters = {"owner_id": owner_id, "name": name}
    return self._get_event(filters)
  
  def create_event(self, data: dict) -> tuple[Event|None, str|None]:
    event = Event.from_dict(data)
    errors = []
    try:
      event_exists = self.get_event_by_name_and_owner(event.owner_id, event.name)
      if event_exists:
        return None, "Event Name Already Exists"
      event_created = self._events_repository.insert(event)
      participants = data["users"]
      for participant in participants:
        user_exists = self._users_usecase.get_user_by_email(participant["email"])
        
        if not user_exists:
          participant["password"] = event_created.name
          user_exists, error = self._users_usecase.create_user(participant)
          if error:
            errors.append(error)
        
        self._event_users_repository.insert_participant(user_exists.id, event_created.id)

      if len(errors) > 0:
        return None, f"Event Created with Errors: {", ".join(errors)}"
      
      return self.get_event_by_id(event_created.id), None
    except Exception as e:
      return None, str(e)

  def get_pick_from_event(self, user_id: int, event_id: int) -> tuple[User|None, str|None]:
    pick_user = self._event_users_repository.get_pick(user_id, event_id)
    if pick_user:
      return pick_user, None
    return None, "Usuario No Encontrado"