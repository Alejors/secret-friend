from src.interfaces import IUser
from src.entities import User


class ManageUsersUsecase:
  def __init__(self, users_repository: IUser):
    self._user_repository = users_repository
  
  def _get_user(self, filters: dict) -> User|None:
    return self._user_repository.get(filters)
  
  def get_user_by_id(self, id: int) -> User|None:
    filters = {"id": id}
    return self._get_user(filters)
  
  def get_user_by_email(self, email: str) -> User|None:
    filters = {"email": email}
    return self._get_user(filters)
  
  def create_user(self, data: dict) -> User:
    pass
