from src.entities import Event, User
from abc import ABC, abstractmethod


class IEventUserRepository(ABC):
    @abstractmethod
    def get_events_by_participant(self, user_id: int) -> list[Event]:
        print("Method Not Implemented")
        pass
  
    @abstractmethod
    def get_pick(self, user_id: int, event_id: int) -> User:
        print("Method Not Implemented")
        pass
  
    @abstractmethod
    def get_who_picked_id(self, user_id: int, event_id: int) -> User:
        print("Method Not Implemented")
        pass
    
    @abstractmethod
    def insert_participant(self, user_id: int, event_id: int) -> None:
        print("Method Not Implemented")
        pass

    @abstractmethod
    def update_participation(self, user_id: int, event_id: int, values: dict) -> None:
        print("Method Not Implemented")
        pass
