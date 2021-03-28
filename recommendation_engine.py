import configparser
import pdb

import food_api

# Stereotypes attributes are stored in an .ini file
config = configparser.ConfigParser()
config.read('resources/stereotypes.ini')


class RecommendationEngine():

    def __init__(self, user, time_to_cook=30):
        # User model passed into recommender
        self.user = user
        self.time_to_cook = time_to_cook

        # STEP 1: check if model contains values for all features
        # E.g.: spiciness, cuisines

        # STEP 2: match user to a stereotype

        # STEP 3: merge user and stereotype preferences
        # Stereotype preferences will fill in gaps in user model
        # Also, will be used to show user some variety?
        # ^ That could be an additional feature - have a try something new
        # button


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
        TODO: this function will combine user and stereotype preferences?
        """

        # Add health goal stereotypes to user model
        stereotype_features = self.match_to_stereotype()

        # TODO: add these stereotype values to the user model
        # cuisines = set(self.user.cuisines + stereotype.cuisines)

        return food_api.generate_recommendations(self.user)
