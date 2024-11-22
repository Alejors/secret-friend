from src.frameworks.db.seeds.commands import seed
from src.frameworks.http.flask import create_flask_app
from src.frameworks.db.sqlalchemy import SQLAlchemyClient
from src.frameworks.bucket.client import BucketClient
from src.frameworks.mail.client import MailingClient

from src.repositories import (
    SQLAlchemyUsersRepository,
    SQLAlchemyEventsRepository,
    SQLAlchemyWishlistRepository,
    SQLAlchemyEventUsersRepository,
)

from src.usecases import (
    ManageUsersUsecase,
    ManageEventsUsecase,
    ManageWishlistUsecase,
)

from src.controllers import (
    create_users_controller,
    create_healthcheck,
    create_events_controller,
    create_wishlist_controller,
    create_landing_controller,
    create_home_controller,
    create_frontevent_controller,
    create_profile_controller,
    create_frontend_wishlist_controller,
)


# Clients
sqlalchemy_client = SQLAlchemyClient()
bucket_client = BucketClient()
mailing_client = MailingClient()

# Repositories
sqlalchemy_user_repository = SQLAlchemyUsersRepository(sqlalchemy_client)
sqlalchemy_event_repository = SQLAlchemyEventsRepository(sqlalchemy_client)
sqlalchemy_wishlist_repository = SQLAlchemyWishlistRepository(sqlalchemy_client)
sqlalchemy_event_user_repository = SQLAlchemyEventUsersRepository(sqlalchemy_client)

# Usecases
users_usecase = ManageUsersUsecase(sqlalchemy_user_repository)
wishlist_usecase = ManageWishlistUsecase(sqlalchemy_wishlist_repository, bucket_client)
events_usecase = ManageEventsUsecase(
    sqlalchemy_event_repository, 
    sqlalchemy_event_user_repository, 
    users_usecase,
    wishlist_usecase,
    mailing_client,
)

blueprints = [
    create_healthcheck(),
    create_users_controller(users_usecase),
    create_events_controller(events_usecase),
    create_wishlist_controller(wishlist_usecase),
    create_landing_controller(users_usecase),
    create_home_controller(users_usecase, events_usecase),
    create_frontevent_controller(events_usecase),
    create_profile_controller(users_usecase),
    create_frontend_wishlist_controller(wishlist_usecase, events_usecase),
]

commands = {
    "seed": seed(sqlalchemy_client)
}

app = create_flask_app(blueprints, commands)
