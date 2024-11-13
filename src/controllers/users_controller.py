import os

from flask import url_for, redirect, flash, make_response, Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required, get_csrf_token

from src.frameworks.validation.validation import validate_schema_flask
from src.frameworks.validation.schemas import REGISTRY_VALIDATION_SCHEMA, LOGIN_VALIDATION_SCHEMA

from src.usecases import ManageUsersUsecase
from src.frameworks.http.codes_constants import *
from src.frameworks.http.http_response_codes import *


def create_users_controller(users_usecase: ManageUsersUsecase):
  blueprint = Blueprint("users", __name__, url_prefix="/v1")
  
  @blueprint.route("/user", methods=["GET"])
  def get_user_by_id():
    user_id = int(request.args.get("id"))
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
          "data": user.serialize_user()
        }
        response_code = OK
      else:
        response = {
          "code": FAIL_CODE,
          "message": f"No User for ID {user_id}"
        }
        response_code = NOT_FOUND
    
    return jsonify(response), response_code
  
  @blueprint.route("/user", methods=["PUT", "PATCH"])
  @jwt_required()
  def update_user():
    user_id = int(get_jwt_identity())
    if not user_id:
      response = {
        "code": FAIL_CODE,
        "message": "User ID required"
      }
      response_code = NOT_FOUND
    else:
      data = request.get_json()
      user_updated, error = users_usecase.update_user(user_id, data)
      if user_updated:
        response = {
          "code": SUCCESS_CODE,
          "message": "User Updated",
          "data": user_updated.serialize_user()
        }
        response_code = OK
      else:
        response = {
          "code": FAIL_CODE,
          "message": f"Error Ocurred while Updateing {error}"
        }
        response_code = BAD_REQUEST
        
    return jsonify(response), response_code
  
  @blueprint.route("/register", methods=["POST"])
  @validate_schema_flask(REGISTRY_VALIDATION_SCHEMA)
  def register_user():
    data = request.get_json() if request.headers.get('Content-Type') == "application/json" else request.form
    user, error = users_usecase.create_user(data)
    if user:
      flash("Registro Exitoso!", "success")
      return redirect(url_for('frontend.login_view'))
    else:
      flash(f"Se Produjo un Error: {error}", "error")
      return redirect(url_for('frontend.register_view'))
  
  @blueprint.route("/login", methods=["POST"])
  @validate_schema_flask(LOGIN_VALIDATION_SCHEMA)
  def user_login():
    data = request.get_json() if request.headers.get('Content-Type') == "application/json" else request.form
    user, token = users_usecase.user_log_in(data)
    if not user:
      flash("Las Credenciales No Coinciden", "error")
      return redirect(url_for('frontend.login_view'))
    else:
      response = make_response(redirect(url_for('frontend.home_view')))
      response.set_cookie('access_token_cookie', token, httponly=True, secure=os.environ.get("ENVIRONMENT")!="local")
      response.set_cookie('csrf_access_token', get_csrf_token(token), httponly=True, secure=os.environ.get("ENVIRONMENT")!="local")
      return response
  
  @blueprint.route("/logout")
  def user_logout():
    response = redirect(url_for('frontend.login_view'))
    response.delete_cookie('access_token_cookie')
    
    return response
  
  return blueprint
