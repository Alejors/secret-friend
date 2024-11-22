import re

from flask import url_for, redirect, flash, render_template, Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.usecases import ManageWishlistUsecase, ManageEventsUsecase
from src.templates.forms import WishlistForm


def create_frontend_wishlist_controller(wishlists_usecase: ManageWishlistUsecase, events_usecase: ManageEventsUsecase):
  blueprint = Blueprint("frontend_wishlist", __name__, url_prefix="/s1")
  
  @blueprint.route("/wishlist", methods=["GET", "POST"])
  @jwt_required()
  def wishlist_view():
    user_id = int(get_jwt_identity())
    events = events_usecase.get_events_by_user_id(user_id)
    event_selected = int(request.args.get("event_id")) if request.args.get("event_id") else None
    wishlist_form = WishlistForm()
    if request.method == "POST":
      form_data = request.form
      request_files = request.files
      wishes_dict = {}
      regex = r'items-(\d+)-(\w+)'
      for key, value in form_data.items():
        if match := re.search(regex, key):
          index = int(match.group(1))
          field = match.group(2)
          
          if index not in wishes_dict:
            wishes_dict[index] = {}
          
          wishes_dict[index][field] = value
      for key, value in request_files.items():
        if match := re.search(regex, key):
          index = int(match.group(1))
          field = match.group(2)
          
          if index not in wishes_dict:
            wishes_dict[index] = {}
          
          wishes_dict[index][field] = value

      wishes = [value for _, value in wishes_dict.items() if value]

      wishlist_data = {
        "event_id": event_selected,
        "wishes": wishes
      }
      
      wishlist, error = wishlists_usecase.create_or_update_wishes(user_id, wishlist_data)
      if error:
        flash(f"Ocurrió un error: {error}", "error")
        return redirect(url_for("home.home_view"))
      else:
        flash(f"Lista Actualizada", "success")
      return redirect(url_for("frontend_wishlist.wishlist_view", event_id=event_selected))
    #TODO: armar flujo POST, evaluar agrega un filefield al form para recibir un archivo para cargar a cloudinary.
    if event_selected:
      wishlist = wishlists_usecase.get_wishlist_by_user_and_event(user_id, event_selected)
      title = next(event.name for event in events if event.id == event_selected)
    else:
      wishlist = title = None
    if wishlist:
      for i, form_item in enumerate(wishlist_form.items):
        if i < len(wishlist):
          form_item.element.data = wishlist[i].element
          form_item.url.data = wishlist[i].url
          
    return render_template("wishlist.html", events=events, wishlist=wishlist, wishlist_form=wishlist_form, wishlist_title=title, event_selected=event_selected)
  
  return blueprint