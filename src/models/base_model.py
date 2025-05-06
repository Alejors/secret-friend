from sqlalchemy import Column, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.inspection import inspect

from datetime import datetime

from src.utils import format_date

from src.frameworks.db.sqlalchemy.sqlalchemy_client import Base


class SQLAlchemyBaseModel(Base):
    """
    Modelo base que incluye las fechas 'created_at', 'updated_at' y
    'deleted_at'. Las primeras dos fechas se asignan automáticamente siempre
    que se guarda o edita el modelo.
    """

    __abstract__ = True

    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.current_timestamp(),
        nullable=False,
    )
    deleted_at = Column(TIMESTAMP)

    def to_dict(self):
        model_columns = inspect(self.__class__).columns
        return {column.name: getattr(self, column.name) for column in model_columns}

    def serialize(self, include_deleted=False):
        _dict = self.to_dict()
        if not include_deleted:
            _dict.pop("deleted_at", None)
        _dict = self._check_datetimes(_dict)

        return _dict

    def _check_datetimes(self, _dict: dict) -> dict:
        for key in _dict.keys():
            if isinstance(_dict[key], dict):
                _dict[key] = self._check_datetimes(_dict[key])
            if isinstance(_dict[key], datetime):
                _dict[key] = format_date(_dict[key])

        return _dict

    @classmethod
    def from_dict(cls, data: dict):
        """
        Abstract Method, must be implemented in concrete classes.
        """
        raise NotImplementedError(f"from_dict Not Implemented in {cls.__name__}")
