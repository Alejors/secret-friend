from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.frameworks.validation.validation import validate_schema_flask
from src.frameworks.validation.schemas import WISHLIST_CREATION_SCHEMA

from src.frameworks.http.codes_constants import *
from src.frameworks.http.http_response_codes import *

from src.usecases import ManageWishlistUsecase


def create_wishlist_controller(wishlist_usecase: ManageWishlistUsecase):
  
  blueprint = Blueprint("wishlist", __name__, url_prefix="/v1")
  
  @blueprint.route("/wishlist", methods=["POST"])
  @validate_schema_flask(WISHLIST_CREATION_SCHEMA)
  @jwt_required()
  def create_wishlist():
    data = request.get_json()
    user_id = int(get_jwt_identity())
    wishlist, errors = wishlist_usecase.create_or_update_wishes(user_id, data)
    if wishlist:
      response = {
        "code": SUCCESS_CODE,
        "message": "Wishlist Created",
        "data": [wish.serialize() for wish in wishlist]
      }
      status_code = CREATED
    else:
      response = {
        "code": FAIL_CODE,
        "message": f"An Error Occurred: {errors}."
      }
      status_code = BAD_REQUEST
    return jsonify(response), status_code
  
  return blueprint
    