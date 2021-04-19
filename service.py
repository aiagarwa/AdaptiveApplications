import ast
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
import json
import jinja2
from markupsafe import escape
import pandas as pd
import pdb
import pickle
import random
from sqlalchemy import func

from user import User
from user_history import UserHistory
from forms.log_in import LogInForm
from forms.preferences import PreferencesForm
from forms.recipe_selection import RecipeSelectionForm
from forms.recommend import RecommendForm
from forms.sign_up import SignUpForm

from recommendation_engine import RecommendationEngine

from extension import db
import os
import click
SECRET_KEY = os.urandom(32)


app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = SECRET_KEY
# database config
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://otter@aaotter:)).~32_t@aaotter.postgres.database.azure.com/otter"
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
    if session.get('logged_in'):
        return redirect(url_for('index'))

    form = LogInForm()
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
                session["user_id"] = data.id
                session["username"] = form.username.data
                session["preferences"] = pickle.dumps(data.preferences)

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


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if session.get('logged_in'):
        return redirect(url_for('index'))

    form = SignUpForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            password=form.password.data)

        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id
        session['logged_in'] = True
        session['username'] = form.username.data
        session['preferences'] = pickle.dumps(new_user.preferences)

        return redirect(url_for('preferences'))

    return render_template(
        'sign_up.html',
        form=form,
        template='templates/sign_up.html',
        username=None,
        logged_in=False,
        title='Sign Up'
    )


@app.route('/preferences', methods=["GET", "POST"])
def preferences():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # Get user preferences
    prefs = pickle.loads(session["preferences"])

    form = PreferencesForm()
    if form.validate_on_submit():
        # Get form values and update user preferences
        data = form.data
        prefs.update(data)

        # Update user preferences in the database
        user = User.query.filter_by(userName=session["username"]).first()
        user.preferences = prefs
        db.session.commit()

        # Update user preferences in the session
        session["preferences"] = pickle.dumps(prefs)

        return redirect(url_for('index'))

    # Pre-select user's current preferences
    form.cuisines.default = prefs.cuisines
    form.allergies.default = prefs.allergies
    form.process()

    return render_template(
        "preferences.html",
        form=form,
        template="templates/preferences.html",
        prefs=prefs,
        username=session["username"],
        logged_in=True,
        title="Preferences"
    )


@app.route('/recipe', methods=["GET", "POST"])
def recipe():
    if not session.get('logged_in'):
        return redirect(url_for('index'))

    if 'recipeid' not in request.values:
        return redirect(url_for('index'))

    # Save user's pick to the UserHistory table
    print(request.values)

    # Do we want to have the user provide a numerical rating?
    # Would that make it seem less "adaptive"?
    entry = UserHistory(
        user_id=session['user_id'],
        username=session['username'],
        recipe_id=request.values['recipeid'],
        mood=request.values['mood'],
        weather=request.values['weather'],
        rating=2)

    db.session.add(entry)
    db.session.commit()

    # Convert string of dict to dict
    recipe = ast.literal_eval(request.values['recipe'])

    # Convert string of list to list
    recipe['ingredients'] = ast.literal_eval(recipe['ingredients'])
    recipe['steps'] = ast.literal_eval(recipe['steps'])

    # Get similar recipes
    prefs = pickle.loads(session["preferences"])
    recommender = RecommendationEngine(prefs, 30)
    similar_recipes = recommender.get_recommendation_filters()

    return render_template(
        "recipe.html",
        recipe=recipe,
        similar_recipes=similar_recipes,
        template="templates/recipe.html",
        username=session["username"],
        logged_in=True,
        title="Recipe"
    )


@app.route('/recommend', methods=["GET", "POST"])
def recommend():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    prefs = pickle.loads(session["preferences"])

    form = RecommendForm()
    if form.validate_on_submit():
        prefs.health_goals = form.healthGoals.data
        prefs.level_of_activity = form.levelOfActivity.data
        timeToCook = form.timeToCook.data

        # Create tag needed to pass time as filter
        timeToCook = 'cooking_time_less_than_%s' % timeToCook

        prefs.time_to_cook = timeToCook

        prefs.current_mood = form.mood.data
        prefs.current_weather = form.weather.data

        recommender = RecommendationEngine(prefs, timeToCook)
        recommendations = recommender.get_recommendation_filters()

        selection_form = RecipeSelectionForm()

        return render_template(
            "results.html",
            template="templates/results.html",
            username=session["username"],
            logged_in=True,
            data=recommendations,
            mood=form.mood.data,
            weather=form.weather.data,
            title="Results",
            form=selection_form
        )

    return render_template(
        "recommendations.html",
        form=form,
        template="templates/recommendations.html",
        username=session["username"],
        logged_in=True,
        title="Recommendation"
    )


@app.route('/sign_out')
def sign_out():
    session.clear()

    return redirect(url_for('login'))


@app.route('/drop')
def dropdb():
    db.drop_all()


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


@app.route('/history')
def get_user_histories():
    history = UserHistory.query.all()

    result = []
    for entry in history:
        data = vars(entry)
        data.pop('_sa_instance_state', None)
        result.append(data)

    groupings = UserHistory.query.with_entities(UserHistory.recipeId, UserHistory.mood, UserHistory.weather, func.count(UserHistory.historyId)).group_by(UserHistory.recipeId, UserHistory.mood, UserHistory.weather).all()

    df = pd.DataFrame(groupings, columns=['recipe_id', 'mood', 'weather', 'count'])

    print(df)

    return jsonify(result)


@app.route('/dummy_history')
def create_dummy_histories():
    mood = ['angry', 'happy', 'sad']
    weather = ['cold', 'rainy', 'sunny']

    results = []
    num_samples = 25
    for x in range(num_samples):
        entry = UserHistory(
            mood=random.choice(mood),
            weather=random.choice(weather),
            rating=random.randrange(10),
            recipe_id=random.randrange(100),
            user_id=random.randrange(1,3),
            username='test')

        results.append(entry)

    db.session.add_all(results)
    db.session.commit()

    return jsonify('Created %s dummy user histories' % len(results))


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
