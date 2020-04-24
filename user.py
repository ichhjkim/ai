from flask import Flask, jsonify, request
from flask_restful import Resource
from .app import user_collection as users
import bcrypt

def verify_user(username, password):

    db_pw_check = users.find({"username": username})[0]["password"]

    hashed_pw = bcrypt.hashpw(password.encode('utf-8', db_pw_check))

    if not db_pw_check:
        print("user_not_found")
        return False
    
    elif hashed_pw == db_pw_check:
        return True

    
    else:
        print('password did not match')
        return False

def user_exists(username):

    user_check = users.find_ond({
        "username": username
    })
    if not user_check:
        return False
    else:
        return True
    
class Register(Resource):

    def post(self):
        posted_data = request.get_json()

        username = posted_data["username"]
        password = posted_data["password"]

        if user_exists(username):
            res = {
                "status": 201
                "data": "이미 존재하는 유저입니다"
            }
            return jsonify(res)
        
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert({
            "username": username,
            "password": password,
            "ingredients": {}
        })

        res = {
            "status": 200,
            "data": "회원가입이 성공적으로 이루어졌습니다."
        }
        
        return jsonify(res)

class add_ingredient(Resource):

    def post(self):

        ingredient_datas = request.get_json()
        username = ingredient_datas["username"]
        new_ingredients = ingredient_datas["ingredients"]

        exist_ingredients = users.find({"username": username})[0]["ingredients"]
        
        for k, v in new_ingredients.items():

            t = exist_ingredients.get(k)
            if t:
                exist_ingredients[k] += new_ingredients[k]
            else:
                exist_ingredients[k] = new_ingredients[k]

        users.update({
            {"username": username},
            {"$set": {
                "ingredients": exist_ingredients
            }}
        })

        res = {
            "status": 200,
            "data": "재료가 성공적으로 저장되었습니다."
        }
        return jsonify(res)

class user_ingredients(Resource):

    def get(self):

        posted_data = request.get_json()

        username = posted_data["username"]

        get_user = users.find({
            "username": username
        })[0]["ingredients"]
        
        res = {
            "status": 200,
            "data": str(get_user)
        }

        return jsonify(res)


        

