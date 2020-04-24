import pymongo 

client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client.recipes

users = db.user_collection
foods = db.food_collection
barcodes = db.barcode_collection
meats = db.meat_collection
vegets = db.vegets_collection

new_documents = [
  {
    "name": "Sun Bakery Trattoria",
    "stars": 4,
    "categories": ["Pizza","Pasta","Italian","Coffee","Sandwiches"]
  }, {
    "name": "Blue Bagels Grill",
    "stars": 3,
    "categories": ["Bagels","Cookies","Sandwiches"]
  }, {
    "name": "Hot Bakery Cafe",
    "stars": 4,
    "categories": ["Bakery","Cafe","Coffee","Dessert"]
  }, {
    "name": "XYZ Coffee Bar",
    "stars": 5,
    "categories": ["Coffee","Cafe","Bakery","Chocolates"]
  }, {
    "name": "456 Cookies Shop",
    "stars": 4,
    "categories": ["Bakery","Cookies","Cake","Coffee"]
  }
]

collection.insert_many(new_documents)

for res in collection.find():
    print(res)