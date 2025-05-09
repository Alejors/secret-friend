from flask import render_template, Blueprint, request, flash, redirect, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.usecases import ManageUsersUsecase, ManageEventsUsecase


def create_home_controller(
    users_usecase: ManageUsersUsecase, events_usecase: ManageEventsUsecase
):
    blueprint = Blueprint("home", __name__)

    @blueprint.route("/home")
    @jwt_required()
    def home_view():
        user_id = int(get_jwt_identity())
        user = users_usecase.get_user_by_id(user_id)
        events = events_usecase.get_events_by_user_id(user_id)
        event_selected = (
            int(request.args.get("event_id")) if request.args.get("event_id") else None
        )
        if len(events) > 0:
            if not event_selected:
                current_event = events[0]
                event_selected = current_event.id
            else:
                try:
                    current_event = next(
                        event for event in events if event.id == event_selected
                    )
                except StopIteration:
                    flash("Event not found", "error")
                    return redirect(url_for("home.home_view"))
            event_pick, wishlist, pick_error = events_usecase.get_pick_from_event(
                user_id, event_selected
            )
        else:
            event_pick = wishlist = None
            pick_error = "Create an Event to Begin!"
            current_event = None

        return render_template(
            "home.html",
            user=user,
            events=events,
            current_event=current_event,
            event_pick=event_pick,
            wishlist=wishlist,
            pick_error=pick_error,
        )

    return blueprint
