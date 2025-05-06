from typing import TypeVar
from abc import ABC, abstractmethod


T = TypeVar('T')
class IImageUploader(ABC):
  @abstractmethod
  def upload(self, data: dict) -> T|None:
    print("Method Not Implemented")
    pass
