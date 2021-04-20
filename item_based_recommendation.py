import pandas as pd
import os 
import ast
import matplotlib.pyplot as plt 
import pickle ### We will use pickleto save files for later access
from sklearn.metrics.pairwise import cosine_similarity ### Cosine Similary
from scipy import sparse
def filter_recipes(recipes, filtering=[], allergies =[]):
  filterRecipes = recipes
  if len(filtering) == 0 and len(allergies) == 0:
    return filterRecipes
  for f in filtering:
    if f == "vegetarian":
      filterRecipes = filterRecipes[filterRecipes["vegetarian"] == 1]
    elif f.startswith("cooking_time_less_than"):
      mins = int(f.split("_")[-1])
      filterRecipes = filterRecipes[filterRecipes["minutes"] <= mins]
      
  for allergy in allergies:
    filterRecipes = filterRecipes[filterRecipes[allergy + "_allergic"] == 0]

  return filterRecipes

def preprocessing(filtering,allergies):
    recipes = pd.read_csv('recipes_less_data_v3.csv', engine='python')
    filter_recipes = filter_recipes(recipes,filtering=filtering, allergies=allergies)
    return filter_recipes
def find_similar_dishes(list_names,data_similarity):
    dummy_data =  data_similarity[data_similarity['recipe1_name'] == list_names]
    dummy_data.sort_values(inplace = True,by =['similarity_rank']) 
    return dummy_data[:20]
def get_recommendation_recipe(dish_name,filtering,allergies):
    recipes = pd.read_csv('recipes_less_data_v3.csv', engine='python')
    data_similarity = pickle.load(open('data_similarity_recipe.pickle','rb'))
    rec_dish = find_similar_dishes(dish_name,data_similarity=data_similarity)
    new_rec = pd.DataFrame()
    for i in rec_dish["recipe2_name"]:
        j = recipes[recipes["name"]==i]
        new_rec = new_rec.append(j)
    items = filter_recipes(recipes=new_rec,filtering=filtering ,allergies=allergies)
    print('item',items)
    return items
def get_recommendation_nutrition(dish_name,filtering,allergies):
    recipes = pd.read_csv('recipes_less_data_v3.csv', engine='python')
    data_similarity = pickle.load(open('data_similarity_nutrition.pickle','rb'))
    rec_dish = find_similar_dishes(dish_name,data_similarity=data_similarity)
    new_rec = pd.DataFrame()
    for i in rec_dish["recipe2_name"]:
        j = recipes[recipes["name"]==i]
        new_rec = new_rec.append(j)
    items = filter_recipes(recipes=new_rec,filtering=filtering ,allergies=allergies)
    return items
def get_recommendation_ingredients(dish_name,filtering,allergies):
    recipes = pd.read_csv('recipes_less_data_v3.csv', engine='python')
    data_similarity = pickle.load(open('data_similarity_ingredients.pickle','rb'))
    rec_dish = find_similar_dishes(dish_name,data_similarity=data_similarity)
    new_rec = pd.DataFrame()
    for i in rec_dish["recipe2_name"]:
        j = recipes[recipes["name"]==i]
        new_rec = new_rec.append(j)
    items = filter_recipes(recipes=new_rec,filtering=filtering ,allergies=allergies)
    return items
def get_recommendation(recipe_name,filtering,allergies):
    rec_recipe = get_recommendation_recipe(recipe_name,filtering,allergies)
    rec_nutrition = get_recommendation_nutrition(recipe_name,filtering,allergies)
    rec_ingredients = get_recommendation_ingredients(recipe_name,filtering,allergies)
    final_dict = {}
    print(rec_recipe)
    for item1 in rec_recipe['id']:
        if item1 in rec_nutrition['id'] or item1 in rec_ingredients['id']:
            continue
        else:
            final_dict['recipe'] = item1
            break
    for item2 in rec_nutrition['id']:
        if item2 in rec_recipe['id'] or item2 in rec_ingredients['id']:
            continue
        else:
            final_dict['nutrition'] = item2
            break
    for item3 in rec_ingredients['id']:
        if item3 in rec_recipe['id'] or item3 in rec_nutrition['id']:
            continue
        else:
            final_dict['ingredients'] = item3
            break
    return final_dict


if __name__ == '__main__':
    rec_dish = get_recommendation('aaloo mattar   indian style peas and potatoes',[],[])
    print(rec_dish)
    

