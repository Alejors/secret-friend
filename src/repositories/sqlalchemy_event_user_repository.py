from sqlalchemy import select, and_, update

from src.models import UserModel, EventModel


class SQLAlchemyEventUsersRepository:
    def __init__(self, sqlalchemy_client):
        self.session_factory = sqlalchemy_client.session_factory

    def get_events_by_participant(self, user_id: int) -> list[EventModel]:
        with self.session_factory() as session:
            query = (
                select(EventModel)
                .join(
                    EventModel.event_users,
                    EventModel.event_users.c.event_id == EventModel.id,
                )
                .where(
                    and_(
                        EventModel.event_users.c.user_id == user_id,
                        EventModel.event_users.c.deleted_at == None,
                    )
                )
            )
            result = list(session.execute(query).scalars().unique())
            return result

    def get_pick(self, user_id: int, event_id: int) -> UserModel | None:
        with self.session_factory() as session:
            query = (
                select(UserModel)
                .join(
                    EventModel.event_users,
                    EventModel.event_users.c.pick_id == UserModel.id,
                )
                .where(
                    and_(
                        EventModel.event_users.c.event_id == event_id,
                        EventModel.event_users.c.user_id == user_id,
                    )
                )
            )
            result = session.execute(query).first()
            return result[0] if result else None

    def get_who_picked_id(self, user_id: int, event_id: int) -> UserModel | None:
        with self.session_factory() as session:
            query = (
                select(UserModel)
                .join(
                    EventModel.event_users,
                    EventModel.event_users.c.user_id == UserModel.id,
                )
                .where(
                    and_(
                        EventModel.event_users.c.event_id == event_id,
                        EventModel.event_users.c.pick_id == user_id,
                    )
                )
            )
            result = session.execute(query).first()
            return result[0] if result else None

    def insert_participant(self, user_id: int, event_id: int):
        with self.session_factory() as session:
            event_user = {"user_id": user_id, "event_id": event_id}

            session.execute(EventModel.event_users.insert().values(event_user))
            session.commit()

    def update_participation(self, user_id: int, event_id: int, values: dict):
        with self.session_factory() as session:
            query = (
                update(EventModel.event_users)
                .where(
                    and_(
                        EventModel.event_users.c.user_id == user_id,
                        EventModel.event_users.c.event_id == event_id,
                    )
                )
                .values(**values)
            )

            session.execute(query)
            session.commit()
