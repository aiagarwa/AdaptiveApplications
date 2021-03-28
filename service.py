from flask import Flask, jsonify, redirect, render_template, session, url_for
import jinja2
from markupsafe import escape
import pdb

from user import User
from forms.log_in import LogInForm
from forms.preferences import PreferencesForm
from forms.sign_up import SignUpForm

from recommendation_engine import RecommendationEngine

from extension import db
import os
import click
SECRET_KEY = os.urandom(32)


app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = SECRET_KEY
# database config
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://otter@aagroup:fdT:)qvNmZ8D5%*d>d.W@aagroup.postgres.database.azure.com/otter"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)

    TEMPLATE_FILE = "templates/home.html"
    template = templateEnv.get_template(TEMPLATE_FILE)
    return template.render(
        title='Home',
        username=session["username"])


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Form"""

    form = LogInForm()

    print("log in form")

    if form.validate_on_submit():
        print("attempting to log in")
        name = form.username.data
        password = form.password.data
        try:
            # data = User.query.filter_by(username=name, password=password).first()
            data = User.query.filter_by(userName=name).first()
            if data is not None:
                # Set user's session variables
                session['logged_in'] = True
                session["username"] = form.username.data
                return redirect(url_for('index'))
            else:
                print("don't log user in")
                return 'Dont Login'
        except:
            print("Error occurred - don't log user in")
            return "Dont Login"

    return render_template(
        "log_in.html",
        form=form,
        template="templates/log_in.html",
        username=None,
        logged_in=False,
        title="Log In"
    )


@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            password=form.password.data)

        db.session.add(new_user)
        db.session.commit()

        session['logged_in'] = True
        session["username"] = form.username.data

        return redirect(url_for('index'))

    return render_template(
        "sign_up.html",
        form=form,
        template="templates/sign_up.html",
        username=None,
        logged_in=False,
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
        username=session["username"],
        logged_in=True,
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


# test add user
@app.route('/add')
def adduser():
    user = User()
    user.userName = os.urandom(8)
    db.session.add(user)
    db.session.commit()
    return user.userName

@app.route('/query')
def queryuser():
    users = User.query.all()
    ans = ""
    for user in users:
        ans += user.userName + " -- "
    return ans

@app.before_first_request
def initdb():
    print("-----------")
    db.create_all()

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))

app.run(debug=True)
