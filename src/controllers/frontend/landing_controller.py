import os

from flask import url_for, redirect, flash, render_template, Blueprint, request, make_response
from flask_jwt_extended import get_csrf_token, set_access_cookies
from src.usecases import ManageUsersUsecase
from src.templates.forms import LoginForm, RegistryForm


def create_landing_controller(users_usecase: ManageUsersUsecase):
  blueprint = Blueprint("landing", __name__, url_prefix="/s1")
  
  @blueprint.route("/", methods=["GET", "POST"])
  def login_view():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
      data = request.form
      user, token = users_usecase.user_log_in(data)
      if not user:
        flash("Las Credenciales No Coinciden", "error")
        return redirect(url_for('landing.login_view'))
      else:
        response = make_response(redirect(url_for('home.home_view')))
        set_access_cookies(response, token)
        return response
    return render_template("login.html", form=form)
  
  @blueprint.route("/register", methods=["GET", "POST"])
  def register_view():
    form = RegistryForm()
    if request.method == "POST" and form.validate():
      data = request.form
      user, error = users_usecase.create_user(data)
      if user:
        flash("Registro Exitoso!", "success")
        return redirect(url_for('landing.login_view'))
      else:
        flash(f"Se Produjo un Error: {error}", "error")
        return redirect(url_for('landing.register_view'))
    return render_template("register.html", form=form)

  @blueprint.route("/logout")
  def user_logout():
    response = redirect(url_for('landing.login_view'))
    response.delete_cookie('access_token_cookie')
    
    return response

  return blueprint