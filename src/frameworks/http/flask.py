import os
from flask import Flask
from flask_jwt_extended import JWTManager


def create_flask_app(blueprints, commands: dict):
  app = Flask(__name__)
  
  jwt = JWTManager(app)
  
  app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY")

  app.json.sort_keys = False

  for blueprint in blueprints:
    app.register_blueprint(blueprint)

  for name, command in commands.items():
    app.cli.command(name)(command)

  return app
