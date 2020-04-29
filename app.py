import os
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
import datetime
import pymongo 

from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt_claims
from flask_bcrypt import Bcrypt

import uuid
import base64
import json
from bson.json_util import dumps
from bson.json_util import loads
import ast

from decouple import config
import itertools

app = Flask(__name__)
CORS(app)

secret_key = b'@\xb8\xc0\x11\x95\xa9d)\xd4s\xad9\t\xdb\xea"'
app.config['SECRET_KEY'] = secret_key

# 암호
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client.recipes

users = db.user_collection
foods = db.food_collection
ingredient_collection = db.ingredient_collection

# 유저 정보 가입, 조회, 삭제, 비밀번호 변경

@app.route('/accounts', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def user():
    
    if request.method == 'GET':
        query = request.args.get('username')
        print(query)
        data = users.find_one({
            "username": query
        }, {"_id":0, "password":0})
        print(data)
        
        if data:
            data = loads(dumps(data, ensure_ascii=False))
            res = {
                'status': 200,
                'data': data
            }
        else:
            res = {
                'status': 200,
                'data': "존재하지 않는 유저입니다"
            }
        return jsonify(res)
    
    if request.method == 'POST':
        data = request.get_json()
        if data.get('username') and data.get('password') and data.get('email'):

            username = data.get('username')
            user_email = data.get('email')

            db_check = users.find_one({
                "username": username
            },{"_id":0})
            db_email_check = users.find_one({
                "email": user_email
            }, {"_id":0})

            if db_check or db_email_check:
                print(db_check)
                print(db_email_check)
                return jsonify({ "status": 200, "data": "이미 존재하는 유저가 있습니다"})

            pw = data.get('password')
            pw_hash = bcrypt.generate_password_hash(pw)

            user = {
                "username": username,
                "password": pw_hash,
                "email": user_email,
                "ingredients": {}
            }
            
            users.insert_one(user)
            expires = datetime.timedelta(days=14)
            access_token = create_access_token(identity=username, expires_delta=expires)

            return jsonify({
                'status': 200,
                'data': '회원가입이 성공적으로 완료되었습니다',
                'token': access_token
            })
            
        else:
            return jsonify({
                'status': 400,
                'data': '입력되지 않은 값이 있습니다'
            })
    
    if request.method == 'DELETE':

        data = request.args.get('username')
        if data:

            db_res = users.delete_one({'username': data})
            print(db_res, '=========')
            if db_res:
                res = {
                    'status': 200,
                    'data': '회원이 성공적으로 삭제되었습니다'
                }
            else:
                res = {
                    'status': 200,
                    'data': '해당 이메일을 가진 회원은 존재하지 않습니다'
                }
            return jsonify(res)
    

        else:
            return jsonify({
                'status': 400,
                'data': '입력되지 않은 값이 있습니다'
            })
    
    if request.method == 'PATCH':

        data = request.get_json()

        if data.get('username') and data.get('password'):
            
            pw = data.get('password')
            pw = bcrypt.generate_password_hash(pw)

            db_res = users.update(
                {"username": data.get('username')},
                {'$set': {"password": pw}}
            )
            if db_res:
                return jsonify({
                    'status': 200,
                    'data': '비밀번호 변경 완료'
                })
            else:
                return jsonify({
                    'status':400,
                    'data': '존재하지 않는 회원입니다'
                })
        
        else:
            return jsonify({
                'status': 200,
                'data': '입력하신 값을 확인하세요'
            })


# 재료 추가, 삭제
@app.route('/ingredient', methods=["POST", "DELETE"])
@jwt_required
def ingredient_manage():
        
    if request.method == 'POST':

        req = request.get_json()
        username = req.get('username')
        new_ingredients = req.get('ingredients')
        way = new_ingredients.get('way')

        exist_ingredients = users.find_one({"username": username}).get("ingredients")

        if not exist_ingredients: exist_ingredients = {}
        #else: exist_ingredients = json.loads(exist_ingredients.replace("'", "\""))

        if way == 'image':

            temp = request.args['image']
            img = temp.base64.b64decode(temp)
            img = img.decode('ascii')

            # 텐서플로우 이미지 분석 결과
            pass
        
        elif way == 'barcode':

            ds = new_ingredients.get('datas')
            
            for k, v in ds.items():
                print(k, v)
                t = exist_ingredients.get(k)
                if not t: 
                    ig = ingredient_collection.find_one({"name":k},{"_id":0}).get('image')
                    if ig:exist_ingredients[k] = ig
                    else:exist_ingredients[k] = 1

            users.find_and_modify(
                query={"username": username},
                update={"$set": {"ingredients": exist_ingredients}}
            )
            result = users.find_one({
            "username": username
            },{"_id":0}).get('ingredients')

            res = {
                "status": 200,
                "data": result
            }
            return jsonify(res)

        
        elif way == "text":
            ds = new_ingredients.get('datas')
            
            for k, v in ds.items():
                print(k, v)
                t = exist_ingredients.get(k)
                if not t: 
                    ig = ingredient_collection.find_one({"name":k},{"_id":0}).get('image')
                    if ig:exist_ingredients[k] = ig
                    else:exist_ingredients[k] = 1

            users.find_and_modify(
                query={"username": username},
                update={"$set": {"ingredients": exist_ingredients}}
            )
            result = users.find_one({
            "username": username
            },{"_id":0}).get('ingredients')

            res = {
                "status": 200,
                "data": result
            }
            return jsonify(res)
    
    if request.method == 'DELETE':
        
        req = request.args
        username = req.get('username')
        user_ingredients = json.loads(req.get('ingredients'))

        exist_ingredients = users.find_one({"username": username})["ingredients"]

        for k, v in user_ingredients.items():
            t = exist_ingredients.get(k)
            if t:
                a = exist_ingredients.pop(k)
                print(a)
                
        
        users.find_and_modify(
            query={"username": username},
            update={"$set": {"ingredients": exist_ingredients}}
        )
        result = users.find_one({
            "username": username
        },{"_id":0}).get('ingredients')
        res = {
            "status": 200,
            "data": result
        }
        return jsonify(res)

# session
@app.route('/user_session')
def user_session():
    if 'username' in session:
        return jsonify({
            "status": 200,
            "data": '로그인 되어 있음'
        })
    return jsonify({
        "status": 200,
        "data": "로그인 안되어있음"
    })

# 로그인
@app.route('/login', methods=["POST", "GET"])
def user_login():
    print(request)
    if request.method == 'POST':

        req = request.get_json()
        username = req.get('username')
        password = req.get('password')

        db_check = users.find_one({'username': username})
        if db_check:
            check_pw = bcrypt.check_password_hash(db_check.get("password"), password)
    
            if db_check and check_pw:
                expires = datetime.timedelta(days=14)
                access_token = create_access_token(identity=username, expires_delta=expires)
                
                return jsonify({
                    "status": 200,
                    "data": "로그인 성공",
                    "access_token": access_token
                })
        
    return jsonify({ "status": 200, "data": "로그인 실패"})


@app.route('/get_username', methods=['GET'])
@jwt_required
def get_username():
    current_user = get_jwt_identity()
    return jsonify(name=current_user), 200

"""
http://localhost:5000/protected header에 아래 추가 Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NTI4MTY5ODEsIm5iZiI6MTU1MjgxNjk4MSwianRpIjoiMGE3ODQ5OGEtY2ZiZS00OWEzLTkxMDktODdjZDNlMjU4ZmIyIiwiZXhwIjoxNTUyODE3ODgxLCJpZGVudGl0eSI6InRlc3QiLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MiLCJ1c2VyX2NsYWltcyI6eyJoZWxsbyI6InRlc3QiLCJmb28iOlsiYmFyIiwiYmF6Il19fQ.mywM-1FEQ1Cv5APcn8saUUbF5z1LIK4gipB-6N2yUJo

출처: https://fenderist.tistory.com/142 [Devman]
"""

@app.route('/image', methods=['GET'])
@jwt_required
def decode_image():
    temp = request.args['image']
    img = temp.base64.b64decode(temp)
    img = img.decode('ascii')


@app.route('/recipes', methods=["GET"])
def get_recipes():

    ingredients = request.args.get('ingredients')
    ingredients = json.loads(ingredients)

    ingredients_length = len(ingredients.keys())
    result = []
    for i in range(ingredients_length, 0, -1):
        combination_ingredients = itertools.combinations(ingredients.keys(), i)
        for combination_ingredient in combination_ingredients:
            search_ingredients = []
            for k in combination_ingredient:
                if not k: continue
                new = {}
                temp = "all_ingredients."+k
                new[temp] = {"$exists": True }
                search_ingredients.append(new)
            else:
                all_recipes = foods.find({ "$and" : search_ingredients},{"_id":0, "process":0, "all_ingredients":0} ).limit(15)
                all_recipes = loads(dumps(all_recipes, ensure_ascii=False))
                for all_recipe in all_recipes:
                    if all_recipe not in result: result.append(all_recipe)
                    if len(result) >= 15:
                        return jsonify({
                                "status": 200,
                                "data": result
                            })
                    
    return jsonify({
        "status": 200,
        "data": result
    })


@app.route('/recipes_detail', methods=["GET"])
def recipe_detail():
    recipe_name = request.args.get('name')
    data = foods.find_one({"name": recipe_name}, {"_id":0})
    res = {
        "status": 200,
        "data": data
    }
    return jsonify(res)

@app.route('/all_recipes', methods=["GET"])
def all_recipes():

    datas = foods.find({},{"_id":0, "process":0, "all_ingredients":0})
    datas = loads(dumps(datas, ensure_ascii=False))
    print(datas)
    return jsonify({
        "status": 200,
        "data": datas
    })


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

@app.route('/user_image', methods=['GET'])
def user_image():

    username = request.args.get('username')