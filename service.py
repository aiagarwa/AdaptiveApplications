from flask import Flask, jsonify, redirect, render_template, url_for
import jinja2
from markupsafe import escape
import pdb

from user import User
from forms.preferences import PreferencesForm
from forms.sign_up import SignUpForm

from recommendation_engine import RecommendationEngine

import os
SECRET_KEY = os.urandom(32)


app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def index():
    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)

    user = User(name='John', age=36)

    TEMPLATE_FILE = "templates/home.html"
    template = templateEnv.get_template(TEMPLATE_FILE)
    outputText = template.render(title='Home', user=user)

    return outputText

@app.route('/login')
def login():
    return 'login'

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        return "ok"

    return render_template(
        "sign_up.html",
        form=form,
        template="templates/sign_up.html",
        user=None,
        title="Sign Up"
    )

@app.route('/preferences', methods=["GET", "POST"])
def preferences():
    form = PreferencesForm()

    if form.validate_on_submit():
        return "ok"

    return render_template(
        "preferences.html",
        form=form,
        template="templates/preferences.html",
        user=None,
        title="Preferences"
    )

@app.route('/recommend')
def recommend():

    user = User()
    user.allergies = ["celery"]
    user.time_to_cook = 30

    recommender = RecommendationEngine(user)
    recommendations = recommender.get_recommendation_filters()

    # TODO: create a Jinja2 template for showing responses
    # (not just turning a JSON object)
    return jsonify(recommendations)


# For user
# https://flask.palletsprojects.com/en/1.1.x/quickstart/#variable-rules
@app.route('/user/<username>')
def profile(username):
    return '{}\'s profile'.format(escape(username))

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))

app.run(debug=True)
