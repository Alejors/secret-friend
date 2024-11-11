from sqlalchemy import select, and_, update

from src.models import User, Event


class SQLAlchemyEventUsersRepository:
  def __init__(self, sqlalchemy_client):
    self.session_factory = sqlalchemy_client.session_factory
    
  def get_pick(self, user_id: int, event_id: int) -> User|None:
    with self.session_factory() as session:
      query = (
        select(User)
        .join(Event.event_users, Event.event_users.c.pick_id == User.id)
        .where(
          and_(
            Event.event_users.c.event_id == event_id,
            Event.event_users.c.user_id == user_id
          )
        )
      )
      result = session.execute(query).first()
      return result[0] if result else None
    
  def insert_participant(self, user_id: int, event_id: int):
    with self.session_factory() as session:
      event_user = {
        "user_id": user_id,
        "event_id": event_id
      }
      
      session.execute(Event.event_users.insert().values(event_user))
      session.commit()
      
  def update_participation(self, user_id: int, event_id: int, values: dict):
    with self.session_factory() as session:      
      query = (
        update(Event.event_users)
        .where(and_(
          Event.event_users.c.user_id == user_id,
          Event.event_users.c.event_id == event_id
          )
        )
        .values(**values)
      )
      
      session.execute(query)
      session.commit()
