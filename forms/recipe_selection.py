from flask_wtf import FlaskForm
from wtforms import (
    HiddenField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
    TextField)
from wtforms.fields.html5 import IntegerRangeField
from wtforms.validators import (
    DataRequired,
    Length,
)


class RecipeSelectionForm(FlaskForm):
    """ Form for user recipe selection """

    recipeid = HiddenField(
        'Recipe Id',
    )
    reason = HiddenField(
        'Reason',
    )
    name = HiddenField(
        'Name',
    )
    weather = HiddenField(
        'Weather',
    )
    mood = HiddenField(
        'Mood',
    )
    submit = SubmitField('Submit')
