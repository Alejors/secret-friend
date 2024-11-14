from flask import url_for, redirect, flash, render_template, Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.usecases import ManageUsersUsecase
from src.templates.forms import ProfileForm

 
def create_profile_controller(users_usecase: ManageUsersUsecase):
  blueprint = Blueprint("profile", __name__, url_prefix="/s1")
  
  @blueprint.route("/profile", methods=["GET", "POST"])
  @jwt_required()
  def profile_view():
    user_id = int(get_jwt_identity())
    form = ProfileForm()
    if request.method == "POST" and form.validate():
      data = request.form
      print(data)
      return
    current_user = users_usecase.get_user_by_id(user_id)
    if not current_user:
      flash("Hay un problema con el usuario")
      return redirect(url_for("landing.user_logout"))
    form.name.data = current_user.name
    form.email.data = current_user.email
    
    return render_template("profile.html", form=form)
  
  return blueprint
