import pymongo 

client = pymongo.MongoClient()
db = client.recipes

# accounts
account_collection = db.account_collection
# food
food_collection = db.food_collection
