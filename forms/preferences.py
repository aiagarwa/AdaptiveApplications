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

# Turkey has turkey in it - not Turkish?
cuisines = ["indian", "japanese", "spanish", "english", "mexican", "italian", "chinese", "greek", "french", "african", "thai"]

class PreferencesForm(FlaskForm):
    """ Food preferences form """

    # Create cuisine tuples (LHS = key, RHS = label)
    cuisines_prepped = []
    for c in cuisines:
        cuisines_prepped.append((c, c.title()))


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
        choices=cuisines_prepped,
    )
    spiciness = IntegerRangeField(
        'Spiciness',
        default=5,
    )

    # Mood inputs
    happy_foods = SelectMultipleField(
        'Happy',
        [DataRequired()],
        choices=cuisines_prepped,
    )
    sad_foods = SelectMultipleField(
        'Sad',
        [DataRequired()],
        choices=cuisines_prepped,
    )
    angry_foods = SelectMultipleField(
        'Angry',
        [DataRequired()],
        choices=cuisines_prepped,
    )

    submit = SubmitField('Submit')
