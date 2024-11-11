from src.models import User
from src.interfaces import IDataRepository

from src.utils import hash_password, check_password, create_token


class ManageUsersUsecase:
  def __init__(self, users_repository: IDataRepository):
    self._user_repository = users_repository
  
  def _get_user(self, filters: dict) -> User|None:
    return self._user_repository.get(filters=filters, first_only=True)
  
  def get_user_by_id(self, id: int) -> User|None:
    filters = {"id": id}
    return self._get_user(filters)
  
  def get_user_by_email(self, email: str) -> tuple[User|None, str|None]:
    filters = {"email": email}
    return self._get_user(filters)
  
  def create_user(self, data: dict) -> User:
    user_exists = self.get_user_by_email(data["email"])
    if user_exists:
      return None, "Email Already in Use"
    
    # Hasheamos el password entregado
    data["password"] = hash_password(data["password"])
    
    # Creamos un User en base al dict del request
    user = User.from_dict(data)
    # Insertamos la entidad y almacenamos en una variable.
    user_created = self._user_repository.insert(user)
    
    return self.get_user_by_id(user_created.id), None
  
  def update_user(self, user_id: int, data: dict) -> User:
    user_exists = self.get_user_by_id(user_id)
    if not user_exists:
      return None, "User Not Found"
    
    return self._user_repository.update(user_id, data), None
  
  def user_log_in(self, data: dict) -> tuple[str|None, str|None]:
    user_email = data["email"]
    input_password = data["password"]
    
    user = self.get_user_by_email(user_email)
    
    # No deberíamos transparentar 
    # si el error está en el email 
    # o el password por razones de seguridad
    if not user or not check_password(user.password, input_password):
      return None, None
    
    return user, create_token(user.id)
