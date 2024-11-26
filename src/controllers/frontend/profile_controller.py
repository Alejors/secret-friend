from flask import url_for, redirect, flash, render_template, Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.usecases import ManageUsersUsecase
from src.templates.forms import ProfileForm
from src.utils import check_password, hash_password

 
def create_profile_controller(users_usecase: ManageUsersUsecase):
  blueprint = Blueprint("profile", __name__, url_prefix="/s1")
  
  @blueprint.route("/profile", methods=["GET", "POST"])
  @jwt_required()
  def profile_view():
    user_id = int(get_jwt_identity())
    form = ProfileForm()
    current_user = users_usecase.get_user_by_id(user_id)
    if request.method == "POST" and form.validate():
      data = request.form
      if not check_password(current_user.password, data["current_password"]):
        flash("La contraseña actual no es correcta!", "error")
      else:        
        user_update_data = {
          "name": data["name"],
          "password": hash_password(data["new_password"])
        }
        _, error = users_usecase.update_user(user_id, user_update_data)
        if error:
          flash(f"Ocurrió un error: {error}", "error")
        flash("Usuario actualizado!", "success")
      return redirect(url_for("profile.profile_view"))
    if not current_user:
      flash("Hay un problema con el usuario")
      return redirect(url_for("landing.user_logout"))
    form.name.data = current_user.name
    form.email.data = current_user.email
    
    return render_template("profile.html", form=form)
  
  return blueprint
