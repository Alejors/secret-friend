import re

from flask import url_for, redirect, flash, render_template, Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.usecases import ManageWishlistUsecase, ManageEventsUsecase
from src.templates.forms import WishlistForm, ItemForm

def create_wishlist_controller(
    wishlists_usecase: ManageWishlistUsecase, 
    events_usecase: ManageEventsUsecase
):
    blueprint = Blueprint("wishlist", __name__)

    @blueprint.route("/wishlist", methods=["GET", "POST"])
    @jwt_required()
    def wishlist_view():
        user_id = int(get_jwt_identity())
        events = events_usecase.get_events_by_user_id(user_id)
        event_selected = (
            int(request.args.get("event_id")) if request.args.get("event_id") else None
        )
        wishlist_form = WishlistForm()
        if request.method == "POST":
            form_data = request.form
            wishes_dict = {}
            regex = r"items-(\d+)-(\w+)"
            for key, value in form_data.items():
                if match := re.search(regex, key):
                    index = int(match.group(1))
                    field = match.group(2)

                    if index not in wishes_dict:
                        wishes_dict[index] = {}
                    if field == "price":
                        try:
                            value = int(value)
                        except ValueError:
                            value = None
                    wishes_dict[index][field] = value

            wishes = [value for _, value in wishes_dict.items() if value]

            wishlist, error = wishlists_usecase.create(user_id, wishes)
            if error:
                flash(f"An Error Occurred: {error}", "error")
                return redirect(url_for("home.home_view"))
            else:
                flash(f"List Updated", "success")
            return redirect(url_for("wishlist.wishlist_view", event_id=event_selected))
        wishlist = wishlists_usecase.get_wishlist_by_user(user_id)

        return render_template(
            "wishlist.html",
            events=events,
            wishlist=wishlist,
            wishlist_form=wishlist_form,
        )

    @blueprint.route("/edit_item", methods=["GET", "POST"])
    @jwt_required()
    def edit_item():
        user_id = int(get_jwt_identity())
        item_id = request.args.get("item_id")
        if not item_id:
            flash("Item ID is required", "error")
            return redirect(url_for("home.home_view"))
        wish = wishlists_usecase.get_wish_by_user_and_id(user_id, item_id)
        if not wish:
            flash("Item not found", "error")
            return redirect(url_for("wishlist.wishlist_view"))
        if request.method == "POST":
            data = request.form
            wish_data = {
                "element": data["element"],
                "price": int(data["price"]) if data["price"] != "" else None,
                "url": data["url"],
            }
            _, error = wishlists_usecase.update(wish.id, wish_data)
            if error:
                flash(f"An Error Occurred: {error}", "error")
            else:
                flash(f"Item Updated", "success")
            return redirect(url_for("wishlist.wishlist_view"))
        item_form = ItemForm()
        item_form.element.data = wish.element
        item_form.price.data = wish.price
        item_form.url.data = wish.url
        return render_template("edit_item.html", wish=wish, item_form=item_form)

    @blueprint.route("/delete-item", methods=["POST"])
    @jwt_required()
    def delete_item():
        user_id = int(get_jwt_identity())
        item_id = request.args.get("item_id")
        if not item_id:
            flash("Item ID is required", "error")
            return redirect(url_for("home.home_view"))
        wish = wishlists_usecase.get_wish_by_user_and_id(user_id, item_id)
        if not wish:
            flash("Item not found", "error")
            return redirect(url_for("wishlist.wishlist_view"))
        _, error = wishlists_usecase.delete(wish.id)
        if error:
            flash(f"An Error Occurred: {error}", "error")
        else:
            flash(f"Item Deleted", "success")
        return redirect(url_for("wishlist.wishlist_view"))

    return blueprint
