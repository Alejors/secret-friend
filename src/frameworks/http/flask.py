import os
from flask import Flask
from flask_jwt_extended import JWTManager


def create_flask_app(blueprints, commands: dict):
  template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "templates"))
  static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "static"))
  app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
  
  jwt = JWTManager(app)
  
  app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY")
  app.config['JWT_TOKEN_LOCATION'] = ['cookies', 'headers']
  app.config['DEBUG'] = True # DEV
  app.config['TEMPLATES_AUTO_RELOAD'] = True # DEV
  app.secret_key = os.environ.get("FLASK_SECRET_KEY")

  app.json.sort_keys = False

  for blueprint in blueprints:
    app.register_blueprint(blueprint)

  for name, command in commands.items():
    app.cli.command(name)(command)

  return app
