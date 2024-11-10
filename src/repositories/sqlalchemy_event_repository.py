from .base_repository import SQLAlchemyBaseRepository
from src.entities import Event
from src.models import map_event


class SQLAlchemyEventsRepository(SQLAlchemyBaseRepository):
  def __init__(self, sqlalchemy_client):
    super().__init__(sqlalchemy_client, Event)
    map_event(sqlalchemy_client)
