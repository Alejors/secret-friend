from datetime import datetime
from sqlalchemy.exc import IntegrityError

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
  
  def get_by_owner_id_and_event_id(self, owner_id: int, event_id: int) -> Event|None:
    filters = {"owner_id": owner_id, "id": event_id}
    return self._get_event(filters=filters)
  
  def get_event_by_name_and_owner(self, owner_id: int, name: str) -> Event|None:
    filters = {"owner_id": owner_id, "name": name}
    return self._get_event(filters)
  
  def _insert_participant(self, data: dict, event: Event) -> User:
    user_exists = self._users_usecase.get_user_by_email(data["email"])

    if not user_exists:
      data["password"] = event.name
      user_exists, error = self._users_usecase.create_user(data)
      # Si hubo un error en la creación, no habrá un User en user_exists,
      # debemos detener aquí la ejecución para evitar errores al intentar 
      # insertar un elemento en event_user
      if error:
        return error
    try:  
      self._event_users_repository.insert_participant(user_exists.id, event.id)
    except IntegrityError as e:
      # si se intentó insertar nuevamente un participante que ya existía 
      # previamente en este concurso, habrá un error de integridad por duplicidad. 
      # En este caso, capturamos el error, verificamos que el código coincida con duplicidad
      # y procedemos a actualizar el registro, quitando el delete_at. 
      # Automáticamente se debería actualizar la fecha de actualización también.
      if e.orig.args[0] == 1062:
        renewal = {"deleted_at": None}
        self._event_users_repository.update_participation(user_exists.id, event.id, renewal)
      else:
        return str(e)
  
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
        error = self._insert_participant(participant, event_created)
        if error:
          errors.append(error)
      if len(errors) > 0:
        return None, f"Event Created with Errors: {", ".join(errors)}"
      return self.get_event_by_id(event_created.id), None
    except Exception as e:
      return None, str(e)

  def update_event(self, user_id: int, event_id: int, data: dict) -> tuple[Event|None, str|None]:
    errors = []
    event_exist = self.get_by_owner_id_and_event_id(user_id, event_id)
    
    if not event_exist:
      return None, "No Event Matches Owner and ID"
    if event_exist.drawn:
      return None, "Can't Update an Already Drawn Event"
    
    if new_participants := data.get("users"):
      current_participants = [participant.email for participant in event_exist.users]
      new_participants_emails = [participant["email"] for participant in new_participants]
      # Estos ya no están considerados y deberán ser eliminados
      participants_to_remove = list(filter(lambda participant: participant not in new_participants_emails, current_participants))
      if len(participants_to_remove) > 0:
        for participant in participants_to_remove:
          # pensando en la posibilidad de que se quiera remover un participante en un momento, 
          # pero luego volver a incorporarlo. Es mejor incluir un soft delete en la tabla.
          user_to_remove = self._users_usecase.get_user_by_email(participant)
          removal = {"deleted_at": datetime.now()}
          self._event_users_repository.update_participation(user_to_remove.id, event_exist.id, removal)
      
      # En este punto removemos los elementos que ya existen en el actual
      new_participants = [participant for participant in new_participants if participant["email"] not in current_participants]
      if len(new_participants) > 0:
        for new_participant in new_participants:
          error = self._insert_participant(new_participant, event_exist)
          if error:
            errors.append(error)
      del data["users"]
    self._events_repository.update(event_exist.id, data)
    
    if len(errors) > 0:
      return None, ", ".join(errors)
    return self.get_event_by_id(event_exist.id), None

  def get_pick_from_event(self, user_id: int, event_id: int) -> tuple[User|None, str|None]:
    pick_user = self._event_users_repository.get_pick(user_id, event_id)
    if pick_user:
      return pick_user, None
    return None, "Usuario No Encontrado"