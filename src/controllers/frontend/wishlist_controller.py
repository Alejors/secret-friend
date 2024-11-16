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
    #TODO: armar flujo POST, evaluar agrega un filefield al form para recibir un archivo para cargar a cloudinary.
    if event_selected:
      wishlist = wishlists_usecase.get_wishlist_by_user_and_event(user_id, event_selected)
    else:
      wishlist = None
      
    wishlist_form = WishlistForm()
    if wishlist:
      for i, form_item in enumerate(wishlist_form.items):
        if i < len(wishlist):
          form_item.element.data = wishlist[i].element
          form_item.url.data = wishlist[i].url
          
    return render_template("wishlist.html", events=events, wishlist=wishlist, wishlist_form=wishlist_form)
  
  return blueprint