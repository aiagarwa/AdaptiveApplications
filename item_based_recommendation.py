import pandas as pd
import os 
import ast
import matplotlib.pyplot as plt 
import pickle ### We will use pickleto save files for later access
from sklearn.metrics.pairwise import cosine_similarity ### Cosine Similary
from scipy import sparse
def preprocessing():
    interactions = pd.read_csv('interactions_less_data_v3.csv',engine='python')
    g = {'rating' : ['mean'],'user_id' : ['nunique']}
    int_summary = interactions.groupby(['recipe_id']).agg(g).reset_index()
    ind = pd.Index([e[0] + "_" +e[1] for e in int_summary.columns.tolist()])
    int_summary.columns = ind
    int_summary.columns = ['recipe_id', 'rating_mean', 'user_id_nunique']
    int_summary_94k = int_summary[ (int_summary['user_id_nunique'] > 1)]
    recipes = pd.read_csv('recipes_less_data_v3.csv', engine='python')
    filter_recipe = pd.merge(recipes,int_summary_94k,right_on = ['recipe_id'],left_on = ['id'],how = 'inner')
    return filter_recipe
def find_similar_dishes(list_names,data_similarity):
    dummy_data =  data_similarity[data_similarity['recipe1_name'] == list_names]
    dummy_data.sort_values(inplace = True,by =['similarity_rank']) 
    return dummy_data[:5]
def get_recommendation_recipe(dish_name):
    # filter_recipe = preprocessing()
    # df1 = pickle.load(open('similarities_sparse.pickle',"rb"))
    # data_similarity = df1.unstack().reset_index() 
    # data_similarity.columns = ['recipe1','recipe2','cosine_similarity']
    # #Filter out too high score as it is cosine similarity with itself and too low scores
    # data_similarity = data_similarity[data_similarity['cosine_similarity']<0.9999]
    # data_similarity = data_similarity[data_similarity['cosine_similarity']>0.6]
    # recipe_dict = {}
    # for j,i in enumerate(filter_recipe['name']):
    #     recipe_dict[j] = i
    # print ("Dictionary is created :")
    # data_similarity['recipe1_name'] = data_similarity['recipe1'].map(recipe_dict)
    # data_similarity['recipe2_name'] = data_similarity['recipe2'].map(recipe_dict)
    # print(data_similarity.head(5))
    # data_similarity['similarity_rank'] = data_similarity.groupby(['recipe1'])['cosine_similarity'].rank("dense", ascending=False)
    # data_similarity = data_similarity[data_similarity['similarity_rank'] <= 5].reset_index()
    # pickle.dump(data_similarity,open("data_similarity_recipe.pickle",'wb'))
    data_similarity = pickle.load(open('data_similarity_recipe.pickle','rb'))
    rec_dish = find_similar_dishes(dish_name,data_similarity=data_similarity)
    return rec_dish
def get_recommendation_nutrition(dish_name):
    # filter_recipe = preprocessing()
    # df1 = pickle.load(open('similarities_nutrition_sparse.pickle',"rb"))
    # data_similarity = df1.unstack().reset_index() 
    # data_similarity.columns = ['recipe1','recipe2','cosine_similarity']
    # #Filter out too high score as it is cosine similarity with itself and too low scores
    # data_similarity = data_similarity[data_similarity['cosine_similarity']<0.9999]
    # data_similarity = data_similarity[data_similarity['cosine_similarity']>0.6]
    # recipe_dict = {}
    # for j,i in enumerate(filter_recipe['name']):
    #     recipe_dict[j] = i
    # print ("Dictionary is created :")
    # data_similarity['recipe1_name'] = data_similarity['recipe1'].map(recipe_dict)
    # data_similarity['recipe2_name'] = data_similarity['recipe2'].map(recipe_dict)
    # print(data_similarity.head(5))
    # data_similarity['similarity_rank'] = data_similarity.groupby(['recipe1'])['cosine_similarity'].rank("dense", ascending=False)
    # data_similarity = data_similarity[data_similarity['similarity_rank'] <= 5].reset_index()
    # pickle.dump(data_similarity,open("data_similarity_nutrition.pickle",'wb'))
    data_similarity = pickle.load(open('data_similarity_nutrition.pickle','rb'))
    rec_dish = find_similar_dishes(dish_name,data_similarity=data_similarity)
    return rec_dish
def get_recommendation_ingredients(dish_name):
    # filter_recipe = preprocessing()
    # df1 = pickle.load(open('similarities_ingredients_sparse.pickle',"rb"))
    # data_similarity = df1.unstack().reset_index() 
    # data_similarity.columns = ['recipe1','recipe2','cosine_similarity']
    # #Filter out too high score as it is cosine similarity with itself and too low scores
    # data_similarity = data_similarity[data_similarity['cosine_similarity']<0.9999]
    # data_similarity = data_similarity[data_similarity['cosine_similarity']>0.6]
    # recipe_dict = {}
    # for j,i in enumerate(filter_recipe['name']):
    #     recipe_dict[j] = i
    # print ("Dictionary is created :")
    # data_similarity['recipe1_name'] = data_similarity['recipe1'].map(recipe_dict)
    # data_similarity['recipe2_name'] = data_similarity['recipe2'].map(recipe_dict)
    # print(data_similarity.head(5))
    # data_similarity['similarity_rank'] = data_similarity.groupby(['recipe1'])['cosine_similarity'].rank("dense", ascending=False)
    # data_similarity = data_similarity[data_similarity['similarity_rank'] <= 5].reset_index()
    # pickle.dump(data_similarity,open("data_similarity_ingredients.pickle",'wb'))
    data_similarity = pickle.load(open('data_similarity_ingredients.pickle','rb'))
    rec_dish = find_similar_dishes(dish_name,data_similarity=data_similarity)
    
    return rec_dish
def get_recommendation(recipe_name):
    rec_recipe = get_recommendation_recipe(recipe_name)
    rec_nutrition = get_recommendation_nutrition(recipe_name)
    rec_ingredients = get_recommendation_ingredients(recipe_name)
    final_dict = {}
    for item1 in rec_recipe['recipe2']:
        if item1 in rec_nutrition['recipe2'] or item1 in rec_ingredients['recipe2']:
            continue
        else:
            final_dict['recipe'] = item1
            break
    for item2 in rec_nutrition['recipe2']:
        if item2 in rec_recipe['recipe2'] or item2 in rec_ingredients['recipe2']:
            continue
        else:
            final_dict['nutrition'] = item2
            break
    for item3 in rec_ingredients['recipe2']:
        if item3 in rec_recipe['recipe2'] or item3 in rec_nutrition['recipe2']:
            continue
        else:
            final_dict['ingredients'] = item3
            break
    
    print(rec_recipe,rec_ingredients,rec_nutrition)
    return final_dict


if __name__ == '__main__':
    
    rec_dish = get_recommendation('aaloo mattar   indian style peas and potatoes')
    print(rec_dish)
    

