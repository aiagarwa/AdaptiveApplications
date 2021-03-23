import ast
import pandas as pd
import pdb
import requests

from user import User

FILENAME = 'resources/RAW_recipes.csv'

DF = pd.read_csv(FILENAME)


def filter_by_time(df, user):
    """ Filter recipes by user's available time to cook """
    return df.loc[df.minutes <= user.time_to_cook]


def filter_by_cuisine(df, user):
    """
    Flag and remove the recipes whose tags do not include at least one of the
    user's cuisine preferences.
    """

    if len(user.cuisines) == 0:
        # User has selected no cuisines - do not need to remove recipes
        return df

    df['cuisine_match'] = df.apply(lambda row:
        check_if_recipe_matches_cuisine(row.tags, user), axis=1)

    return df.loc[df.cuisine_match == True]


def check_if_recipe_matches_cuisine(tags, user):
    """ Check recipe tags for user's selected cuisine(s) """

    # Convert string containing list to list
    tags = ast.literal_eval(tags)

    if len(list(set(tags) & set(user.cuisines))) > 0:
        # Recipe tags contains user's cuisine(s)
        return True

    return False


def remove_recipes_with_allergies(df, user):
    """
    Flag and remove the recipes that contain one or more ingredients that the
    user is allergic to.
    """

    if len(user.allergies) == 0:
        # User has no allergies - do not need to remove recipes
        return df

    df['allergy_present'] = df.apply(lambda row:
        check_for_allergies(row.ingredients, user), axis=1)

    return df.loc[df['allergy_present'] == False]


def check_for_allergies(ingredients, user):
    """ Check recipe ingredients for allergies """

    # Convert string containing list to list
    recipe = ast.literal_eval(ingredients)

    if len(list(set(recipe) & set(user.allergies))) > 0:
        # Recipe ingredients contains allergy
        return True

    return False


def get_unique_tags(df):
    """ Get list of unique tags in dataset (this is slow) """
    tags = []

    for index, row in df.iterrows():
        tags = list(set(tags + ast.literal_eval(row.tags)))

    pdb.set_trace()


def get_recipe_dataset():
    """ Load recipe dataset from csv downloaded from Kaggle """
    df = pd.read_csv(FILENAME)
    print("# of rows - no filtering: %s" % len(df))

    df = df.head(500)
    print("# of rows - reduce size of DF for testing: %s" % len(df))

    return df


def generate_recommendations(user):
    # This is a little janky - once I preprocess the data I'll clean it up
    # df = get_recipe_dataset()
    df = DF

    df = filter_by_time(df, user)
    print("# of rows - time filter: %s" % len(df))

    df = filter_by_cuisine(df, user)

    df = remove_recipes_with_allergies(df, user)
    print("# of rows - allergy filter: %s" % len(df))

    # TODO: this needs to be made smarter (not just first 2 results)
    recommendations = df.head(2)
    recommendations.fillna('', inplace=True)

    # Convert DataFrame to JSON like object
    recommendations = recommendations.to_dict(orient='records')

    return recommendations
