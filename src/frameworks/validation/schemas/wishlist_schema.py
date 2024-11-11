WISHLIST_CREATION_SCHEMA = {
  "event_id": {
    "required": True,
    "type": "integer"
  },
  "wishes": {
    "required": True,
    "type": "list",
    "minlength": 1,
    "schema": {
      "type": "dict",
      "schema": {
        "element": {
          "type": "string",
          "required": True,
          "nullable": False
        },
        "url": {
          "type": "string",
          "required": False,
          "nullable": True
        }
      }
    }
  }
}