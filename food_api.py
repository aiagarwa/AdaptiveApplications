import ast
import pandas as pd
import pdb
import requests

from user import User

FILENAME = 'datasets/recipes_less_data_v3.csv'

DF = pd.read_csv(FILENAME)


def filter_by_time(df, user):
    """ Filter recipes by user's available time to cook """

    time = user.time_to_cook.replace('cooking_time_less_than_', '')

    return df.loc[df.minutes <= int(time)]


def filter_by_cuisine(df, user):
    """
    Flag and remove the recipes whose tags do not include at least one of the
    user's cuisine preferences.
    """

    if len(user.cuisines) == 0:
        # User has selected no cuisines - do not need to remove recipes
        return df

    return df.loc[df.cuisines.isin(user.cuisines)]


def remove_recipes_with_allergies(df, user):
    """
    Flag and remove the recipes that contain one or more ingredients that the
    user is allergic to.
    """

    if len(user.allergies) == 0:
        # User has no allergies - do not need to remove recipes
        return df

    allergies = [a + '_allergic' for a in user.allergies]

    return df.loc[df[allergies].any(1) == False]


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
    df = filter_by_cuisine(df, user)
    df = remove_recipes_with_allergies(df, user)

    if user.vegetarian == True:
        df = df.loc[df.vegetarian == 1]

    recommendations = df.head(6)
    recommendations.fillna('', inplace=True)

    # Convert DataFrame to JSON like object
    recommendations = recommendations.to_dict(orient='records')

    return recommendations
