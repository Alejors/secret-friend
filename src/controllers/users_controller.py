from flask import Blueprint, request, jsonify
from src.frameworks.validation.validation import validate_schema_flask
from src.frameworks.validation.schemas import REGISTRY_VALIDATION_SCHEMA, LOGIN_VALIDATION_SCHEMA

from src.usecases import ManageUsersUsecase
from src.frameworks.http.http_response_codes import *
from src.frameworks.http.codes_constants import *


def create_users_controller(users_usecase: ManageUsersUsecase):
  blueprint = Blueprint("users", __name__, url_prefix="/v1")
  
  @blueprint.route("/user", methods=["GET"])
  def get_user_by_id(user_id):
    user_id = request.args.get("id")
    if not user_id:
      response = {
        "code": FAIL_CODE,
        "message": "User ID required"
      }
      response_code = BAD_REQUEST
    else:
      user = users_usecase.get_user_by_id(user_id)
      if user:
        response = {
          "code": SUCCESS_CODE,
          "message": "User Found",
          "data": user.serialize()
        }
        response_code = OK
      else:
        response = {
          "code": FAIL_CODE,
          "message": f"No User for ID {user_id}"
        }
        response_code = NOT_FOUND
    
    return jsonify(response), response_code
  
  @blueprint.route("/register", methods=["POST"])
  @validate_schema_flask(REGISTRY_VALIDATION_SCHEMA)
  def register_user():
    data = request.get_json()
    user, error = users_usecase.create_user(data)
    if user:
      user_data = user.serialize_user()
      response = {
          "code": SUCCESS_CODE,
          "message": "User Created",
          "data": user_data
        }
      response_code = CREATED
    else:
      response = {
          "code": FAIL_CODE,
          "message": f"Error Creating User: {error}"
        }
      response_code = BAD_REQUEST
      
    return jsonify(response), response_code
  
  @blueprint.route("/login", methods=["POST"])
  @validate_schema_flask(LOGIN_VALIDATION_SCHEMA)
  def user_login():
    data = request.get_json()
    user, token = users_usecase.user_log_in(data)
    if not user:
      response = {
        "code": FAIL_CODE,
        "message": "Credentials do not Match"
      }
      response_code = UNAUTHORIZED
    else:
      response = {
        "code": SUCCESS_CODE,
        "message": "Log in Succesful",
        "data": {
          "user": user.serialize_user(),
          "token": token
        }
      }
      response_code = OK
    return jsonify(response), response_code
  
  return blueprint
    