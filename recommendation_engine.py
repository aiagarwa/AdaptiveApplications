import configparser
import pandas as pd
import pdb
import random

import item_based_coll_filtering_mood_weather_ratings as COL

# import food_api as GOALS
# import similar_users_recommendation as USERS

# Stereotypes attributes are stored in an .ini file
config = configparser.ConfigParser()
config.read('resources/stereotypes.ini')

RECIPES = pd.read_csv('datasets/recipes_less_data_v3.csv')


class RecommendationEngine():

    def __init__(self, user, time_to_cook=30):
        # User model passed into recommender
        self.user = user
        self.time_to_cook = time_to_cook


    def match_to_stereotype(self):
        """
        TODO: get stereotype for user
         - We could make this a stereotype for their health goal(s)?
        """

        # Example of goal: 'less_fat'
        goal = self.user.health_goals[0]

        # TODO: if users can have more than one health goal this will need to
        # be updated
        stereotype = dict(config.items(goal))
        print("Stereotype: %s" % goal)
        print("Stereotype cuisines: %s" % stereotype['cuisines'])
        print("Stereotype tags: %s" % stereotype['tags'])

        return stereotype


    def get_recommendation_filters(self):
        """
        Get the recommendations based off of:
        * similar users
        * mood and weather
        """

        # NOTE: This will be replaced with calls to the scripts
        # Placeholder for now

        results = COL.get_all_recommendations(
            user_id=491979,
            weather=self.user.current_weather,
            mood=self.user.current_mood,
            filtering=['cooking_time_less_than_30'])

        mood_weather_key = 'Mood Weather Ratings Recommendations'
        similar_users_key = 'Similar User Recommendations'

        return {
            mood_weather_key: self.get_recipes_from_ids(results[mood_weather_key]),
            similar_users_key: self.get_recipes_from_ids(results[similar_users_key])
        }


    @staticmethod
    def get_recipes_from_ids(score_df):
        """
        Match recipes ids from recommendation list to recipe dataset.
        Used to get all recipe info such as number of steps, ingredients, etc.
        """

        ids = score_df.recipe_id.tolist()

        recipes = RECIPES.loc[RECIPES.id.isin(ids)]

        # Merge score into recipe info
        recipes = recipes.merge(score_df, left_on='id', right_on='recipe_id')

        return recipes.to_dict(orient='records')


    @staticmethod
    def get_random_sample_of_recipes():
        """
        Temporary function to random return recipes until recommendation
        scripts ready
        """

        random_idxs = random.sample(list(range(len(RECIPES))), 3)

        random_recipes = RECIPES.iloc[random_idxs]

        return random_recipes.to_dict(orient='records')


    @staticmethod
    def get_reason_for_recommendation(reason_key):
        base = "We think you will like this as "

        if reason_key == 'health_goal':
            return base + 'it matches your health goal'
        elif reason_key == 'similar_users':
            return base + 'similiar users liked this recipe'

        return base + 'TODO'
