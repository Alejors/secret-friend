from flask import Blueprint, request

from src.usecases import ManageUsersUsecase
from src.frameworks.http.http_response_codes import *


def create_users_controller(users_usecase: ManageUsersUsecase):
  blueprint = Blueprint("users", __name__, url_prefix="/v1")
  
  @blueprint.route("/user", methods=["GET"])
  def get_user_by_id(user_id):
    user_id = request.args.get("id")
    if not user_id:
      response = {
        "code": "failed",
        "message": "User ID required"
      }
      response_code = BAD_REQUEST
    else:
      user = users_usecase.get_user_by_id(user_id)
      if user:
        response = {
          "code": "success",
          "message": "User Found",
          "data": user.serialize()
        }
        response_code = OK
      else:
        response = {
          "code": "failed",
          "message": f"No User for ID {user_id}"
        }
        response_code = NOT_FOUND
    
    return response, response_code
  
  return blueprint
    