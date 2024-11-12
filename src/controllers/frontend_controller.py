from datetime import datetime
from flask import render_template, Blueprint


def create_frontend_controller():
  blueprint = Blueprint("frontend", __name__, url_prefix="/s1")
  
  @blueprint.route("/")
  def main_view():
    today = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return render_template("main.html", date=today)
  
  return blueprint
  