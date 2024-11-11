EVENT_CREATION_SCHEMA = {
  "name": {
    "required": True,
    "type": "string"
  },
  "min_price": {
    "required": False,
    "type": "integer",
    "min": 0
  },
  "max_price": {
    "required": False,
    "type": "integer",
    "min": 0
  },
  "users": {
    "required": True,
    "type": "list",
    "minlength": 1,
    "schema":{
      "type": "dict",
      "schema": {
        "email": {
          "type": "string",
          "required": True,
          "regex": r"^([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)(,\s*[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)*$"
        },
        "name": {
          "type": "string",
          "required": True
        }
      }
    }
  }
}