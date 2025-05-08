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
