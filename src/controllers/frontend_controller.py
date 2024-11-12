from flask import render_template, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.usecases import ManageUsersUsecase


def create_frontend_controller(users_usecase: ManageUsersUsecase):
  blueprint = Blueprint("frontend", __name__, url_prefix="/s1")
  
  @blueprint.route("/")
  def main_view():
    return render_template("main.html")

  @blueprint.route("/home")
  @jwt_required()
  def home_view():
    user_id = int(get_jwt_identity())
    user = users_usecase.get_user_by_id(user_id)
    
    return render_template("home.html", user=user.name)
  
  return blueprint
