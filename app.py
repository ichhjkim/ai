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

from YOLOAI.YOLO_image import YOLO

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
            temp_img = "data:image/jpeg;base64,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"
            #temp = request.args['image']
            img = temp.base64.b64decode(temp)
            img = img.decode('ascii')
            
            # 텐서플로우 이미지 분석 결과
            filename = 'user_photo.jpg'
            img_data = base64.b64decode(temp_img)
            with open(filename, 'wb') as f:
                f.write(img_data)
                print('파일이 저장되었습니다')
            
            result = YOLO(img)
        
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