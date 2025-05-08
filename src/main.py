from src.frameworks.db.seeds.commands import seed
from src.frameworks.http.flask import create_flask_app
from src.frameworks.db.sqlalchemy import SQLAlchemyClient
from src.frameworks.mail.sendgrid_client import SendgridClient

from src.repositories import (
    SQLAlchemyUsersRepository,
    SQLAlchemyEventsRepository,
    SQLAlchemyWishlistRepository,
    SQLAlchemyEventUsersRepository,
    SendGridEmailRepository,
)

from src.usecases import (
    ManageUsersUsecase,
    ManageEventsUsecase,
    ManageWishlistUsecase,
)

from src.controllers import (
    create_healthcheck,
    create_landing_controller,
    create_home_controller,
    create_event_controller,
    create_profile_controller,
    create_wishlist_controller,
)

# Clients
sqlalchemy_client = SQLAlchemyClient()
mailing_client = SendgridClient()

# Repositories
sqlalchemy_user_repository = SQLAlchemyUsersRepository(sqlalchemy_client)
sqlalchemy_event_repository = SQLAlchemyEventsRepository(sqlalchemy_client)
sqlalchemy_wishlist_repository = SQLAlchemyWishlistRepository(sqlalchemy_client)
sqlalchemy_event_user_repository = SQLAlchemyEventUsersRepository(sqlalchemy_client)
sendgrid_mailing_repository = SendGridEmailRepository(mailing_client)

# Usecases
users_usecase = ManageUsersUsecase(sqlalchemy_user_repository)
wishlist_usecase = ManageWishlistUsecase(
    sqlalchemy_wishlist_repository,
    sqlalchemy_event_repository,
    sqlalchemy_event_user_repository,
)
events_usecase = ManageEventsUsecase(
    sqlalchemy_event_repository,
    sqlalchemy_event_user_repository,
    users_usecase,
    wishlist_usecase,
    sendgrid_mailing_repository,
)

blueprints = [
    create_healthcheck(),
    create_landing_controller(users_usecase),
    create_home_controller(users_usecase, events_usecase),
    create_event_controller(events_usecase),
    create_profile_controller(users_usecase),
    create_wishlist_controller(wishlist_usecase, events_usecase),
]

commands = {"seed": seed(sqlalchemy_client)}

app = create_flask_app(blueprints, commands)
