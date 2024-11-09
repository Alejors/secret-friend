from sqlalchemy import Column, Integer, String

from src.entities import User


def map_user(sqlalchemy_client):
  sqlalchemy_client.map_entity_to_table(
    User,
    "users",
    [
      Column("id", Integer, primary_key=True),
      Column("name", String, nullable=False),
      Column("email", String, nullable=False),
      Column("password", String, nullable=False),
    ],
  )
