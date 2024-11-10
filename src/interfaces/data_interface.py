from typing import TypeVar
from abc import ABC, abstractmethod


T = TypeVar('T')
class IDataRepository(ABC):
  @abstractmethod
  def get(self, filters: dict) -> T|None:
    print("Method Not Implemented")
    pass
  
  @abstractmethod
  def insert(self, data: T) -> T|None:
    print("Method Not Implemented")
    pass
  
  @abstractmethod
  def update(self, original_class: T, data: dict) -> T|None:
    print("Method Not Implemented")
    pass
