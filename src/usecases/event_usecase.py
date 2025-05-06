import copy
import random
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from src.entities import Event, User, Wish
from src.interfaces import IDataRepository, IEventUserRepository, IMailerRepository
from src.usecases import ManageUsersUsecase
from src.usecases.wishlist_usecase import ManageWishlistUsecase

from src.utils import get_random_password

class ManageEventsUsecase:
    def __init__(
        self, 
        events_repository: IDataRepository, 
        event_user_repository: IEventUserRepository,
        users_usecase: ManageUsersUsecase,
        wishlist_usecase: ManageWishlistUsecase,
        mailing_repository: IMailerRepository,
    ):
        self._event_users_repository = event_user_repository
        self._events_repository = events_repository
        self._users_usecase = users_usecase
        self._wishlist_usecase = wishlist_usecase
        self._mailing_repository = mailing_repository
    
    def _get_event(self, filters: dict) -> Event|None:
        return self._events_repository.get(filters=filters, first_only=True)
  
    def _get_events(self, filters: dict) -> list[Event|None]:
        return self._events_repository.get(filters=filters)
  
    def get_event_by_id(self, id: int) -> Event|None:
        filters = {"id": id}
        return self._get_event(filters)
    
    def get_events_by_owner_id(self, owner_id: int) -> list[Event]:
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
            initial_password = get_random_password()
            data["password"] = initial_password
            user_exists, error = self._users_usecase.create_user(data)
            # Si hubo un error en la creación, no habrá un User en user_exists,
            # debemos detener aquí la ejecución para evitar errores al intentar 
            # insertar un elemento en event_user
            if error:
                return error
            else:
                self._mailing_repository.send_new_user_email(user_exists, initial_password)
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
        errors = []
        try:
            event_exists = self.get_event_by_name_and_owner(data['owner_id'], data['name'])
            if event_exists:
                return None, "Event Name Already Exists"
            event_created = self._events_repository.insert(data)
            participants = data["users"]
            for participant in participants:
                error = self._insert_participant(participant, event_created)
                if error:
                    errors.append(error)
            if len(errors) > 0:
                return None, f"Event Created with Errors: {", ".join(errors)}"
            return self.get_event_by_id(event_created.id), None
        except Exception as e:
            print("ERROR: ", e)
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
                    # En este punto removemos los elementos que ya existen en el actual
                    user_to_remove = self._users_usecase.get_user_by_email(participant)
                    removal = {"deleted_at": datetime.now()}
                    self._event_users_repository.update_participation(user_to_remove.id, event_exist.id, removal)
        
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

    def draw_event(self, user_id: int, event_id: int) -> tuple[bool, str|None]:
        event = self.get_by_owner_id_and_event_id(user_id, event_id)
        if not event:
            return False, "Este evento no le pertenece a este usuario."
        if event.drawn:
            return False, "El evento ya fue sorteado!"
        
        # listamos todos los participantes del concurso
        event_participants_ids = [participant.id for participant in event.users]
        
        # realizamos una copia que iremos modificando
        not_picked_participants = copy.copy(event_participants_ids)
        
        # iteramos todos los participantes desde la lista que no se modifica
        try:
            for participant in event_participants_ids:
                # copiamos la lista de los no seleccionados
                possible_picks = list(filter(lambda possible_pick: possible_pick != participant, not_picked_participants))
                
                # obtenemos un número al azar correspondiente al indice de la lista
                pick_idx = random.randrange(0, len(possible_picks))
                # recuperamos el id que corresponda
                pick = possible_picks[pick_idx]
                
                # actualizamos la tabla event_user
                pick_selection = {"pick_id": pick}
                self._event_users_repository.update_participation(participant, event.id, pick_selection)
                # quitamos este elemento de la lista de los no escogidos aún
                not_picked_participants.remove(pick)
            self._events_repository.update(event.id, {"drawn": True})
        # Si falla cualquier update, tenemos que eliminar cualquier update que alcanzó a hacerse
        except Exception as e:
            remove_pick = {"pick_id": None}
            for participant in event_participants_ids:
                self._event_users_repository.update_participation(participant, event.id, remove_pick)
            self._events_repository.update(event.id, {"drawn": False})
            print("ERROR: ", e)
            return False, f"Se retrocede. Ocurrió un error: {str(e)}"
        try:
            self._send_event_drawn_mail(event_participants_ids, event)
        except Exception as e:
            print("ERROR: ", e)
            return False, f"Se realizó el sorteo, pero hubo un error al enviar los correos: {str(e)}"
        return True, None

    def get_pick_from_event(self, user_id: int, event_id: int) -> tuple[User|None, list[Wish]|None, str|None]:
        event = self.get_event_by_id(event_id)
        if not event:
            return None, None, "Evento no encontrado"
        if user_id not in [participant.id for participant in event.users]:
            return None, None, "Este usuario no está en este evento"
        if not event.drawn:
            return None, None, "El evento no se ha sorteado aún"
        pick_user = self._event_users_repository.get_pick(user_id, event_id)
        if pick_user:
            wishlist = self._wishlist_usecase.get_wishlist_by_user(pick_user.id)
            return pick_user, wishlist, None
        return None, None, "Usuario no encontrado"
    
    def get_events_by_user_id(self, user_id: int) -> list[Event]:
        return self._event_users_repository.get_events_by_participant(user_id)

    def _send_event_drawn_mail(self, user_ids: list, event: Event):
        for participant in user_ids:
            current_participant = next(user for user in event.users if user.id == participant)
            picked_user, wishlist, error = self.get_pick_from_event(current_participant.id, event.id)
            if not error:
                self._mailing_repository.send_event_drawn_mail(current_participant, picked_user, wishlist, event)
            else:
                print(error)
