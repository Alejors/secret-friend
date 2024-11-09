from flask import Flask


def create_flask_app(blueprints, commands: dict):
  app = Flask(__name__)

  app.json.sort_keys = False

  for blueprint in blueprints:
    app.register_blueprint(blueprint)

  for name, command in commands.items():
    app.cli.command(name)(command)

  return app
