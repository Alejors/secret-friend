LOGIN_VALIDATION_SCHEMA = {
  "email": {
    "required": True,
    "type": "string",
    "regex": r"^([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)(,\s*[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)*$"
  },
  "password": {
    "required": True,
    "type": "string"
  }
}