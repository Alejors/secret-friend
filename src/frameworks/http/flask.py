import os
from flask import Flask
from jinja2 import Environment
from flask_jwt_extended import JWTManager

from src.frameworks.jinja.custom_filters import custom_methods


def create_flask_app(blueprints, commands: dict):
  template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "templates"))
  static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "static"))
  app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

  environment = os.environ.get("ENVIRONMENT")
  app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY")
  app.config['JWT_TOKEN_LOCATION'] = ['cookies', 'headers', 'query_string']
  if environment == "local":
    app.config['DEBUG'] = True # DEV
    app.config['TEMPLATES_AUTO_RELOAD'] = True # DEV
  else:
    app.config['JWT_COOKIE_DOMAIN'] = os.environ.get("DOMAIN")
    app.config['JWT_COOKIE_SAMESITE'] = 'Lax'
  app.config['JWT_COOKIE_CSRF_PROTECT'] = False
  app.config['WTF_CSRF_ENABLED'] = True
  app.config["JWT_COOKIE_SECURE"] = False
  app.secret_key = os.environ.get("JWT_SECRET_KEY")

  jinja_env = Environment()
  for filter, method in custom_methods.items():
    jinja_env.filters[filter] = method

  app.jinja_env.filters.update(jinja_env.filters)

  jwt = JWTManager(app)

  for blueprint in blueprints:
    app.register_blueprint(blueprint)

  for name, command in commands.items():
    app.cli.command(name)(command)

  return app
