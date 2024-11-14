from flask import url_for, redirect, flash, render_template, Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.usecases import ManageEventsUsecase


def create_frontevent_controller(events_usecase: ManageEventsUsecase):
  blueprint = Blueprint("frontevent", __name__, url_prefix="/s1")
  
  @blueprint.route("/manage-events", methods=["GET", "POST"])
  @jwt_required()
  def events_view():
    
    user_id = int(get_jwt_identity())
    
    events = events_usecase.get_events_by_owner_id(user_id)
    
    event_selected = int(request.args.get("event_id")) if request.args.get("event_id") else None
    
    if len(events) > 0:
      if not event_selected:
        current_event = events[0]
        event_selected = current_event.id
      else:
        current_event = next(event for event in events if event.id == event_selected)
    else:
      event_selected = current_event = None
      
    return render_template(
      "manage_events.html", 
      events=events, 
      event_selected=event_selected, 
      current_event=current_event,
    )
  
  @blueprint.route("/draw-event", methods=["GET"])
  @jwt_required()
  def draw_event():
    user_id = int(get_jwt_identity())
    event_id = int(request.args.get("event_id"))
    
    if not event_id or not user_id:
      drawn = None
      error = "Error: Información Necesaria No Llegó"
    else:
      drawn, error = events_usecase.draw_event(user_id, event_id)
      
    if drawn:
      flash("Sorteo Realizado!", "success")
      return redirect(url_for("frontend.home_view"))
    else:
      flash(error, "error")
      return redirect(url_for("frontend.events_view"))
  
  return blueprint