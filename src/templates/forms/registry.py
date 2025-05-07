from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Regexp, Length

from src.utils import *


class RegistryForm(FlaskForm):
    name = StringField(
        NAME_FIELD, validators=[DataRequired(), Length(min=NAME_LENGTH, message=NAME_FIELD_LENGTH_ERROR)]
    )
    email = StringField(
        EMAIL_FIELD, validators=[DataRequired(), Email(message=EMAIL_FIELD_ERROR)]
    )
    password = PasswordField(
        PASSWORD_FIELD,
        validators=[
            DataRequired(),
            Regexp(
                PASSWORD_REGEX, message=PASSWORD_REQUIREMENTS
            ),
        ],
    )

    submit = SubmitField("Sign Up")
