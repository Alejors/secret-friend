from flask import Blueprint, request, jsonify, redirect, url_for, flash
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
      event_data = event.serialize_event()
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
      event_data = event_data = event.serialize_event()
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
  
  @blueprint.route("/event", methods=["PUT", "PATCH"])
  @jwt_required()
  def update_event():
    user_id = int(get_jwt_identity())
    event_id = int(request.args.get("event_id"))
    if not event_id:
      response = {
        "code": FAIL_CODE,
        "message": "Event ID Needed"
      }
      status_code = BAD_REQUEST
    else:
      data = request.get_json()
      event, error = events_usecase.update_event(user_id, event_id, data)
      if event:
        event_data = event.serialize_event()
        response = {
          "code": SUCCESS_CODE,
          "message": "Event Updated",
          "data": event_data
        }
        status_code = OK
      else:
        response = {
          "code": FAIL_CODE,
          "message": error
        }
        status_code = BAD_REQUEST
    return jsonify(response), status_code
  
  @blueprint.route("/get-pick", methods=["GET"])
  @jwt_required()
  def get_pick():
    user_id = int(get_jwt_identity())
    event_id = int(request.args.get("event_id"))
    if not event_id:
      response = {
        "code": FAIL_CODE,
        "message": "Event ID Needed"
      }
      status_code = BAD_REQUEST
    else:
      try:
        pick_user, wishlist, error = events_usecase.get_pick_from_event(user_id, event_id)
        if pick_user:
          user_data = pick_user.serialize_user()
          user_data["wishlist"] = [wish.serialize() for wish in wishlist if wish]
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
  
  @blueprint.route("/draw-event", methods=["GET"])
  @jwt_required()
  def draw_event():
    user_id = int(get_jwt_identity())
    event_id = int(request.args.get("event_id"))
    if not event_id:
      response = {
        "code": FAIL_CODE,
        "message": "Event ID Needed"
      }
      status_code = BAD_REQUEST
    else:
      drawn, error = events_usecase.draw_event(user_id, event_id)
      if drawn:
        flash("Sorteo Realizado!", "success")
        return redirect(url_for("frontend.home_view"))
      else:
        flash(error, "error")
        return redirect(url_for("frontend.events_view"))
              
    return jsonify(response), status_code
  return blueprint