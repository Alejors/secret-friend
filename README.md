# Secret Santa APP

### Video Demo:  
<[Watch the presentation](https://youtu.be/aZ5OnreyTc4)>

### Description:

Secret Santa APP is a web application where you can create and manage secret santa contests.

## Technologies:

- Python
- Flask
- Jinja2
- MySQL
- Docker
- Github Copilot

## Structure

The project was developed following a repository pattern. Requests are managed by a controller, the controller send the data to a usecase. Usecases have a specific repository which has the required methods to access or create records in databases, or create requests to third-party APIs (e.g. SendGrid). 

The project was developed complying with **SOLID principles** and **ACID** transactions with rollbacks in when exceptions happen during event drawing.

```
secret-santa/                                   # Root directory of the project
├── migrations/                                 # Alembic migrations directory
│   ├── env.py                                  # Alembic environment configuration
│   ├── script.py.mako                          # Alembic script template
│   └── versions/                               # Directory for migration scripts
├── src/                                        # Source code directory
│   ├── controllers/                            # Flask controllers
│   │   ├── __init__.py                         # Module initialization for easy access to imports
│   │   ├── health_check.py                     # Controller for health check route
│   │   ├── home_controller.py                  # Controller for home-related routes
│   │   ├── landing_controller.py               # Controller for landing page routes (login/registry)
│   │   ├── profile_controller.py               # Controller for profile-related routes
│   │   ├── wishlist_controller.py              # Controller for wishlist-related routes
│   │   └── event_controller.py                 # Controller for event-related routes
│   ├── entities/                               # Domain entities
│   │   ├── __init__.py                         # Module initialization
│   │   ├── user.py                             # User entity
│   │   ├── event.py                            # Event entity
│   │   └── wish.py                             # Wish entity
│   ├── frameworks/                             # Framework-specific utilities and configurations
│   │   ├── db/                                 # Database-related utilities
│   │   │   ├── __init__.py                     # Module initialization for the db package
│   │   │   ├── seeds/                          # Database seeding scripts
│   │   │   │   ├── __init__.py                 # Module initialization for the seeds package
│   │   │   │   └── sql/                        # SQL seed scripts
│   │   │   │       ├── init-data.sql           # Initial data for database seeding
│   │   │   │       └── tables-dll.sql          # Database schema definitions
│   │   │   └── sqlalchemy/                     # SQLAlchemy-specific utilities
│   │   │       ├── __init__.py                 # Module initialization for the sqlalchemy package
│   │   │       └── sqlalchemy_client.py        # SQLAlchemy client setup
│   │   ├── http/                               # HTTP-related utilities
│   │   │   ├── codes_constants.py              # HTTP response codes constants
│   │   │   ├── flask.py                        # Flask application factory and configurations
│   │   │   └── http_response_codes.py          # HTTP response status codes
│   │   ├── jinja/                              # Jinja2-related utilities
│   │   │   └── custom_filters.py               # Custom Jinja2 filters
│   │   └── mail/                               # Email-related utilities
│   │       ├── client.py                       # Gmail Mailing client implementation
│   │       └── sendgrid_client.py              # SendGrid-specific mailing client
│   ├── interfaces/                             # Interfaces for repositories and use cases
│   │   ├── __init__.py                         # Module initialization
│   │   ├── event_user_interface.py             # Interface for event_user repository
│   │   ├── data_interface.py                   # Base interface for data repositories
│   │   ├── mailer_interface.py                 # Interface for any mailing repository
│   │   └── wishlist_interface.py               # Interface for wishlist repository
│   ├── models/                                 # SQLAlchemy models
│   │   ├── __init__.py                         # Module initialization
│   │   ├── base_model.py                       # Base SQL Alchemy model. Including commong methods
│   │   ├── user_model.py                       # User model
│   │   ├── event_model.py                      # Event model
│   │   └── wishlist_model.py                   # Wish model
│   ├── repositories/                           # Repository implementations
│   │   ├── __init__.py                         # Module initialization
│   │   ├── base_repository.py                  # Base repository for SQLAlchemy
│   │   ├── gmail_email_repository.py           # Repository to connect with Gmail mailing service
│   │   ├── sendgrid_email_repository.py        # Repository to connect with SendGrid mailing service
│   │   ├── sqlalchemy_user_repository.py       # SQLAlchemy User repository
│   │   ├── sqlalchemy_event_repository.py      # SQLAlchemy Event Repository
│   │   ├── sqlalchemy_event_user_repository.py # SQLAlchemy Event-User Repository
│   │   └── sqlalchemy_wishlist_repository.py   # SQLAlchemy Wishlist repository
│   ├── static/                                 # Static files directory
│   │   └── img/                                # Images
│   │       └── gift.png                        # Image used in the Navbar
│   ├── templates/                              # Jinja2 templates directory
│   │   ├── forms/                              # WTForms directory
│   │   │   ├── __init__.py                     # Module initialization for imports
│   │   │   ├── event.py                        # Event creation form
│   │   │   ├── login.py                        # Login form
│   │   │   ├── profile.py                      # Profile update form
│   │   │   ├── registry.py                     # Sign up form
│   │   │   └── wishlist.py                     # Wishes creation form
│   │   ├── base.html                           # Base HTML template
│   │   ├── nav.html                            # Navigation bar template
│   │   ├── profile.html                        # Profile page template
│   │   ├── wishlist.html                       # Wishlist page template
│   │   ├── edit_item.html                      # Wish update page template
│   │   ├── home.html                           # Home page template
│   │   ├── login.html                          # Login page template
│   │   ├── register.html                       # Registry page template
│   │   ├── manage_events.html                  # Event management page template
│   │   ├── flash_messages.html                 # CSS Styles for flash messages to be displayed
│   │   ├── css_login.html                      # Login and registry specifig CSS styles
│   │   └── css_html.html                       # CSS styles base styles included in base
│   ├── usecases/                               # Application use cases
│   │   ├── __init__.py                         # Module initialization
│   │   ├── users_usecase.py                    # Use case for managing users
│   │   ├── events_usecase.py                   # Use case for managing events
│   │   └── wishlist_usecase.py                 # Use case for managing wishlists
│   ├── utils/                                  # Utility functions
│   │   ├── __init__.py                         # Module initialization
│   │   ├── dates.py                            # Helper for date formatting
│   │   ├── encryption.py                       # Helper for password encryption and checking
│   │   ├── random_password.py                  # Function to generate random passwords
│   │   ├── form_constants.py                   # Constants for WTForms
│   │   ├── mail_constants.py                   # Constants for Mails templates
│   │   └── token.py                            # Helper for token creation
│   └── main.py                                 # Entry point for the Flask application
├── .env.example                                # Example environment variables file
├── .gitignore                                  # Git ignoring configuration
├── alembic.ini                                 # Alembic configurations for migrations
├── docker-compose.yml                          # Docker Compose configuration file
├── Dockerfile                                  # Docker file with commands to build the main container
├── README-ES.md                                # Spanish version of the project documentation
├── README.md                                   # Project documentation
└── requirements.txt                            # Text file for all required dependencies to be installed
```

#### Creating an Event

To create an **Event**, you need to create and log into your account, navigate to the **Manage Events** tag, and define a name, optionally minimum and/or maximum gift price, and participants. 

**Important**: *There is a minimum of 3 participants required to create a valid event (less than 3 would not make sense)*.

After creating the event, a purple button will be displayed on the right side of the screen (bottom if mobile), which says "Draw Event". Clicking this button will randomly pick contestants from the list and assign to each other participant for them to be secret Santa.

#### Wishlist

Optionally you can add *wishes* to your wishlist. 
This wishes will show to your secret Santa when an event has been drawn it they:

- Don't have a price.
- It's price is set to 0.
- They match the event's constraints (i.e. the event has a minimum of $10 and maximum of $20, only gifts within this range will appear).
- The event doesn't have any price constraints.

#### Profile

You can change your name and password anytime, but not your email since it is the main distinctive information used when creating events.

#### Home

Your home will show every Event you've been added to. Toggling events let you know who you are secret Santa for and the wishlist that matches the event's constraints.

## Deployment

Once the repository is cloned, the *.env* file must be created. You can use *.env.example* as boilerplate since it is configured to work locally.

**Notes**: 
- A *JWT_SECRET_KEY* and *FLASK_SECRET_KEY* are needed for flask to maintain sessions and tokens to be created and checked.
- A *SENDGRID_API_KEY* and *MAIL_USER* must be added if you want mails to be delivered using SendGrid.

Once the previous is done, run the command:

```
docker-compose up --build
```

This will clone necessary docker images, compile them and start the containers (Python 3.12 and MySQL). 

### Healthcheck

To verify the application is up and ready, you can make a request from your terminal by running:

```
curl --location 'localhost:8000/health-check'
```

## Migrations

### Run

Once the service is up, the Database needs to run migrations for the tables to be created. This application uses *alembic*, so running migrations is easy as running:

```
docker-compose exec api alembic upgrade head
```

### Creating New Migrations

In case DB models are modified, an alembic command can be run to create new migrations:

```
docker-compose exec api alembic revision --autogenerate -m"<descriptive message>"
```

Migrations will be stored in: *migrations/versions*. 

## DB Seeding

With the Database already up to date, you can insert test information using seeds.
To help with this, the command *seed* was created and you can run:

```
docker-compose exec api flask --app src.main:app seed
```

This command runs SQL statements defined in:

- init-data.sql

The passwords defined for seeded users is Hola1234, considering the *JWT_SECRET_KEY*: **MyM3g45up3r53cr3tK3y!** 
