DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT_MILLISECONDS = "%Y-%m-%d %H:%M:%S.%f"


def format_date(datetime, add_milliseconds=False):
  """
  Retorna una representación en String de una fecha/hora dada.
  """
  if datetime:
    if add_milliseconds:
      return datetime.strftime(DATE_FORMAT_MILLISECONDS)
    return datetime.strftime(DATE_FORMAT)

  return None


def read_sql(path, filename) -> dict:
  """
  Lee archivo SQL desde un archivo.
  """
  with open(f"src/{path}/{filename}.sql", "r") as query_file:
    return query_file.read()
