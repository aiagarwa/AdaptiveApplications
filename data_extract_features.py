# -*- coding: utf-8 -*-
"""Data_Preprocessing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1F735mILOTb8bkR_qaI-q8svzZ8KDS5YC
"""

import pandas as pd
import numpy as np

from google.colab import drive 
drive.mount('/content/gdrive')

# read the raw data
df_raw_recipes = pd.read_csv('gdrive/My Drive/RAW_recipes.csv')
display(df_raw_recipes.head())

# get the information of tags
tags = df_raw_recipes.tags.apply(lambda x: x[1:-1].split(','))
d = {}
size = len(df_raw_recipes)
for tag in tags:
    for item in tag:
        s = item.strip().strip("\'")
        if(len(s) > 0) :
            if s in d:
                d[s] = d[s] + 1
            else:
                d[s] = 1
                
# print the tag and frequency
for kv in sorted(d.items(), key = lambda kv:(kv[1], kv[0]), reverse=True):
    print(kv)

# some tags
# cook time:   60-minutes-or-less, 30-minutes-or-less, 4-hours-or-less, 15-minutes-or-less, 1-day-or-more
# cuisines: japanese, spanish, english,mexican, midwestern,turkey, indian, european, greek, chinese, thai, french, african,(north-american, american, northeastern-united-states, southwestern-united-states, american),asian, italian, canadian
# vegetarian
# comfort-food
# healthy
# flavors: spicy sweet

# add new columns from nutrition
nutritions = df_raw_recipes.nutrition.apply(lambda x: x[1:-1].split(','))
# separate nutrition column
calories = []
total_fat = []
sugar = []
sodium = []
protein = []
saturated_fat = []

for n in nutritions:
    if(len(n) == 0):
         print("Find missing value")
    else:
        calories.append(float(n[0])) 
        total_fat.append(float(n[1]))
        sugar.append(float(n[2]))
        sodium.append(float(n[3]))
        protein.append(float(n[4]))
        saturated_fat.append(float(n[5]))

df_raw_recipes.insert(len(df_raw_recipes.columns), "calories", calories)
df_raw_recipes.insert(len(df_raw_recipes.columns), "total_fat", total_fat)
df_raw_recipes.insert(len(df_raw_recipes.columns), "sugar", sugar)
df_raw_recipes.insert(len(df_raw_recipes.columns), "sodium", sodium)
df_raw_recipes.insert(len(df_raw_recipes.columns), "protein", protein)
df_raw_recipes.insert(len(df_raw_recipes.columns), "saturated_fat", saturated_fat)

display(df_raw_recipes.head())
print(df_raw_recipes.info())

# add vegetarian column
vegetarian = []
for tag in tags:
    if(" 'vegetarian'" in tag):
        vegetarian.append(1)
    else:
        vegetarian.append(0)            
print(len(vegetarian))  

df_raw_recipes.insert(len(df_raw_recipes.columns), "vegetarian", vegetarian)
display(df_raw_recipes.head())
print(df_raw_recipes.info())

# comfort-food
comfort_food = []
for tag in tags:
    if(" 'comfort-food'" in tag):
        comfort_food.append(1)
    else:
        comfort_food.append(0)            
print(len(comfort_food)) 
df_raw_recipes.insert(len(df_raw_recipes.columns), "comfort_food", comfort_food)

# cuisines: japanese, spanish, english,mexican, midwestern,turkey, 
#indian, european, greek, chinese, thai, french, african,
#(north-american, american, northeastern-united-states, southwestern-united-states, american),
#asian, italian, canadian

l = ["indian", "japanese", "spanish", "english", "mexican", "turkey", 
     "italian", "chinese", "greek", "french", "african", "chinese", "thai"]

american = ["north-american", "american"]

cuisines = []
for tag in tags:
    cuisine = "";
    for item in tag:
        s = item.strip().strip("\'") 
        if s in l:
            cuisine = s
            break;
        if s in american:
            cuisine = "american"        
    cuisines.append(cuisine);

print(len(cuisines)) 

df_raw_recipes.insert(len(df_raw_recipes.columns), "cuisines", cuisines)
display(df_raw_recipes.head())

# keep the vaild recipes
ids = []
vaild_df = df_raw_recipes[df_raw_recipes.cuisines != ""]
for index in vaild_df['id']:
    ids.append(index);   
print(len(ids))

recipes = df_raw_recipes[df_raw_recipes.id.isin(ids)]
recipes.head();
display(recipes.info())

# keep the vaild recipes for ratings.csv
food_ratings = pd.read_csv('gdrive/My Drive/RAW_interactions.csv')
food_ratings = food_ratings[food_ratings.recipe_id.isin(ids)]
display(food_ratings.head())
print(food_ratings.info())

food_ratings = pd.read_csv('gdrive/My Drive/RAW_interactions_remove_empty_cuisine_type.csv',engine='python')
food_ratings.head()

# recipes = pd.read_csv('gdrive/My Drive/RAW_recipes_with_new_columns.csv')
# recipes.head()

user_ids = food_ratings.user_id.unique().tolist()
recipe_ids = food_ratings.recipe_id.unique().tolist()
print('Number of Ratings: {}'.format(len(recipes)))
print('Number of Users: {}'.format(len(user_ids)))
print('Number of Recipes: {}'.format(len(recipe_ids)))

recipes = recipes.dropna(subset=['cuisines'])

recipes.shape



# get number of ratings given by every user
df_users_cnt = pd.DataFrame(food_ratings.groupby('user_id').size(), columns=['count'])
df_users_cnt.head()

# filter unactive users
ratings_thres = 5
active_users = list(set(df_users_cnt.query('count >= @ratings_thres').index))
food_ratings_drop_users = food_ratings[food_ratings.user_id.isin(active_users)]
print('shape of original ratings data: ', food_ratings.shape)
print('shape of ratings data after dropping both unpopular recipes and inactive users: ', food_ratings_drop_users.shape)
user_ids = food_ratings_drop_users.user_id.unique().tolist()
recipe_ids = food_ratings_drop_users.recipe_id.unique().tolist()
print('Number of Ratings: {}'.format(len(food_ratings_drop_users)))
print('Number of Users: {}'.format(len(user_ids)))
print('Number of Recipes: {}'.format(len(recipe_ids)))

df_ratings_cnt = pd.DataFrame(food_ratings_drop_users.groupby('recipe_id').size(), columns=['count'])
df_ratings_cnt.head()

# filter data, remove unpopular recipes
popularity_thres = 5
popular_recipes = list(set(df_ratings_cnt.query('count >= @popularity_thres').index))

food_ratings_drop_recipes = food_ratings_drop_users[food_ratings_drop_users.recipe_id.isin(popular_recipes)]
food_ratings_drop_recipes
print('shape of original ratings data: ', food_ratings.shape)
print('shape of ratings data after dropping both unpopular recipes and inactive users: ', food_ratings_drop_users.shape)
user_ids = food_ratings_drop_recipes.user_id.unique().tolist()
recipe_ids = food_ratings_drop_recipes.recipe_id.unique().tolist()
print('Number of Ratings: {}'.format(len(food_ratings_drop_recipes)))
print('Number of Users: {}'.format(len(user_ids)))
print('Number of Recipes: {}'.format(len(recipe_ids)))

recipes = recipes[recipes.id.isin(food_ratings_drop_recipes.recipe_id.unique().tolist())]
recipes.groupby(['cuisines']).size().reset_index(name='counts')

# remove some recipes to make the distribution of cuisins column more balanced
recipes_counts = food_ratings_drop_recipes.loc[:,'recipe_id'].value_counts()

recipes_american = recipes[recipes.cuisines == 'american']
need_to_removed = []
for index, row in recipes_american.iterrows():
  rid = row["id"]
  if(recipes_counts[rid] <= 21):
     need_to_removed.append(rid)

print(len(need_to_removed))

food_ratings_drop_recipes = food_ratings_drop_recipes[~food_ratings_drop_recipes.recipe_id.isin(need_to_removed)]
user_ids = food_ratings_drop_recipes.user_id.unique().tolist()
recipe_ids = food_ratings_drop_recipes.recipe_id.unique().tolist()
print('Number of Ratings: {}'.format(len(food_ratings_drop_recipes)))
print('Number of Users: {}'.format(len(user_ids)))
print('Number of Recipes: {}'.format(len(recipe_ids)))

recipes = recipes[recipes.id.isin(food_ratings_drop_recipes.recipe_id.unique().tolist())]
recipes.groupby(['cuisines']).size().reset_index(name='counts')

"""### Add allergies columns"""

size = len(recipes)
dairy_flags = [0] * size
egg_flags = [0] * size
tree_nuts_flags = [0] * size
peanuts_flags = [0] * size
fish_flags = [0] * size
soya_flags = [0] * size
wheat_flags = [0] * size


dairy_buzzwords = ['cheese', 'cream']
peanuts_buzzwords = ["peanut"]
fish_buzzwords = [
        'anchovy', 'cod,' 'crab', 'fish', 'haddock', 'halibut',
        'oyster', 'perch', 'salmon', 'sardine', 'sea bass', 'shrimp', 'sole',
        'trout', 'tuna']

tree_nuts_buzzwords = []

wheat_buzzwords = [
        'bran', 'bread', 'bulgar', 'bun', 'couscous', 'cereal', 'cracker',
        'crouton', 'farina', 'flour', 'germ', 'gluten', 'malt', 'noodle',
        'pasta', 'seitan', 'semolina', 'soy sauce', 'starch', 'vermicelli', 'wheat',
        'whole grain'
    ]

ok_nuts = [
        'coconut', 'doughnuts', 'minute', 'nutmeg', 'nutritional',
        'water chestnuts']

index = 0
for ingredient in recipes.ingredients:
  #peanuts
  for buzzword in peanuts_buzzwords:
    if buzzword in ingredient:
      peanuts_flags[index] = 1
      break

  #fish
  for buzzword in fish_buzzwords:
     if buzzword in ingredient:
      fish_flags[index] = 1
      break
  if fish_flags[index] != 1 and "eel" in ingredient and "peel" not in ingredient:
     fish_flags[index] = 1  
  
  #wheat
  for buzzword in wheat_buzzwords:
    if buzzword in ingredient:
      wheat_flags[index] = 1
      break
  
  #egg
  if "egg" in ingredient and "eggplant" not in ingredient and "egg substitute" not in ingredient:
      egg_flags[index] = 1
  
  #dairy
  for buzzword in dairy_buzzwords:
    if buzzword in ingredient:
      dairy_flags[index] = 1
      break
  if "milk" in ingredient and "coconut" not in ingredient:
     dairy_flags[index] = 1

  #tree_nuts
  if "nut" in ingredient:
    findOk = False
    for nut in ok_nuts:
      if nut in ingredient:
        findOk = True
        break;
    if not findOk:
      tree_nuts_flags[index] = 1

  #soya
  if "soy" in ingredient:
    soya_flags[index] = 1

  index+=1

recipes.insert(len(recipes.columns), "dairy_allergic", dairy_flags)
recipes.insert(len(recipes.columns), "egg_allergic", egg_flags)
recipes.insert(len(recipes.columns), "soya_allergic", soya_flags)
recipes.insert(len(recipes.columns), "tree_nuts_allergic", tree_nuts_flags)
recipes.insert(len(recipes.columns), "wheat_allergic", wheat_flags)
recipes.insert(len(recipes.columns), "fish_allergic", fish_flags)
recipes.insert(len(recipes.columns), "peanuts_allergic", peanuts_flags)

recipes.head()

from google.colab import files

recipes.to_csv('recipes_less_data_v3.csv',index=False) 
files.download('recipes_less_data_v3.csv')

food_ratings_drop_recipes.to_csv('interactions_less_data_v3.csv',index=False) 
files.download('interactions_less_data_v3.csv')
