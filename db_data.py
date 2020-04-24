import pymongo 

import csv, json
import re

client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client.recipes

users = db.user_collection
foods = db.food_collection
barcodes = db.barcode_collection
meats = db.meat_collection
vegets = db.vegets_collection

#users.insert(new_user)
#foods.insert(new_food)

recipe = {
    "name": "",
    "image": "",
    "manual01": "",
    "manual01_img": "",
    "manual02": "",
    "manual02_img" : "",
    "manual03": "",
    "manual03_img": "",
    "manual04": "",
    "manual04_img": "",
    "manual05": "",
    "manual05_img": "",
    "manual06": "",
    "manual06_img": "",
    "manual07": "",
    "manual07_img": "",
    "manual08": "",
    "manual08_img": "",
    "manual09": "",
    "manual09_img": "",
    "manual10": "",
    "manual10_img": "",
    "manual11": "",
    "manual11_img": "",
    "manual12": "",
    "manual12_img": "",
    "manual13": "",
    "manual13_img": "",
    "manual14": "",
    "manual14_img": "",
    "manual15": "",
    "manual15_img": "",
    "manual16": "",
    "manual16_img": "",
    "manual17": "",
    "manual17_img": "",
    "manual18": "",
    "manual18_img": "",
    "manual19": "",
    "manual19_img": "",
    "manual20": "",
    "manual20_img": "",
    "main_ingredient": {},
    "condiment": {},
    "essential_ingredient": {},
    "omittable_ingredient": {},
    "all_ingredients": {},
    "kcal": "",
    "car": "",
    "pro": "",
    "nat": "",
    "fat": "",
    "field": ""
}

with open('recipe.json', 'r', encoding='UTF-8-sig') as j:
    json_data = json.load(j)
    datas = json_data.get("COOKRCP01").get("row")
    for d in datas:
        recipe = {
                    "name": "",
                    "image": "",
                    "manual01": "",
                    "manual01_img": "",
                    "manual02": "",
                    "manual02_img" : "",
                    "manual03": "",
                    "manual03_img": "",
                    "manual04": "",
                    "manual04_img": "",
                    "manual05": "",
                    "manual05_img": "",
                    "manual06": "",
                    "manual06_img": "",
                    "manual07": "",
                    "manual07_img": "",
                    "manual08": "",
                    "manual08_img": "",
                    "manual09": "",
                    "manual09_img": "",
                    "manual10": "",
                    "manual10_img": "",
                    "manual11": "",
                    "manual11_img": "",
                    "manual12": "",
                    "manual12_img": "",
                    "manual13": "",
                    "manual13_img": "",
                    "manual14": "",
                    "manual14_img": "",
                    "manual15": "",
                    "manual15_img": "",
                    "manual16": "",
                    "manual16_img": "",
                    "manual17": "",
                    "manual17_img": "",
                    "manual18": "",
                    "manual18_img": "",
                    "manual19": "",
                    "manual19_img": "",
                    "manual20": "",
                    "manual20_img": "",
                    "main_ingredient": {},
                    "condiment": {},
                    "essential_ingredient": {},
                    "omittable_ingredient": {},
                    "all_ingredients": {},
                    "kcal": "",
                    "car": "",
                    "pro": "",
                    "nat": "",
                    "fat": "",
                    "field": ""
                }

        recipe['name'] = d['RCP_NM']
        recipe['image'] = d["ATT_FILE_NO_MAIN"]
        recipe["manual01"] = d["MANUAL01"]
        recipe["manual01_img"] = d["MANUAL_IMG01"]
        recipe["manual02"] = d["MANUAL02"]
        recipe["manual02_img"] = d["MANUAL_IMG02"]
        recipe["manual03"] = d["MANUAL03"]
        recipe["manual03_img"] = d["MANUAL_IMG03"]
        recipe["manual04"] = d["MANUAL04"]
        recipe["manual04_img"] = d["MANUAL_IMG04"]
        recipe["manual05"] = d["MANUAL05"]
        recipe["manual05_img"] = d["MANUAL_IMG05"]
        recipe["manual06"] = d["MANUAL06"]
        recipe["manual06_img"] = d["MANUAL_IMG06"]
        recipe["manual07"] = d["MANUAL07"]
        recipe["manual07_img"] = d["MANUAL_IMG07"]
        recipe["manual08"] = d["MANUAL08"]
        recipe["manual08_img"] = d["MANUAL_IMG08"]
        recipe["manual09"] = d["MANUAL09"]
        recipe["manual09_img"] = d["MANUAL_IMG09"]
        recipe["manual10"] = d["MANUAL10"]
        recipe["manual10_img"] = d["MANUAL_IMG10"]
        recipe["manual11"] = d["MANUAL11"]
        recipe["manual11_img"] = d["MANUAL_IMG11"]
        recipe["manual12"] = d["MANUAL12"]
        recipe["manual12_img"] = d["MANUAL_IMG12"]
        recipe["manual13"] = d["MANUAL13"]
        recipe["manual13_img"] = d["MANUAL_IMG13"]
        recipe["manual14"] = d["MANUAL14"]
        recipe["manual14_img"] = d["MANUAL_IMG14"]
        recipe["manual15"] = d["MANUAL15"]
        recipe["manual15_img"] = d["MANUAL_IMG15"]
        recipe["manual16"] = d["MANUAL16"]
        recipe["manual16_img"] = d["MANUAL_IMG16"]
        recipe["manual17"] = d["MANUAL17"]
        recipe["manual17_img"] = d["MANUAL_IMG17"]
        recipe["manual18"] = d["MANUAL18"]
        recipe["manual18_img"] = d["MANUAL_IMG18"]
        recipe["manual19"] = d["MANUAL19"]
        recipe["manual19_img"] = d["MANUAL_IMG19"]
        recipe["manual20"] = d["MANUAL20"]
        recipe["manual20_img"] = d["MANUAL_IMG20"]

        igs = d["MAIN_INGREDIENT"].split(',')

        for ig in igs:
            ig = ig.split('|')
            ig_name = ig[0]
            if len(ig) > 1:
                ig_q = ig[1]
            else:
                ig_q = 1
            recipe["main_ingredient"][ig_name] = ig_q

        cds = d["CONDIMENT"].split(',')
        for cd in cds:
            cd = cd.split('|')
            cd_name = cd[0]
            if len(cd) > 1:
                cd_q = cd[1]
            else:
                cd_q = 1
            recipe["condiment"][cd_name] = cd_q
        
        ess = d["ESSENTIAL_INGREDIENT"].split(',')
        for es in ess:
            es = es.split('|')
            es_name = es[0]
            if len(es) > 1:
                es_q = es[1]
            else:
                es_q = 1
            recipe["essential_ingredient"][es_name] = es_q

        if not d["OMITTABLE_INGREDIENT"]:
            oms = d["OMITTABLE_INGREDIENT"].split(',')
            for om in oms:
                om = om.split('|')
                om_name = om[0]
                if len(om) > 1:
                    om_q = om[1]
                else:
                    om_q = 1
                recipe["omittable_ingredient"][om_name] = om_q

        alls = d["RCP_PARTS_DTLS"].replace('\n', ',')
        alls = alls.split(',')
        for al in alls:
            al = al.split(' ')
            if len(al) > 1:
                if '재료' in al[0] or recipe['name'] in al[0]: 
                    if len(al) == 2:
                        al_name=al[-1]
                        al_q = 1
                    else:
                        al_name = al[1:-1][0]
                        al_q = al[-1]
                else:
                    al_name = al[:-1][0]
                    al_q = al[-1]
            else:
                al_name = al[0]
                al_q = 1
            recipe["all_ingredients"][al_name] = al_q
        
        recipe["kcal"] = d["INFO_ENG"]
        recipe["car"] = d["INFO_CAR"]
        recipe["pro"] = d["INFO_PRO"]
        recipe["nat"] = d['INFO_NA']
        recipe["fat"] = d['INFO_FAT']
        recipe["field"] = d["RCP_PAT2"]
        foods.insert_one(recipe)


f = open('barcode.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
for r in rdr:
    if not r[1]:
        r[1] = r[2]
    barcode = {
        "number": r[0],
        "product_name": r[1],
        "field": r[3],
        "food_type": r[4]
    }
    barcodes.insert_one(barcode)
