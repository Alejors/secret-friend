from flask import Blueprint, jsonify

from src.frameworks.http.http_response_codes import *
from src.frameworks.http.codes_constants import *


def create_healthcheck():
  blueprint = Blueprint("health-check", __name__, url_prefix="/v1")
  
  @blueprint.route("/", methods=["GET"])
  def health_check():
    response = {
      "code": SUCCESS_CODE,
      "message": "I'm Alive!"
    }
    response_code = OK
    
    return jsonify(response), response_code
  
  return blueprint
    