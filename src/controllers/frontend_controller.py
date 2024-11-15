from flask import render_template, Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.usecases import ManageUsersUsecase, ManageEventsUsecase


def create_frontend_controller(users_usecase: ManageUsersUsecase, events_usecase: ManageEventsUsecase):
  blueprint = Blueprint("frontend", __name__, url_prefix="/s1")
  
  @blueprint.route("/")
  def login_view():
    return render_template("login.html")

  @blueprint.route("/home")
  @jwt_required()
  def home_view():
    user_id = int(get_jwt_identity())
    user = users_usecase.get_user_by_id(user_id)
    events = events_usecase.get_events_by_user_id(user_id)
    event_selected = int(request.args.get("event_id")) if request.args.get("event_id") else None
    if len(events) > 0:
      if not event_selected:
        current_event = events[0]
        event_selected = current_event.id
      else:
        current_event = next(event for event in events if event.id == event_selected)
      event_pick, wishlist, pick_error = events_usecase.get_pick_from_event(user_id, event_selected)
    else:
      event_pick = wishlist = None
      pick_error = "Crea un Evento Para Comenzar!"
    return render_template("home.html", user=user, events=events, current_event=current_event, event_pick=event_pick, wishlist=wishlist, pick_error=pick_error)
  
  @blueprint.route("/register")
  def register_view():
    return render_template("register.html")
  
  @blueprint.route("/profile")
  def profile_view():
    return "OK"
  
  @blueprint.route("/wishlist")
  def wishlist_view():
    return "OK"
  
  @blueprint.route("/manage-events")
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
    return render_template("manage_events.html", events=events, event_selected=event_selected, current_event=current_event)
  
  return blueprint
