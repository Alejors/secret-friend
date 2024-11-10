from sqlalchemy import Column, Integer, String, ForeignKey

from src.entities import Wish


def map_wishlist(sqlalchemy_client):
  
  sqlalchemy_client.map_entity_to_table(
    Wish,
    "wishlist",
    [
      Column("id", Integer, primary_key=True),
      Column("user_id", ForeignKey("users.id"), nullable=False),
      Column("event_id", ForeignKey("events.id"), nullable=False),
      Column("element", String(50), nullable=False),
      Column("url", String(250), nullable=True),
    ],
  )