from src.frameworks.db.sqlalchemy import SQLAlchemyClient


def seed(
  sqlalchemy_client: SQLAlchemyClient
):
  def command():
    """
    Carga los scripts con datos iniciales para las bases de datos usadas
    por esta API.
    """
    path = "src/frameworks/db/seeds/sql"
    
    sqlalchemy_client.load_script(f"{path}/tables-dll.sql", throw_exception=False)
    sqlalchemy_client.load_script(f"{path}/init-data.sql", throw_exception=False)

  return command