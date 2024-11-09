from src.entities import User


class IUser:
  def __init__(self, database_client):
    self.client = database_client
  
  def get(self, filters: dict) -> User:
    print("Method Not Implemented")
    pass
  
  def insert(self, user: User) -> User:
    print("Method Not Implemented")
    pass
  
  def update(self, user: User, data: dict) -> User:
    print("Method Not Implemented")
    pass
