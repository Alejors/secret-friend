from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.frameworks.validation.validation import validate_schema_flask
from src.frameworks.validation.schemas import EVENT_CREATION_SCHEMA
 
from src.usecases import ManageEventsUsecase

from src.frameworks.http.http_response_codes import *
from src.frameworks.http.codes_constants import *


def create_events_controller(events_usecase: ManageEventsUsecase):
  blueprint = Blueprint("events", __name__, url_prefix="/v1")
  
  @blueprint.route("/event", methods=["GET"])
  def get_event():
    event_id = int(request.args.get("id"))
    event = events_usecase.get_event_by_id(event_id)
    if event:
      event_users = event.users
      event_owner = event.owner
      
      event_data = event.serialize()
  
      event_data["owner"] = event_owner.serialize_user()
      del event_data["owner_id"]
      
      event_data["users"] = [user.serialize_user() for user in event_users]
      response = {
        "code": SUCCESS_CODE,
        "message": "Event Obtained",
        "data": event_data
      }
      status_code = OK
    else:
      response = {
        "code": FAIL_CODE,
        "message": "Event Not Found"
      }
      status_code = NOT_FOUND
    return jsonify(response), status_code
  
  @blueprint.route("/event", methods=["POST"])
  @validate_schema_flask(EVENT_CREATION_SCHEMA)
  @jwt_required()
  def create_event():
    owner_id = int(get_jwt_identity())
    data = request.get_json()
    data["owner_id"] = owner_id
    event, error = events_usecase.create_event(data)
    if event:
      event_users = event.users
      event_owner = event.owner
      
      event_data = event.serialize()
      
      event_data["owner"] = event_owner.serialize_user()
      del event_data["owner_id"]
      
      event_data["users"] = [user.serialize_user() for user in event_users]
      
      response = {
        "code": SUCCESS_CODE,
        "message": "Event Created",
        "data": event_data
      }
      status_code = CREATED
    else:
      response = {
        "code": FAIL_CODE,
        "message": f"An Error Ocurred: {error}"
      }
      status_code = INTERNAL_SERVER_ERROR
    
    return jsonify(response), status_code
  
  @blueprint.route("/event", methods=["POST"])
  @jwt_required()
  def update_participants():
    event_id = request.args.get("event_id")
    if not event_id:
      response = {
        "code": FAIL_CODE,
        "message": "Event ID Needed"
      }
      status_code = BAD_REQUEST
    else:
      pass
  
  @blueprint.route("/get-pick", methods=["GET"])
  @jwt_required()
  def get_pick():
    user_id = int(get_jwt_identity())
    event_id = request.args.get("event_id")
    if not event_id:
      response = {
        "code": FAIL_CODE,
        "message": "Event ID Needed"
      }
      status_code = BAD_REQUEST
    else:
      try:
        pick_user, error = events_usecase.get_pick_from_event(user_id, event_id)
        if pick_user:
          user_data = pick_user.serialize_user()
          response = {
            "code": SUCCESS_CODE,
            "message": "Pick User Fetched",
            "data": user_data
          }
          status_code = OK
        else:
          response = {
            "code": FAIL_CODE,
            "message": error
          }
          status_code = NOT_FOUND
      except Exception as e:
        response = {
          "code": FAIL_CODE,
          "message": f"An Error Occurred: {str(e)}"
        }
        status_code = INTERNAL_SERVER_ERROR
        
      return jsonify(response), status_code
  
  
  return blueprint