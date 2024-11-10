from sqlalchemy import Column, Integer, String

from src.entities import User


def map_user(sqlalchemy_client):
  sqlalchemy_client.map_entity_to_table(
    User,
    "users",
    [
      Column("id", Integer, primary_key=True),
      Column("name", String(50), nullable=False),
      Column("email", String(100), nullable=False, unique=True),
      Column("password", String(250), nullable=False),
    ],
  )
