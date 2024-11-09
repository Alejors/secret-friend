import os
import logging

from sqlalchemy import create_engine, Table, Column, TIMESTAMP
from sqlalchemy.engine import url
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import close_all_sessions, sessionmaker, registry
from sqlalchemy.sql import func
from sqlalchemy_utils import database_exists, create_database


Base = declarative_base()
class SQLAlchemyClient:
  def __init__(self, test: bool = False):
    driver = os.environ["SQL_ALCHEMY_DRIVER"]
    username = os.environ["SQL_ALCHEMY_USERNAME"]
    password = os.environ["SQL_ALCHEMY_PASSWORD"]
    database = os.environ["SQL_ALCHEMY_DATABASE"]

    self.test = test
    if test:
      database += "_test"

    host = os.environ.get("SQL_ALCHEMY_HOST", None)
    socket = os.environ.get("SQL_ALCHEMY_SOCKET", None)
    socket_query = None

    if host:
      socket = None
    elif socket:
      socket_query = {"unix_socket": "/cloudsql/%s" % socket}

    db_url = url.URL.create(
      drivername=driver,
      username=username,
      password=password,
      database=database,
      host=host,
      query=socket_query,
    )

    self.engine = create_engine(db_url, echo=False)

    if test and not database_exists(self.engine.url):
      create_database(self.engine.url)

    self.session_factory = sessionmaker(bind=self.engine, expire_on_commit=False)
    self.mapper_registry = registry()

  def map_entity_to_table(
    self,
    entity_class,
    table_name: str,
    columns: list,
    include_date_columns: bool = True,
    properties: dict = None,
  ):
    """
    Mapea una entidad a una tabla, útil al usar el repositorio con estilo imperativo.
    """
    if include_date_columns:
      columns += [
        Column("created_at", TIMESTAMP, server_default=func.now(), nullable=False),
        Column("updated_at", TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp(), nullable=False),
        Column("deleted_at", TIMESTAMP),
      ]

    table = Table(
      table_name,
      self.mapper_registry.metadata,
      *columns,
    )

    self.mapper_registry.map_imperatively(entity_class, table, properties=properties)

    return table

  def create_tables(self):
    """
    Crea las tablas que aún no están creadas en la base de datos.
    """
    Base.metadata.create_all(self.engine)
    self.mapper_registry.metadata.create_all(self.engine)

  def drop_table(self, table: Table):
    """
    Borra una tabla específica. Sólo usado durante tests.
    """
    if self.test:
      close_all_sessions()
      Base.metadata.drop_all(self.engine, tables=[table])
      self.mapper_registry.metadata.drop_all(self.engine, tables=[table])

  def drop_all_tables(self):
    """
    Borra todas las tablas. Sólo usado durante tests.
    """
    if self.test:
      close_all_sessions()
      Base.metadata.drop_all(self.engine)
      self.mapper_registry.metadata.drop_all(self.engine)

  def _dispose_mapper(self):
    """
    Limpia el mapper registry en caso de usar el modo imperativo.
    Sólo usado durante tests.
    """
    if self.test:
        self.mapper_registry.dispose()

  def load_script(self, file_path: str, throw_exception: bool = True):
    """
    Recibe la ruta completa de un script .sql y lo carga a través del
    cliente de SQLAlchemy.

    El cliente de SQLAlchemy no permite cargar scripts completos, como
    tampoco permite ejecutar queries de más de una línea, así que es
    necesario leer el archivo completo, quitar los saltos de línea y
    comentarios, y luego ejecutar las queries una a una.

    Si el parámetro "throw_exception" es True, entonces se arroja excepción
    si es que una de las queries falla, interrumpiendo el resto del
    proceso. Si es False, entonces simplemente loguea una advertencia pero
    continúa con el resto de las queries.
    """
    def remove_comment(query: str) -> str:
      idx = query.find('--')
      if idx >= 0:
          query = query[:idx]
      return query

    lines = []
    with open(file_path, 'r') as f:
      for line in f.readlines():
        line = line.strip()
        line = remove_comment(line)
        if line:
          lines.append(line)

    whole_line = ' '.join(lines)
    queries = whole_line.split(';')
    queries = [query.strip() for query in queries]

    with self.engine.connect() as connection:
      for query in queries:
        if query:
          try:
            connection.execute(query)
          except Exception as e:
            if throw_exception:
              raise e
            else:
              print(e)
