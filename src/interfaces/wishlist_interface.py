from typing import TypeVar
from abc import ABC, abstractmethod

from .data_interface import IDataRepository


T = TypeVar('T')
class IWishlistRepository(IDataRepository, ABC):
  @abstractmethod
  def get_wishlist_by_range(self, user_id:int, min_price:int|None, max_price:int|None) -> T|None:
    print("Method Not Implemented")
    pass

