from flask import request
from functools import wraps
from cerberus import Validator

from src.frameworks.http.codes_constants import *
from src.frameworks.validation.errors import ERROR_MESSAGES
from src.frameworks.validation.translations import ERROR_TRANSLATIONS


def validate_schema(
  data: dict,
  schema: dict,
  allow_undefined_fields: bool = True,
  use_public_api_response: bool = False,
) -> dict:
  """
  Recibe un diccionario con los datos por validar, y retorna un objeto con
  los posibles errores con el formato correcto, de lo contrario retorna None.
  """
  errors = None

  allowEmpty = True
  for _, value in schema.items():
    required = value.get("required", False)
    if required:
      allowEmpty = False
      break

  # Utilizar Cerberus para validar el esquema recibido.
  if not data and allowEmpty:
    return None
  elif data:
    validator = Validator(allow_unknown=allow_undefined_fields)
    is_valid = validator.validate(data, schema)
    if is_valid:
      return None
    else:
      errors = _format_errors(schema, validator.errors)
  else:
    errors = [{
      "code": "empty_body",
      "message": "Body must not be empty"
    }]

  results = {
    "code": FAIL_CODE,
    "message": "There was an error in the input data",
    "errors": errors,
  }

  if use_public_api_response:
    results["status"] = FAIL_CODE
    del results["code"]

  return results
  
def _format_errors(schema: dict, errors: dict, parent_field: bool = None) -> dict:
  formatted_errors = []

  for field_name, error_list in errors.items():
    if parent_field:
      field_name = f"{parent_field}.{field_name}"

    for value in error_list:
      if isinstance(value, str):
        code, message = _get_translation(schema, field_name, value)
        formatted_error = {
          "field": field_name,
          "code": code,
          "message": message,
        }
        formatted_errors.append(formatted_error)
      elif isinstance(value, dict):
        formatted_errors += _format_errors(
          schema,
          value,
          parent_field=field_name
        )

  return formatted_errors

def _get_translation(schema: dict, dot_key: str, text: str) -> tuple[str, str]:
  """
  Busca el texto en la lista de traducciones y retorna su código y mensaje
  traducido. De no encontrarlo, retorna la traducción por defecto.
  """
  code = ERROR_TRANSLATIONS[0][1]

  for row in ERROR_TRANSLATIONS:
    value = row[0]
    translation = row[1]
    if value in text or text in value:
      code = translation

  # Buscar el mensaje según la traducción.
  message = ERROR_MESSAGES.get(code)

  if code == "max_length":
    amount = text.replace("max length is ", "")
    message += amount

  elif code == "incorrect_type":
    field_type = text.replace("must be of ", "").replace(" type", "")
    prefix = "a"
    if field_type in ["integer"]:
      prefix = "an"
    message += f"{prefix} {field_type}"

  elif code == "invalid_value":
    allowed_values = get_value_from_schema(schema, dot_key).get("allowed")
    allowed_values = ", ".join(allowed_values)
    message += allowed_values

  return code, message

def get_value_from_schema(schema: dict, dot_key: str) -> dict:
  """
  Busca el valor desde el esquema de Cerberus usando la llave recibida.
  La llave puede venir en notación de puntos, ej: "user.values".
  """
  value = None
  parent_dict = schema
  keys = dot_key.split(".")

  for key in keys:
    value = parent_dict.get(key)
    if isinstance(value, dict):
      parent_dict = value.get("schema", {})
    else:
      parent_dict = {}

  return value

def validate_schema_flask(schema: dict, allow_undefined_fields: bool = True):
  def decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
      json_data = request.get_json()
      errors = validate_schema(json_data, schema, allow_undefined_fields)

      if not errors:
          return f(*args, **kwargs)

      status_code = 400
      return errors, status_code

    return wrapper

  return decorator