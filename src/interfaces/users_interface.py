from abc import ABC, abstractmethod

from src.entities import User


class IDataRepository(ABC):
  @abstractmethod
  def get(self, filters: dict) -> User:
    print("Method Not Implemented")
    pass
  
  @abstractmethod
  def insert(self, user: User) -> User:
    print("Method Not Implemented")
    pass
  
  @abstractmethod
  def update(self, user: User, data: dict) -> User:
    print("Method Not Implemented")
    pass
