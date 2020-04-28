import pymongo 

import csv, json
import re

client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client.recipes

users = db.user_collection
foods = db.food_collection
ingredients = db.ingredient_collection

with open('recipes.json') as f:
    recipes = json.load(f)

f = open('food.csv', 'r', encoding='cp949')
fds = csv.reader(f) 
all_things = {}
next(fds)

for fd in fds:
    all_things[fd[1]] = fd[-2]
igs = {}

for recipe_k, recipe_v in recipes.items():
    result = {}
    result['name'] =  recipe_v['name']
    result['description'] =  recipe_v['description']
    result['type'] = recipe_v['type']
    result['food_type'] = recipe_v['foodType']
    result['time'] = recipe_v['time']
    result['kcal'] = recipe_v['kcal']
    result['person'] = recipe_v['person']
    result['level'] = recipe_v['level']

    result['all_ingredients'] = recipe_v['ingredients']
    for ig_k, ig_v in recipes[recipe_k]['ingredients'].items():
        if not igs.get(ig_k):
            igs[ig_k] = ig_v[1]
            r = {}
            r['name'] = ig_k
            r['image'] = ig_v[1]
            ingredients.insert_one(r)

    result['image'] = all_things[recipe_v['name']]
    result['process'] = recipe_v['process']
    #print(result)
    foods.insert_one(result)