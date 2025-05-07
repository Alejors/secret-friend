from flask import url_for, redirect, flash, render_template, Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.usecases import ManageUsersUsecase
from src.templates.forms import ProfileForm
from src.utils import check_password, hash_password


def create_profile_controller(users_usecase: ManageUsersUsecase):
    blueprint = Blueprint("profile", __name__)

    @blueprint.route("/profile", methods=["GET", "POST"])
    @jwt_required()
    def profile_view():
        user_id = int(get_jwt_identity())
        form = ProfileForm()
        current_user = users_usecase.get_user_by_id(user_id)
        if request.method == "POST":
            if not form.validate():
                flash(f"Form Validation Failed: {form.errors}", "error")
                return redirect(url_for("profile.profile_view"))
            data = request.form
            if not check_password(current_user.password, data["current_password"]):
                flash("Incorrect Current Password!", "error")
            else:
                user_update_data = {
                    "name": data["name"],
                }
                if data["new_password"] and data["new_password"] != "":
                    user_update_data["password"] = data["new_password"]
                _, error = users_usecase.update_user(user_id, user_update_data)
                
                if error:
                    flash(f"An Error Occurred: {error}", "error")
                else:
                    flash("User Updated!", "success")
            return redirect(url_for("profile.profile_view"))
        if not current_user:
            flash("There's A Problem With Your Account", "error")
            return redirect(url_for("landing.user_logout"))
        form.name.data = current_user.name
        form.email.data = current_user.email

        return render_template("profile.html", form=form)

    return blueprint
