import configparser
import pandas as pd
import pdb
import random

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
        return {
            'recommendation_type_1': self.get_random_sample_of_recipes(),
            'recommendation_type_2': self.get_random_sample_of_recipes(),
        }


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
