from .base_repository import SQLAlchemyBaseRepository
from src.models import Event, User


class SQLAlchemyEventsRepository(SQLAlchemyBaseRepository):
  def __init__(self, sqlalchemy_client):
    super().__init__(sqlalchemy_client, Event)
