from flask_wtf import FlaskForm
from wtforms import (
    SelectMultipleField,
    StringField,
    SubmitField,
    TextField)
from wtforms.fields.html5 import IntegerRangeField
from wtforms.validators import (
    DataRequired,
    Length,
)


class PreferencesForm(FlaskForm):
    """ Food preferences form """

    allergies = SelectMultipleField(
        'Allergies',
        choices=[
            ('dairy', 'dairy'),
            ('nuts', 'nuts'),
            ('wheat', 'wheat')
        ]
    )
    cuisines = SelectMultipleField(
        'Cuisines',
        [DataRequired()],
        choices=[
            ('burgers', 'Burgers'),
            ('indian', 'Indian'),
            ('italian', 'Italian'),
        ],
    )
    spicyness = IntegerRangeField(
        'Spicyness',
        default=5,
    )
    submit = SubmitField('Submit')
