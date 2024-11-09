from sqlalchemy import Column, TIMESTAMP
from sqlalchemy.sql import func

from src.frameworks.db.sqlalchemy import Base


class SQLAlchemyBaseModel(Base):
    """
    Modelo base que incluye las fechas 'created_at', 'updated_at' y
    'deleted_at'. Las primeras dos fechas se asignan automáticamente siempre
    que se guarda o edita el modelo.
    """
    __abstract__ = True

    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp(), nullable=False)
    deleted_at = Column(TIMESTAMP)