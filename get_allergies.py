
def check_for_dairy(ingredient):
    buzzwords = ['cheese', 'cream']

    for i in buzzwords:
        if i in ingredient:
            return True

    if 'milk' in ingredient:
        # Coconut milk isn't dairy
        if 'coconut' not in ingredient:
            return True

    return False


def check_for_eggs(ingredient):
    if 'egg' not in ingredient:
        # Ingredient doesn't contain word egg (so it's ok)
        return False

    if 'eggplant' in ingredient:
        return False

    if 'egg substitute' in ingredient:
        return False

    # Ingredient is egg-based
    return True


def check_for_peanuts(ingredient):
    if 'peanuts' not in ingredient:
        return False

    return True


def check_for_tree_nuts(ingredient):
    if 'nut' not in ingredient:
        return False

    ok_nuts = [
        'coconut', 'doughnuts', 'minute', 'nutmeg', 'nutritional',
        'water chestnuts']

    for ok in ok_nuts:
        if ok in ingredient:
            return False

    return True


def check_for_fish(ingredient):
    buzzwords = [
        'anchovy', 'cod,' 'crab', 'fish', 'haddock', 'halibut',
        'oyster', 'perch', 'salmon', 'sardine', 'sea bass', 'shrimp', 'sole',
        'trout', 'tuna']

    for i in buzzwords:
        if i in ingredient:
            return True

    if 'eel' in ingredient and 'peel' not in ingredient:
        return True

    return False


def check_for_soya(ingredient):
    if 'soy' not in ingredient:
        return False

    return True


def check_for_wheat(ingredient):
    buzzwords = [
        'bran', 'bread', 'bulgar', 'bun', 'couscous', 'cereal', 'cracker',
        'crouton', 'farina', 'flour', 'germ', 'gluten', 'malt', 'noodle',
        'pasta', 'seitan', 'semolina', 'soy sauce', 'starch', 'vermicelli', 'wheat',
        'whole grain'
    ]

    for i in buzzwords:
        if i in ingredient:
            return True

    return False


dairy_ingredients = []
egg_ingredients = []
tree_nuts_ingredients = []
nuts_ingredients = []
fish_ingredients = []
soya_ingredients = []
wheat_ingredients = []

f = open("resources/ingredients.txt", "r")

for ingredient in f:
    ingredient = ingredient.replace('\n', '').lower()

    if check_for_dairy(ingredient) == True:
        dairy_ingredients.append(ingredient)
    if check_for_eggs(ingredient) == True:
        egg_ingredients.append(ingredient)
    if check_for_tree_nuts(ingredient) == True:
        tree_nuts_ingredients.append(ingredient)
    if check_for_peanuts(ingredient) == True:
        nuts_ingredients.append(ingredient)
    if check_for_fish(ingredient) == True:
        fish_ingredients.append(ingredient)
    if check_for_soya(ingredient) == True:
        soya_ingredients.append(ingredient)
    if check_for_wheat(ingredient) == True:
        wheat_ingredients.append(ingredient)

f.close()

# print(dairy_ingredients)
# print(egg_ingredients)
