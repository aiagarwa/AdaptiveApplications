from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
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
cuisines = ['african', 'american', 'chinese', 'english', 'french', 'greek', 'indian', 'italian', 'japanese', 'mexican', 'spanish', 'thai']

allergies = ['---', 'dairy', 'egg', 'fish', 'peanuts', 'soya', 'tree_nuts', 'wheat']

class PreferencesForm(FlaskForm):
    """ Food preferences form """

    # Create cuisine tuples (LHS = key, RHS = label)
    cuisine_options = []
    for c in cuisines:
        cuisine_options.append((c, c.title()))

    # Create allergy tuples (LHS = key, RHS = label)
    allergy_options = []
    for a in allergies:
        allergy_options.append((a, a.replace('_', ' ')))

    allergies = SelectMultipleField(
        'Allergies',
        choices=allergy_options,
        default=allergy_options[0]
    )
    cuisines = SelectMultipleField(
        'Cuisines',
        [DataRequired()],
        choices=cuisine_options,
    )

    vegetarian = BooleanField(
        'Vegetarian',
    )

    submit = SubmitField('Submit')
