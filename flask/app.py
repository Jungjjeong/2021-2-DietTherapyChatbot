from flask import Flask, json, request, jsonify
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient
from fractions import Fraction

app = Flask(__name__)

cluster = MongoClient("mongodb+srv://user:0000@cluster0.uio0y.mongodb.net/myFirstDatabase?retryWrites=true&w=majority") # DB연결
db = cluster["DietTherapy"]
음식영양성분 = db["음식영양성분"]
음식섭취양 = db["음식섭취양"]

food_name = ""

@app.route("/")
def hello():
    return "Chatbot server"

# 사진 전송 요구 + 사진 클라우드 링크 받아오는 함수 
@app.route("/getPhoto", methods = ["GET", "POST"]) 
def start():
    print("start func")
    req = request.get_json()

    print(req)

    photo_type3 =  req["action"]["detailParams"]["사진전송"]["value"]
    photo_json = json.loads(photo_type3)
    print('3',photo_type3)

    print(photo_json["secureUrls"])

    res = {
        "version" : "2.0",
        "template":{
            "outputs": [
                {
                    "simpleText": {
                        "text" : "사진 전송이 완료되었습니다.\n\n '인식된 음식'의 드신 양을 입력해 주세요."
                    }
                }
            ],
        }
    }

    return jsonify(res)

# 음식 엔티티 연동 + 섭취양 불러와서 quickReplies
@app.route("/food",methods = ["GET","POST"])
def food():
    global food_name

    print("음식 엔티티 연동 + 디비에서 섭취양 불러오기")
    req = request.get_json()
    print(req)

    food_type = req["action"]["detailParams"]["음식"]["value"]
    print(food_type)

    dbResult = str(음식섭취양.find_one({"음식종류" : food_type},{"_id" : False, "음식종류" : False})).split("'")

    answer = food_type + "을(를) 드신 양을 골라주세요."
    answer1 = dbResult[3] + dbResult[15]
    answer2 = dbResult[7] + dbResult[15]
    answer3 = dbResult[11] + dbResult[15]
    print(answer1)
    print(answer2)
    print(answer3) 

    res = {
        "version" : "2.0",
        "template": {
            "outputs" : [
                {
                    "simpleText" : {
                        "text": answer
                    }
                }
            ],
            "quickReplies": [
                {
                    "messageText" : "선택1",
                    "action": "message",
                    "label" : answer1
                },{
                    "messageText" : "선택2",
                    "action": "message",
                    "label" : answer2
                },{
                    "messageText" : "선택3",
                    "action": "message",
                    "label" : answer3
                },{
                    "messageText" : "기타",
                    "action": "message",
                    "label" : "기타"
                }
            ]
        }
    }

    food_name = food_type
    return jsonify(res)

# 칼로리 계산 및 엑셀 출력 
@app.route("/calorie", methods = ["GET", "POST"]) 
def calorie():
    global food_name

    req = request.get_json()

    select = req["action"]["detailParams"]["선택지"]["value"]
    print(select)

    user_id = req["userRequest"]["user"]["id"]
    print(user_id)

    food_detail = str(음식영양성분.find_one({"음식종류" : food_name},{"_id" : False, "음식종류" : False})).replace(':','').replace(',','').replace('}','').split("'")
    print(food_detail)
    food_amount = str(음식섭취양.find_one({"음식종류" : food_name},{"_id" : False, "음식종류" : False})).split("'")
    print(food_amount)

    if select == '선택1':
        task1 = Fraction(food_amount[3])
        task2 = Fraction(food_amount[7])
        print(task1)

        calorie = round(float(food_detail[2]) / task2 * task1, 2) #칼로리(kcal)
        sodium = round(float(food_detail[10]) / task2 * task1, 2) #나트륨(mg)
        carbohydrate = round(float(food_detail[4]) / task2 * task1, 2) #탄수화물(g)
        protein = round(float(food_detail[6]) / task2 * task1, 2) #단백질(g)
        fat = round(float(food_detail[8]) / task2 * task1, 2) #지방(g)
        kal = round(float(food_detail[12]) / task2 * task1, 2) #칼슘
        vC = round(float(food_detail[14]) / task2 * task1, 2) #비타민 C
        saturatedFat = round(float(food_detail[16]) / task2 * task1, 2) #포화지방산

    elif select == '선택2' :
        task2 = Fraction(food_amount[7])
        print(task2)

        calorie = food_detail[2] #칼로리(kcal)
        sodium = food_detail[10] #나트륨(mg)
        carbohydrate = food_detail[4] #탄수화물(g)
        protein = food_detail[6] #단백질(g)
        fat = food_detail[8] #지방(g)
        kal = food_detail[12] #칼슘
        vC = food_detail[14] #비타민 C
        saturatedFat = food_detail[16] #포화지방산

    elif select == '선택3' :
        task3 = Fraction(food_amount[11])
        task2 = Fraction(food_amount[7])
        print(task3)

        calorie = round(float(food_detail[2]) / task2 * task3, 2) #칼로리(kcal)
        sodium = round(float(food_detail[10]) / task2 * task3, 2)# 나트륨(mg)
        carbohydrate = round(float(food_detail[4]) / task2 * task3, 2) #탄수화물(g)
        protein = round(float(food_detail[6]) / task2 * task3, 2) #단백질(g)
        fat = round(float(food_detail[8]) / task2 * task3, 2) #지방(g)
        kal = round(float(food_detail[12]) / task2 * task3, 2) #칼슘
        vC = round(float(food_detail[14]) / task2 * task3, 2) #비타민 C
        saturatedFat = round(float(food_detail[16]) / task2 * task3, 2) #포화지방산

    calculate = [calorie, sodium, carbohydrate, protein, fat, kal, vC, saturatedFat]

    
    print("음식 :" , calculate)
    
    answer = "섭취한 음식의 정보입니다. \n\n칼로리 : " + str(calculate[0]) + "kcal\n나트륨 : " + str(calculate[1]) + "mg\n탄수화물 : " + str(calculate[2]) + "g\n단백질 : " + str(calculate[3]) + "g\n지방 : " + str(calculate[4]) + "g\n칼슘 : " + str(calculate[5]) + "g\n비타민C : " + str(calculate[6]) + "g\n포화지방산 : " + str(calculate[7]) + " g\n\n다음 음식은 무엇을 드셨나요?\n없다면 [종료]를 입력해주세요."

    to_excel(user_id, calculate)

    res = {
        "version" : "2.0",
        "template":{
            "outputs": [
                {
                    "simpleText": {
                        "text" : answer
                    }
                }
            ],"quickReplies": [
                {
                    "messageText" : "종료",
                    "action": "message",
                    "label" : "🏠종료"
                }
            ]
        }
    }

    return jsonify(res)





@app.route("/test", methods = ["GET","POST"])
def test():
    print("test func")

    res = {
        "version" : "2.0",
        "template":{
            "outputs": [
                {
                    "simpleText": {
                        "text" : "server response"
                    }
                }
            ]
        }
    }

    return jsonify(res)


def to_excel(user_id, food_calculate):
    df = None

    now = str(datetime.now())

    try:
        df = pd.read_excel("./data/" + user_id + ".xlsx", engine='openpyxl')
    except Exception as e:
        df = pd.DataFrame(columns = ["날짜 시간","음식","calorie","sodium","carbonhydrate","protein","fat","calcium", "vitamin C", "saturated Fat"])
    
    new_data = {
        "날짜 시간" : now,
        "음식" : food_name,
        "calorie" : food_calculate[0],
        "sodium" : food_calculate[1],
        "carbonhydrate" : food_calculate[2],
        "protein" : food_calculate[3],
        "fat" : food_calculate[4],
        "calcium" : food_calculate[5],
        "vitamin C" : food_calculate[6],
        "saturated Fat" : food_calculate[7]
    }

    df = df.append(new_data, ignore_index=True)
    df.to_excel("./data/" + user_id +".xlsx", index=False)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, threaded = True)