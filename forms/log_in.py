from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    StringField,
    SubmitField,
    PasswordField,
    DateField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
)


class LogInForm(FlaskForm):
    """ Form for user to log in """

    username = StringField(
        'Username',
        [DataRequired()]
    )
    password = PasswordField(
        'Password',
        [
            DataRequired(message="Please enter a password."),
        ]
    )
    submit = SubmitField('Submit')
