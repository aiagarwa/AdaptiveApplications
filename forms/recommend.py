from flask_wtf import FlaskForm
from wtforms import (
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


class RecommendForm(FlaskForm):
    """ Form for meal recommendation """

    # healthGoals = SelectMultipleField(
    #     'Health Goals',
    #     [DataRequired()],
    #     choices=[
    #         ('less_fat', 'Eat less fat'),
    #         ('more_veg', 'Eat more vegetables'),
    #     ],
    # )
    levelOfActivity = IntegerRangeField(
        'Level of Activity',
        default=5,
    )
    timeToCook = IntegerRangeField(
        'Time to Cook',
        default=30,
    )
    mood = SelectField(
        'Mood',
        [DataRequired()],
        choices=[
            ('happy', 'happy'),
            ('sad', 'sad'),
            ('angry', 'angry'),
        ],
    )
    weather = SelectField(
        'Weather',
        [DataRequired()],
        choices=[
            ('sunny', 'sunny'),
            ('rainy', 'rainy'),
            ('cold', 'cold'),
        ],
    )
    submit = SubmitField('Submit')
