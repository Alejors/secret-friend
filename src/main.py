import os

from src.frameworks.db.seeds.commands import seed
from src.frameworks.http.flask import create_flask_app
from src.frameworks.db.sqlalchemy import SQLAlchemyClient

# Users
from src.repositories import SQLAlchemyUsersRepository
from src.usecases import ManageUsersUsecase
from src.controllers import create_users_controller


# Repositories
sqlalchemy_client = SQLAlchemyClient()
sqlalchemy_user_repository = SQLAlchemyUsersRepository(sqlalchemy_client)

# Usecases
users_usecase = ManageUsersUsecase(sqlalchemy_user_repository)

blueprints = [
    create_users_controller(users_usecase),
]

commands = {
    "seed": seed(sqlalchemy_client)
}

app = create_flask_app(blueprints, commands)
