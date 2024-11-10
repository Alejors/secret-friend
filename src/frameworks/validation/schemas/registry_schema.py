REGISTRY_VALIDATION_SCHEMA = {
  "name": {
    "required": True,
    "type": "string",
    "minlength": 3
  },
  "email": {
    "required": True,
    "type": "string",
    "regex": r"^([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)(,\s*[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)*$"
  },
  "password": {
    "required": True,
    "type": "string",
    "regex": r"^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,12}$"
  }
}