from src.entities import User, Event, Wish
from abc import ABC, abstractmethod


class IMailerRepository(ABC):
    @abstractmethod
    def send_new_user_email(self, user: User, password: str) -> None:
        print("Method Not Implemented")
        pass

    @abstractmethod
    def send_event_drawn_mail(self, current_participant: User, picked_user: User, wishlist: list[Wish], event: Event) -> None:
        print("Method Not Implemented")
        pass
