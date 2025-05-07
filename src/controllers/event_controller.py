import re
from flask import url_for, redirect, flash, render_template, Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.usecases import ManageEventsUsecase
from src.templates.forms import EventForm


def create_event_controller(events_usecase: ManageEventsUsecase):
  blueprint = Blueprint("event", __name__)
  
  @blueprint.route("/manage-events", methods=["GET", "POST"])
  @jwt_required()
  def events_view():
    user_id = int(get_jwt_identity())
    form = EventForm()
    event_selected = int(request.args.get("event_id")) if request.args.get("event_id") else None
    if request.method == "POST" and form.validate():
      data = request.form
      users_dict = {}
      regex = r'users\[(\d+)\]\[(\w+)\]'
      for key, value in data.items():
        if match := re.search(regex, key):
          index = int(match.group(1))
          field = match.group(2)
          
          if index not in users_dict:
            users_dict[index] = {}
          
          users_dict[index][field] = value
      users = [value for _, value in users_dict.items()]
      
      event_data = {
        "name": data.get("name"),
        "min_price": int(data.get("min_price")) if data.get("min_price") else None,
        "max_price": int(data.get("max_price")) if data.get("max_price") else None,
        "users": users
      }
      if len(users) < 3:
        error = "At Least 3 Participants Required!"
      else:
        if event_selected:
          _, error = events_usecase.update_event(user_id, event_selected, event_data)
          flash("Event Updated", "success")
        else:
          event_data["owner_id"] = user_id
          _, error = events_usecase.create_event(event_data)
          flash("Event Created", "success")
      if error:
        flash(error, "error")
        return redirect(url_for("event.events_view", event_id=event_selected))
      return redirect(url_for("home.home_view"))
    
    events = events_usecase.get_events_by_owner_id(user_id)
    
    if event_selected:
      current_event = next(event for event in events if event.id == event_selected)
    else:
      current_event = None
    
    if current_event:
      form.name.data = current_event.name
      form.min_price.data = current_event.min_price
      form.max_price.data = current_event.max_price
    
    return render_template(
      "manage_events.html",
      event_selected=event_selected,
      current_event=current_event,
      events=events,
      form=form,
    )

  @blueprint.route("/draw-event", methods=["GET"])
  @jwt_required()
  def draw_event():
    user_id = int(get_jwt_identity())
    event_id = int(request.args.get("event_id"))
    
    if not event_id or not user_id:
      drawn = None
      error = "Error: Not enough data to draw the event"
    else:
      drawn, error = events_usecase.draw_event(user_id, event_id)
      
    if drawn:
      flash("Event Drawn!", "success")
      return redirect(url_for("home.home_view"))
    else:
      flash(error, "error")
      return redirect(url_for("event.events_view"))
  
  return blueprint