from flask import Flask, json, request, jsonify
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.core.indexes.api import get_objs_combined_axis
from pymongo import MongoClient
from fractions import Fraction
import re


from user import SurveyUser
app = Flask(__name__)

cluster = MongoClient("mongodb+srv://user:0000@cluster0.uio0y.mongodb.net/myFirstDatabase?retryWrites=true&w=majority") # DB연결
db = cluster["DietTherapy"]
음식영양성분 = db["음식영양성분"]
음식섭취양 = db["음식섭취양"]
식이빈도조사_음식섭취양 = db["식이빈도조사_음식섭취양"]
식이빈도조사_단위영양성분 = db["식이빈도조사_단위영양성분"]
user_dict = {} # SurveyUser 객체가 들어감. 

food_name = ""
user_name = ""
age = 0
gender = ""
height = 0
weight = 0
exercise = ""
exerciseTime = ""
exerciseNum = ""
nutriSupplement = ""
nutriIntake = ""
foodFrequency = []
foodEntity = []
foodArr = []



solution_칼로리 = 0
solution_탄수화물 = 0
solution_단백질 = 0
solution_지방 = 0
solution_나트륨 = 0
solution_비타민C = 0
solution_포화지방산 = 0
solution_칼슘 = 0

solutionResultText = ""

@app.route("/")
def hello():
    return "Chatbot server"

#------------------------------------------------------------------------1년 솔루션(서울대)------------------------------------------------------------------------#

@app.route("/getUserName", methods = ["GET", "POST"]) 
def getUserName():
    print("이름 정보 받는 함수")

    req = request.get_json()

    print(req)

    user_id = req["userRequest"]["user"]["id"]
    user_name =  req["action"]["detailParams"]["userName"]["value"] 

    user = SurveyUser(user_id, user_name)
    user_dict[user_id] = user

    res = {
        "version" : "2.0",
        "template":{
            "outputs": [
                {
                    "simpleText": {
                        "text" : "입력하신 이름은 " + user_dict[user_id].user_name + "입니다. 😊\n\n사용자님의 나이를 입력해 주세요. \nex) 24세"
                    }
                }
            ]
        }
    }
    print(user_dict)
    return jsonify(res)


@app.route("/getAge", methods = ["GET", "POST"]) 
def getAge():

    global age
    req = request.get_json()

    print(req)

    user_id = req["userRequest"]["user"]["id"]
    ageReq =  req["action"]["detailParams"]["sys_number_age"]["origin"] #나이 **세
    age = int(ageReq.replace("세",""))
    user_dict[user_id].age = age

    res = {
        "version" : "2.0",
        "template":{
            "outputs": [
                {
                    "simpleText": {
                        "text" : "입력하신 나이는 " + ageReq + "입니다. 😊\n\n사용자님의 성별을 입력해 주세요. \nex) 남자"
                    }
                }
            ]
        }
    }
    return jsonify(res)



@app.route("/getGender", methods = ["GET","POST"])
def getGender():
    req = request.get_json()

    print(req)

    user_id = req["userRequest"]["user"]["id"]
    gender =  req["action"]["detailParams"]["성별"]["value"] #성별

    user_dict[user_id].gender = gender

    res = {
        "version" : "2.0",
        "template":{
            "outputs": [
                {
                    "simpleText": {
                        "text" : "입력하신 성별은 " + gender + "입니다. 😊\n\n사용자님의 키를 입력해 주세요. \nex) 165cm"
                    }
                }
            ]
        }
    }

    return jsonify(res)



@app.route("/getHeight", methods = ["GET", "POST"]) 
def Height():
    req = request.get_json()

    print(req)

    user_id = req["userRequest"]["user"]["id"]
    heightReq =  req["action"]["detailParams"]["sys_unit_length"]["origin"] #키 **cm
    print(heightReq)


    height = int(heightReq.replace("cm",""))
    user_dict[user_id].height = height

    res = {
        "version" : "2.0",
        "template":{
            "outputs": [
                {
                    "simpleText": {
                        "text" : "입력하신 키는 " + heightReq + "입니다. 😊\n\n사용자님의 몸무게를 입력해 주세요. \nex) 55kg"
                    }
                }
            ]
        }
    }

    return jsonify(res)



@app.route("/getWeight", methods = ["GET", "POST"]) 
def Weight():
    req = request.get_json()

    print(req)

    user_id = req["userRequest"]["user"]["id"]
    weightReq =  req["action"]["detailParams"]["sys_unit_weight"]["origin"] #몸무게 **kg
    weight = int(weightReq.replace("kg",""))
    user_dict[user_id].weight = weight

    res = {
        "version" : "2.0",
        "template":{
            "outputs": [
                {
                    "itemCard": {
                        "title": "종합 정보",
                        "description": "입력된 정보를 확인해 주세요.\n맞으면 '맞습니다', 정보가 틀리면 '재입력'을 눌러 다시 진행해주세요.",
                        "itemList": [
                            {
                                "title": "이름",
                                "description": user_dict[user_id].user_name
                            },
                            {
                                "title": "나이",
                                "description": str(user_dict[user_id].age) + "세"
                            },
                            {
                                "title": "성별",
                                "description": user_dict[user_id].gender
                            },
                            {
                                "title": "키",
                                "description": str(user_dict[user_id].height) + "cm"
                            },
                            {
                                "title": "몸무게",
                                "description": weightReq
                            }
                        ],
                        "itemListAlignment" : "left",
                        "buttons": [
                            {
                                "action": "message",
                                "label": "맞습니다",
                                "messageText": "운동량"
                            },
                            {
                                "action":  "message",
                                "label": "재입력",
                                "messageText": "기본정보"
                            }
                        ],
                        "buttonLayout" : "vertical"
                    }
                }
            ]
        }
    }

    print(user_dict[user_id])
    return jsonify(res)


@app.route("/getExercise", methods = ["GET", "POST"]) 
def Exercise():
    print("1회 운동시간 정보 받는 함수")
    exercise = ''
    req = request.get_json()

    print(req)

    user_id = req["userRequest"]["user"]["id"]
    exerciseReq =  req["action"]["detailParams"]["sys_number_ordinal"]["origin"] #운동 번호
    
    if exerciseReq == "1번":  exercise = "산책이나 출퇴근 걷기"
    elif exerciseReq == "2번": exercise = "실외 또는 실내 천천히 달리기"
    elif exerciseReq == "3번": exercise = "실외 또는 실내 빨리 달리기"
    elif exerciseReq == "4번": exercise = "등산"
    elif exerciseReq == "5번": exercise = "야외 또는 실내 자전거 타기"
    elif exerciseReq == "6번": exercise = "테니스, 스쿼시, 라켓볼"
    elif exerciseReq == "7번": exercise = "수영"
    elif exerciseReq == "8번": exercise = "에어로빅, 댄스"
    elif exerciseReq == "9번": exercise = "골프"
    elif exerciseReq == "10번": exercise = "스키"
    elif exerciseReq == "11번": exercise = "볼링"
    elif exerciseReq == "12번": exercise = "탁구"
    elif exerciseReq == "13번": exercise = "배드민턴"
    elif exerciseReq == "14번": exercise = "요가, 스트레칭"
    elif exerciseReq == "15번": exercise = "웨이트 트레이닝"
    elif exerciseReq == "16번": exercise = "윗몸 일으키기"
    elif exerciseReq == "17번": exercise = "팔굽혀펴기"
    elif exerciseReq == "18번": exercise = "줄넘기"
    elif exerciseReq == "19번": exercise = "아이스 스케이팅"
    elif exerciseReq == "20번": exercise = "롤러 스케이팅"
    elif exerciseReq == "21번": exercise = "태권도, 유도, 가라데 등의 무술"
    elif exerciseReq == "22번": exercise = "태극권, 기체조"
    elif exerciseReq == "23번": exercise = "단전호흡, 명상"
    elif exerciseReq == "24번": exercise = "복싱, 다이어트 복싱"
    elif exerciseReq == "25번": exercise = "아쿠아로빅"

    user_dict[user_id].exercise = exercise

    res = {
        "version" : "2.0",
        "template":{
            "outputs": [
                {
                    "simpleText": {
                        "text" : "입력하신 번호는 " + exerciseReq + "이므로, 선택 운동은 " + exercise + "입니다.\n\n해당 운동의 1회 운동 시간을 입력해주세요. \nex) 1시간20분\n\n* 한시간 미만인 경우 0시간30분 과 같이 입력해 주세요."
                    }
                }
            ]
        }
    }

    print(user_dict[user_id])
    return jsonify(res)



@app.route("/getExerciseTime", methods = ["GET", "POST"]) 
def ExerciseTime():
    print("1회 운동 시간 정보 받는 함수")
    req = request.get_json()

    print(req)

    user_id = req["userRequest"]["user"]["id"]
    exerciseTime =  req["action"]["detailParams"]["sys_unit_duration"]["origin"] #1회 운동 시간
    user_dict[user_id].exerciseTime = exerciseTime
    res = {
        "version" : "2.0",
        "template":{
            "outputs": [
                {
                    "simpleText": {
                        "text" : "입력하신 1회 운동 시간은 " + exerciseTime + "입니다.\n\n해당 운동의 주당 운동 횟수를 입력해주세요.\nex) 3회"
                    }
                }
            ]
        }
    }

    print(user_dict[user_id])
    return jsonify(res)


@app.route("/getExerciseNum", methods = ["GET", "POST"]) 
def ExerciseNum():
    print("주당 운동 횟수 정보 받는 함수")
    req = request.get_json()

    user_id = req["userRequest"]["user"]["id"]
    exerciseNum =  req["action"]["detailParams"]["횟수"]["value"] #주당 운동 횟수
    user_dict[user_id].exerciseNum = exerciseNum

    res = {
        "version" : "2.0",
        "template":{
            "outputs": [
                {
                    "itemCard": {
                        "title": "운동 정보",
                        "description": "입력된 정보를 확인해 주세요.\n맞으면 '맞습니다', 정보가 틀리면 '재입력'을 눌러 다시 진행해주세요.",
                        "itemList": [
                            {
                                "title": "운동",
                                "description": user_dict[user_id].exercise
                            },
                            {
                                "title": "1회운동시간",
                                "description": user_dict[user_id].exerciseTime
                            },
                            {
                                "title": "주당운동횟수",
                                "description": user_dict[user_id].exerciseNum
                            }
                        ],
                        "itemListAlignment" : "left",
                        "buttons": [
                            {
                                "action": "message",
                                "label": "맞습니다",
                                "messageText": "추가운동조사"
                            },
                            {
                                "action":  "message",
                                "label": "재입력",
                                "messageText": "운동량"
                            }
                        ],
                        "buttonLayout" : "vertical"
                    }
                }
            ]
        }
    }

    print(user_dict[user_id])
    return jsonify(res)



@app.route("/getNutriNum", methods = ["GET", "POST"]) 
def NutriNum():
    print("영양제 종류 받는 함수")
    req = request.get_json()

    print(req)

    user_id = req["userRequest"]["user"]["id"]
    nutriType =  req["action"]["detailParams"]["nutriNum"]["value"] #영양제 종류(개수)
    print(nutriType)

    
    nutriType2Num = re.findall("\d+", nutriType)
    
    user_dict[user_id].nutriType = nutriType

   
    res = {
        "version" : "2.0",
        "template":{
            "outputs": [
                {
                    "simpleText": {
                        "text" : "영양제 종류가" + user_dict[user_id].nutriType + "가 맞는지 확인해 주세요.\n맞으면 '맞습니다', 정보가 틀리면 '재입력'을 눌러 다시 진행해주세요."
                    }
                }
            ], "quickReplies": [
                {
                    "messageText" : "영양제이름",
                    "action": "message",
                    "label" : "맞습니다"
                },{
                    "messageText" : "영양제종류",
                    "action": "message",
                    "label" : "재입력"
                }
            ]
        }
    }

    
    print(user_dict[user_id])
    return jsonify(res)


@app.route("/getNutri", methods = ["GET", "POST"]) 
def Nutri():
    print("영양제 이름 받는 함수")
    req = request.get_json()

    print(req)

    user_id = req["userRequest"]["user"]["id"]
    nutriSupplement =  req["action"]["detailParams"]["nutri"]["value"] #영양제 이름
    print(nutriSupplement)

    user_dict[user_id].nutriSupplement = nutriSupplement

    res = {
        "version" : "2.0",
        "template":{
            "outputs": [
                {
                    "simpleText": {
                        "text" : "입력하신 영양제의 이름은 " + nutriSupplement + "입니다.\n\n해당 영양제의 하루 섭취 횟수를 선택해주세요.\n섭취하시는 횟수가 없으시면 기타를 눌러주세요."
                    }
                }
            ], "quickReplies": [
                {
                    "messageText" : "영양제선택1",
                    "action": "message",
                    "label" : "1알(포)"
                },{
                    "messageText" : "영양제선택2",
                    "action": "message",
                    "label" : "2알(포)"
                },{
                    "messageText" : "영양제선택3",
                    "action": "message",
                    "label" : "3알(포)"
                },{
                    "messageText" : "영양제기타",
                    "action": "message",
                }
            ]
        }
    }

    print(user_dict[user_id])
    return jsonify(res)



@app.route("/getNutriIntake", methods = ["GET", "POST"]) 
def nutriIntake():

    print("영양제 섭취량 받는 함수")

    req = request.get_json()
    print(req)
    
    nutriIntake = ""
    user_id = req["userRequest"]["user"]["id"]
    nutriIntakeStr =  req["action"]["detailParams"]["영양제선택지"]["value"] #영양제 복용량
    

    if nutriIntakeStr == "영양제선택1":
        nutriIntake = "1알(포)"
    elif nutriIntakeStr == "영양제선택2":
        nutriIntake = "2알(포)"
    elif nutriIntakeStr == "영양제선택3":
        nutriIntake == "3알(포)"

    user_dict[user_id].nutriIntake = nutriIntake

    res = {
        "version" : "2.0",
        "template":{
            "outputs": [
                {
                    "itemCard": {
                        "title": "종합 정보",
                        "description": "입력된 정보를 확인해 주세요.\n맞으면 '맞습니다', 정보가 틀리면 '재입력'을 눌러 다시 진행해주세요.",
                        "itemList": [
                            {
                                "title": "영양제 이름",
                                "description": user_dict[user_id].nutriSupplement
                            },
                            {
                                "title": "하루 섭취량",
                                "description": user_dict[user_id].nutriIntake
                            }
                        ],
                        "itemListAlignment" : "left",
                        "buttons": [
                            {
                                "action": "message",
                                "label": "맞습니다",
                                "messageText": "식품섭취빈도조사"
                            },
                            {
                                "action":  "message",
                                "label": "재입력",
                                "messageText": "영양제"
                            }
                        ],
                        "buttonLayout" : "vertical"
                    }
                }
            ]
        }
    }

    print(user_dict[user_id])
    return jsonify(res)


# ---------------------------------------식품섭취 빈도 시작 -----------------------------------------------

import constant

foodListForSurvey = list(식이빈도조사_음식섭취양.find())

@app.route("/get1Frequency", methods = ["GET", "POST"])
def get1Frequency():

    req = request.get_json()
    user_id = req["userRequest"]["user"]["id"]

    nowFood = ''
    idx = user_dict[user_id].survey.idx

    if user_dict[user_id].survey.idx == 0:
        print("새로운 읍식 섭취 빈도 조사 시작")
        nowFood = foodListForSurvey[user_dict[user_id].survey.idx]

    else :
        reqEntity = req["action"]["detailParams"]["섭취양선택지"]["value"]
        beforeFood = foodListForSurvey[user_dict[user_id].survey.idx-1]
        portion = 0

        dbResult = str(식이빈도조사_음식섭취양.find_one({"음식종류" : beforeFood ["음식종류"]},{"_id" : False, "음식종류" : False})).split("'")
        if reqEntity == '빈도선택1':
            user_dict[user_id].survey.foodEntity.append(dbResult[3])
            portion = dbResult[3]
        elif reqEntity == '빈도선택2' :
            user_dict[user_id].survey.foodEntity.append(dbResult[7])
            portion = dbResult[7]
        elif reqEntity == '빈도선택3':
            user_dict[user_id].survey.foodEntity.append(dbResult[11])
            portion = dbResult[11]
        
        frequencyPerDay = user_dict[user_id].survey.foodFrequency[idx-1]
        print(frequencyPerDay, portion, beforeFood['음식종류'])

        calculateSolution(user_id, frequencyPerDay = frequencyPerDay, portion= portion, foodName= beforeFood['음식종류'])

        if user_dict[user_id].survey.idx == len(foodListForSurvey):
            # if user_dict[user_id].survey.idx == 4:
            add_survey_result_to_excel(user_dict[user_id])

            user_dict[user_id].solutionResultText = provideSolution(
                user_id = user_id, 
                energy = user_dict[user_id].solution_칼로리, 
                carbo = user_dict[user_id].solution_탄수화물, 
                protein = user_dict[user_id].solution_단백질, 
                fat = user_dict[user_id].solution_지방, 
                sodium = user_dict[user_id].solution_나트륨, 
                calcium = user_dict[user_id].solution_칼슘, 
                vitaminC = user_dict[user_id].solution_비타민C, 
                SFA = user_dict[user_id].solution_포화지방산
            )
            
            # init_info() # 얘는 뭐징..?
            res = {
                "version" : "2.0",
                "template":{
                    "outputs": [
                        {
                            "simpleText": {
                                "text" : "모든 문항에 대한 검사가 완료되었습니다.\n감사합니다."
                            }
                        }
                    ], "quickReplies": [{
                            "messageText" : "1년섭취빈도조사종료",
                            "action": "message",
                            "label" : "1년섭취빈도조사종료",
                            "messageText": "1년섭취빈도조사종료"
                        }
                    ]
                }
            }

            return res   

        nowFood = foodListForSurvey[idx]

    # 답변과 다음 설문조사지 만들기.
    print(foodFrequency, foodEntity)
    print("{foodName}에 대한 음식 섭취 빈도 조사 시작".format(foodName = nowFood["음식종류"]))
    
    simpleText = "("+ str(idx+1) + "/119)' {foodName}'을 최근 1년간 얼마나 자주 섭취했는지 선택해 주세요,\n선택지에 없을 경우, 최대한 비슷한 횟수를 선택해주세요.".format(foodName=nowFood["음식종류"])
    quickReplies = constant.FOOD_SURVEY_QUICKREPLIES

    res = {
        "version" : "2.0",
        "template":{
            "outputs": [
                {
                    "simpleText": {
                        "text" : simpleText
                    }
                }
            ], "quickReplies": quickReplies
        }
    }

    return res

@app.route("/get1Entity", methods = ["GET", "POST"])
def get1Entity():
    req = request.get_json()
    user_id = req["userRequest"]["user"]["id"]

    print("1년 섭취 빈도 받기, 섭취량 시작 함수")
    frequency =  req["action"]["detailParams"]["식품섭취빈도조사선택지"]["value"] #식품섭취빈도

    nowFood = foodListForSurvey[user_dict[user_id].survey.idx]

    simpleText = "선택하신 섭취 빈도는 {frequency} 입니다. \n'{foodName}'을 1회 섭취하실 때, 평균 섭취량을 선택해 주세요.\n선택지에 없을 경우, 최대한 비슷한 횟수를 선택해주세요.".format(frequency = frequency, foodName=nowFood["음식종류"])
    quickReplies = makeQuickRepliesForFoodEntity(nowFood)

    res = {
        "version" : "2.0",
        "template":{
            "outputs": [
                {
                    "simpleText": {
                        "text" : simpleText
                    }
                }
            ], "quickReplies": quickReplies
        }
    }

    frequencyPerDay = 0 # 하루 섭취량으로 변경

    if frequency == '거의 안 먹음':
        frequencyPerDay = 0
    elif frequency == '1개월 1번':
        frequencyPerDay = 0.083
    elif frequency == '1개월 2-3번':
        frequencyPerDay = 0.083
    elif frequency == '1주일 1번':
        frequencyPerDay = 0.143
    elif frequency == '1주일 2-4번':
        frequencyPerDay = 0.429
    elif frequency == '1주일 5-6번':
        frequencyPerDay = 0.786
    elif frequency == '1일 1번':
        frequencyPerDay = 1
    elif frequency == '1일 2번':
        frequencyPerDay = 2
    elif frequency == '1일 3번':
        frequencyPerDay = 3
    

    user_dict[user_id].survey.idx += 1
    user_dict[user_id].survey.foodFrequency.append(frequencyPerDay)
    return res

@app.route("/serveSolution", methods = ["GET", "POST"])
def serveSolution():
    req = request.get_json()
    user_id = req["userRequest"]["user"]["id"]
    solutionResultText = user_dict[user_id].solutionResultText

    res = {
        "version" : "2.0",
        "template":{
            "outputs": [
                {
                    "simpleText": {
                        "text" : solutionResultText
                    }
                }
            ], "quickReplies": [
                {
                    "messageText" : "시작",
                    "action": "message",
                    "label" : "종료"
                }
            ]
        }
    }

    return res

#------------------------------------------------------------------------관련 함수------------------------------------------------------------------------#

# 설문 결과 엑셀로.
def add_survey_result_to_excel(user: SurveyUser):

    now = str(datetime.now())
    excel_row = []

    excel_row.append(now)
    for info in user.get_user_info():
        excel_row.append(info)

    for frequency, entity in zip(user.survey.foodFrequency, user.survey.foodFrequency):
        excel_row.append(frequency)
        excel_row.append(entity)

    while len(excel_row) < 250:
        excel_row.append("응답 없음")

    df = None
    df = pd.read_excel("./data/1년섭취빈도조사.xlsx", engine='openpyxl')
    df = df.append(pd.Series(excel_row, index=df.columns) , ignore_index=True)
    df.to_excel("./data/1년섭취빈도조사.xlsx", index=False)

def init_info():
    pass

def makeQuickRepliesForFoodEntity(food):
    quickReplies = []

    for k,v in food.items():
        if k == "선택1" or k == "선택2" or k == "선택3":
            quickReplies.append({
                "messageText" : "빈도{k}".format(k = k),
                "action": "message",
                "label" : "{v}{단위}".format(v = v, 단위=food["단위"])
            })

    return quickReplies


# 솔루션 계산 함수
def calculateSolution(user_id,frequencyPerDay, portion, foodName):
    dbResult = str(식이빈도조사_단위영양성분.find_one({"음식종류" : foodName},{"_id" : False, "음식종류" : False})).replace(':','').replace(',','').replace('}','').split("'")
    
    # 솔루션을 위한 각 합 -> 이걸로 솔루션 제공 가능 
    user_dict[user_id].solution_칼로리 += frequencyPerDay * Fraction(portion) * float(dbResult[2])
    user_dict[user_id].solution_탄수화물 += frequencyPerDay * Fraction(portion) * float(dbResult[4])
    user_dict[user_id].solution_단백질 += frequencyPerDay * Fraction(portion) * float(dbResult[6])
    user_dict[user_id].solution_지방 += frequencyPerDay * Fraction(portion) * float(dbResult[8])
    user_dict[user_id].solution_나트륨 += frequencyPerDay * Fraction(portion) * float(dbResult[10])
    user_dict[user_id].solution_칼슘 += frequencyPerDay * Fraction(portion) * float(dbResult[12])
    user_dict[user_id].solution_비타민C += frequencyPerDay * Fraction(portion) * float(dbResult[14])
    user_dict[user_id].solution_포화지방산 += frequencyPerDay * Fraction(portion) * float(dbResult[16])
    
    print(solution_칼로리, solution_탄수화물, solution_단백질, solution_지방, solution_나트륨, solution_칼슘, solution_비타민C, solution_포화지방산)

# 솔루션 그래프 + 줄글 제공
def provideSolution(user_id, energy, carbo, protein, fat, sodium, calcium, vitaminC, SFA):
    age = user_dict[user_id].age
    user_name = user_dict[user_id].user_name
    # 탄단지 비율 구하기
    carboRatio = round(carbo * 4 / (carbo*4 + protein * 4 + fat * 9), 2)
    proteinRatio = round(protein *4 / (carbo*4 + protein * 4 + fat * 9),2)
    fatRatio = round(fat*9 / (carbo*4 + protein * 4 + fat * 9),2)

    SFARatio = round(SFA * 9 / energy, 2)

    print(carboRatio, proteinRatio, fatRatio, SFARatio)

     #나이에 맞는 기준량
    if age >= 19 and age < 30:
        print("19~29") 
        val_calorie = 2600 #값 - 칼로리(kcal)
        val_sodium = 2300 # 값 - 나트륨(mg)
        val_protein = 65 # 값 - 단백질(g)
        val_cal = 800 #값 - 칼슘
        val_vC = 100 #값 - 비타민 C
        saturatedFat = 7 #비율 - 포화지방산 비율
    elif age >= 30 and age < 50:
        print("30~49")
        val_calorie = 2500 #값 - 칼로리(kcal)
        val_sodium = 2300 # 값 - 나트륨(mg)
        val_protein = 65 # 값 - 단백질(g)
        val_cal = 800 #값 - 칼슘
        val_vC = 100 #값 - 비타민 C
        saturatedFat = 7 #비율 - 포화지방산 비율
    elif age >= 50 and age < 65:
        print("50~64")
        val_calorie = 2000 #값 - 칼로리(kcal)
        val_sodium = 2100 # 값 - 나트륨(mg)
        val_protein = 60 # 값 - 단백질(g)
        val_cal = 750 #값 - 칼슘
        val_vC = 100 #값 - 비타민 C
        saturatedFat = 7 #비율 - 포화지방산 비율
    elif age >= 65 and age < 75:
        print("65~74")
        val_calorie = 2000 #값 - 칼로리(kcal)
        val_sodium = 2100 # 값 - 나트륨(mg)
        val_protein = 60 # 값 - 단백질(g)
        val_cal = 700 #값 - 칼슘
        val_vC = 100 #값 - 비타민 C
        saturatedFat = 7 #비율 - 포화지방산 비율
    elif age >= 75:
        print("75 이상")
        val_calorie = 1900 #값 - 칼로리(kcal)
        val_sodium = 1700 # 값 - 나트륨(mg)
        val_protein = 60 # 값 - 단백질(g)
        val_cal = 700 #값 - 칼슘
        val_vC = 100 #값 - 비타민 C
        saturatedFat = 7 #비율 - 포화지방산 비율
    else:
        print("나이 미입력")

    # 영양성분 부족, 적절, 초과 판단
    # 칼로리
    if energy > val_calorie :
        printEnergySolution = '적절'
    elif energy <= val_calorie:
        printEnergySolution = '부족'
    
    # 단백질
    if protein > val_protein:
        printProteinSolution = '충분'
    elif protein <= val_protein:
        printProteinSolution = '부족'

    # 포화지방 비율
    if SFARatio < saturatedFat:
        printSFASolution = '적절'
    elif SFARatio >= saturatedFat:
        printSFASolution = '초과'
    
    # 나트륨
    if sodium <= val_sodium:
        printSodiumSolution = '적절'
    elif sodium > val_sodium:
        printSodiumSolution = '초과'

    # 칼슘
    if calcium > val_cal :
        printCalciumSolution = '적절'
    elif calcium <= val_cal:
        printCalciumSolution = '부족'

    # 비타민C
    if vitaminC > val_vC:
        printVCSolution = '적절'
    elif vitaminC <= val_vC:
        printVCSolution = '부족'

    print(printEnergySolution, printProteinSolution, printSFASolution, printSodiumSolution, printCalciumSolution, printVCSolution)

    totalSolution = "본 솔루션은 영양제와 운동량 정보를 포함하지 않습니다.\n\n▶ 영양 평가는 " + user_name + "님께서 기록하신 최근 1년 동안 섭취한 음식들의 빈도로 분석한 영양평가입니다. \n따라서 기록하신 최근 1년 동안의 식사섭취가 본인의 평소 식사와 같았는지, 아니면 어떻게 달랐는지를 생각하면서 영양평가를 참고하시어 건강한 식생활을 유지하시기 바랍니다."

    ratioSolution = "\n▶ 영양 권장량 대비 섭취 비율입니다.\n한국인의 3대 열량 영양소의 권장 섭취 비율은 [탄수화물: 단백질: 지방 = 55-65: 7-20: 15-30] 입니다.\n귀하의 최근 1년 동안의 식품 섭취 빈도조사에 따른 평균 열량 영양소 섭취 비율은 다음과 같습니다.\n열량(kcal) : " + str(round(energy,3)) + "\n탄수화물(g) : " + str(round(carboRatio * 100,2)) + "%\n지방(g) : " + str(round(fatRatio * 100,2)) + "%\n단백질(g) : " + str(round(proteinRatio*100,2)) + "%"

    resultSolution = "\n▶ 영양소별 평가 결과입니다.\n열량은 에너지필요추정량(" + str(val_calorie) + "kcal) 기준으로 " + str(printEnergySolution) + "하게 섭취하셨습니다.\n단백질은 권장섭취량(" + str(val_protein) + "g)을 기준으로 " + str(printProteinSolution) + "하게 섭취하셨습니다.\n포화지방의 경우 에너지적정비율(" + str(saturatedFat) + "%)기준으로 " + str(printSFASolution) + "하게 섭취하셨습니다.\n나트륨은 만성질환위험감소섭취량(" + str(val_sodium) + "mg)을 기준으로 " + str(printSodiumSolution) + "하게 섭취하셨습니다."

    cal_vC_Solution = "칼슘은 권장 섭취량(" + str(val_cal) + "mg) 기준으로 " + str(printCalciumSolution) + "하게 섭취하셨습니다.\n비타민C는 권장 섭취량(" + str(val_vC) + "mg) 기준으로 " + str(printVCSolution) + "하게 섭취하셨습니다."

    print(totalSolution)
    print(ratioSolution)
    print(resultSolution)
    print(cal_vC_Solution)
    
    resultArr = [totalSolution, ratioSolution, resultSolution, cal_vC_Solution]
    result = "\n".join(resultArr)

    print(result)

    return result


    
#------------------------------------------------------------------------1일 솔루션(의대)------------------------------------------------------------------------#

import urllib.request
import requests
from PIL import Image

# 사진 전송 요구 + 사진 클라우드 링크 받아오는 함수 
@app.route("/getPhoto", methods=["GET", "POST"])
def start():
    print("사진을 받는 함수")
    global foodArr
    req = request.get_json()

    print(req)

    # photo_type = req["action"]["detailParams"]["image"]["value"]
    photo_type = req["action"]["detailParams"]["사진전송"]['value']
    photo_json = json.loads(photo_type)

    photo_url = photo_json["secureUrls"]
    u = photo_url[5:-1]

    class AppURLopener(urllib.request.FancyURLopener):
        version = "Mozilla/5.0"
        
    urllib._urlopener = AppURLopener()

    urllib._urlopener.retrieve(u, "test.jpg")
    urlretrieve_img = Image.open("test.jpg")

    upload = {'image': open('/home/user/jiyoung/flask/test.jpg', 'rb')} # 업로드하기위한 파일

    res = requests.post('http://localhost:5000/receive', files=upload).json() # JSON 포맷, POST 형식으로 해당 URL에 파일 전송
    imgurl = res[0]['imgurl']
    food = res[1]['food']
    foodArr = food
    foodstr = ", ".join(food)

    print(":::::::::::::::::;",imgurl,food)

    res = {
              "version": "2.0",
              "template": {
                "outputs": [
                  {
                    "simpleText": {
                       "text": "사진에서 인식된 음식은 " +foodstr+ " 입니다. \n인식이 잘 되었는지 아래에서 선택해주세요."
                     }
                   }
                 ],
                  "quickReplies": [
                     {
                       "messageText": "직접 입력",
                       "action": "message",
                       "label": "아니요. 없는 음식이 있습니다."
                      }, {
                       "messageText": "사진음식양입력",
                       "action": "message",
                       "label": "네. 인식이 잘 되었습니다."
                     }
                   ]
                 }
               }
    print(foodArr)
    return res

@app.route("/photoFood", methods = ["GET", "POST"])
def photoFood():
    global foodArr

    req = request.get_json()
    print(req)

    food_type = req["action"]["detailParams"]["음식"]["value"]
    print(food_type)



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
                    "messageText" : "식단입력종료",
                    "action": "message",
                    "label" : "🏠종료"
                }
            ]
        }
    }

    return jsonify(res)


@app.route("/solution",methods = ["GET","POST"])
def solution():
    df = None
    print("솔루션 제공 함수")

    req = request.get_json()
    user_id = req["userRequest"]["user"]["id"]
    print(user_id)


    answer = "3끼를 기준으로 솔루션을 제공합니다."
    now = str(datetime.today().strftime("%Y-%m-%d"))

    try:
        df = pd.read_excel("./data/" + user_id + ".xlsx", engine='openpyxl')
        solutionDF = df[df.날짜 == now]

        calorie_sum = solutionDF['calorie'].sum()
        sodium_sum = solutionDF['sodium'].sum()
        carbo_sum = solutionDF['carbonhydrate'].sum()
        protein_sum = solutionDF['protein'].sum()
        fat_sum = solutionDF['fat'].sum()
        calcium_sum = solutionDF['calcium'].sum()
        vitC_sum = solutionDF['vitamin C'].sum()
        saturated_sum = solutionDF['saturated Fat'].sum()

        print(calorie_sum, sodium_sum, carbo_sum, protein_sum, fat_sum, calcium_sum, vitC_sum, saturated_sum)
        answer = provideDaySolution(user_id, calcium_sum, carbo_sum, protein_sum, fat_sum, sodium_sum, calcium_sum, vitC_sum, saturated_sum)
        print('comeback')

    except Exception as e:
        answer = "입력된 식단 정보가 없습니다.\n식단 입력 후 다시 시도해주세요."



    res = {
        "version" : "2.0",
        "template":{
            "outputs": [
                {
                    "simpleText": {
                        "text" : answer
                    }
                }
            ], "quickReplies": [{
                    "messageText" : "시작",
                    "action": "message",
                    "label" : "종료",
                }
            ]
        }
    }

    print(answer)

    return res

def provideDaySolution(userID, energy, carbo, protein, fat, sodium, calcium, vitaminC, SFA):
    df = None
    print('일간 식단 솔루션 제공')
    # try:
    #     df = pd.read_excel("./data/1년섭취빈도조사.xlsx", engine='openpyxl')
    #     userDF = df[df.UserID == userID]

    #     age = userDF.at[0, '나이']
    #     user_name = userDF.at[0, '이름']

    #     print(age, user_name)
        
    # except:
    #     result = "사용자님의 정보가 존재하지 않습니다.\n'홈'메뉴의 '챗봇 시작하기'를 눌러 1년 섭취량 기준 솔루션을 먼저 제공받아주세요."

    global age
    global user_name

    # 탄단지 비율 구하기
    carboRatio = round(carbo * 4 / (carbo*4 + protein * 4 + fat * 9), 2)
    proteinRatio = round(protein *4 / (carbo*4 + protein * 4 + fat * 9),2)
    fatRatio = round(fat*9 / (carbo*4 + protein * 4 + fat * 9),2)

    SFARatio = round(SFA * 9 / energy, 2)

    print(carboRatio, proteinRatio, fatRatio, SFARatio)

     #나이에 맞는 기준량
    if age >= 19 and age < 30:
        print("19~29") 
        val_calorie = 2600 #값 - 칼로리(kcal)
        val_sodium = 2300 # 값 - 나트륨(mg)
        val_protein = 65 # 값 - 단백질(g)
        val_cal = 800 #값 - 칼슘
        val_vC = 100 #값 - 비타민 C
        saturatedFat = 7 #비율 - 포화지방산 비율
    elif age >= 30 and age < 50:
        print("30~49")
        val_calorie = 2500 #값 - 칼로리(kcal)
        val_sodium = 2300 # 값 - 나트륨(mg)
        val_protein = 65 # 값 - 단백질(g)
        val_cal = 800 #값 - 칼슘
        val_vC = 100 #값 - 비타민 C
        saturatedFat = 7 #비율 - 포화지방산 비율
    elif age >= 50 and age < 65:
        print("50~64")
        val_calorie = 2000 #값 - 칼로리(kcal)
        val_sodium = 2100 # 값 - 나트륨(mg)
        val_protein = 60 # 값 - 단백질(g)
        val_cal = 750 #값 - 칼슘
        val_vC = 100 #값 - 비타민 C
        saturatedFat = 7 #비율 - 포화지방산 비율
    elif age >= 65 and age < 75:
        print("65~74")
        val_calorie = 2000 #값 - 칼로리(kcal)
        val_sodium = 2100 # 값 - 나트륨(mg)
        val_protein = 60 # 값 - 단백질(g)
        val_cal = 700 #값 - 칼슘
        val_vC = 100 #값 - 비타민 C
        saturatedFat = 7 #비율 - 포화지방산 비율
    elif age >= 75:
        print("75 이상")
        val_calorie = 1900 #값 - 칼로리(kcal)
        val_sodium = 1700 # 값 - 나트륨(mg)
        val_protein = 60 # 값 - 단백질(g)
        val_cal = 700 #값 - 칼슘
        val_vC = 100 #값 - 비타민 C
        saturatedFat = 7 #비율 - 포화지방산 비율
    else:
        print("나이 미입력")

    # 영양성분 부족, 적절, 초과 판단
    # 칼로리
    if energy > val_calorie :
        printEnergySolution = '적절'
    elif energy <= val_calorie:
        printEnergySolution = '부족'
    
    # 단백질
    if protein > val_protein:
        printProteinSolution = '충분'
    elif protein <= val_protein:
        printProteinSolution = '부족'

    # 포화지방 비율
    if SFARatio < saturatedFat:
        printSFASolution = '적절'
    elif SFARatio >= saturatedFat:
        printSFASolution = '초과'
    
    # 나트륨
    if sodium <= val_sodium:
        printSodiumSolution = '적절'
    elif sodium > val_sodium:
        printSodiumSolution = '초과'

    # 칼슘
    if calcium > val_cal :
        printCalciumSolution = '적절'
    elif calcium <= val_cal:
        printCalciumSolution = '부족'

    # 비타민C
    if vitaminC > val_vC:
        printVCSolution = '적절'
    elif vitaminC <= val_vC:
        printVCSolution = '부족'

    print(printEnergySolution, printProteinSolution, printSFASolution, printSodiumSolution, printCalciumSolution, printVCSolution)

    totalSolution = "▶ 영양 평가는 " + user_name + "님께서 오늘 하루동안 섭취한 음식들의 빈도로 분석한 영양평가입니다.\n앞으로의 건강한 식단 구성에 참고하시길 바랍니다."

    ratioSolution = "\n▶ 영양 권장량 대비 섭취 비율입니다.\n한국인의 3대 열량 영양소의 권장 섭취 비율은 [탄수화물: 단백질: 지방 = 55-65: 7-20: 15-30] 입니다.\n귀하의 금일 식품 섭취 빈도조사에 따른 평균 열량 영양소 섭취 비율은 다음과 같습니다.\n열량(kcal) : " + str(round(energy,3)) + "\n탄수화물(g) : " + str(round(carboRatio * 100,2)) + "%\n지방(g) : " + str(round(fatRatio * 100,2)) + "%\n단백질(g) : " + str(round(proteinRatio*100,2)) + "%"

    resultSolution = "\n▶ 영양소별 평가 결과입니다.\n열량은 에너지필요추정량(" + str(val_calorie) + "kcal) 기준으로 " + str(printEnergySolution) + "하게 섭취하셨습니다.\n단백질은 권장섭취량(" + str(val_protein) + "g)을 기준으로 " + str(printProteinSolution) + "하게 섭취하셨습니다.\n포화지방의 경우 에너지적정비율(" + str(saturatedFat) + "%)기준으로 " + str(printSFASolution) + "하게 섭취하셨습니다.\n나트륨은 만성질환위험감소섭취량(" + str(val_sodium) + "mg)을 기준으로 " + str(printSodiumSolution) + "하게 섭취하셨습니다."

    cal_vC_Solution = "칼슘은 권장 섭취량(" + str(val_cal) + "mg) 기준으로 " + str(printCalciumSolution) + "하게 섭취하셨습니다.\n비타민C는 권장 섭취량(" + str(val_vC) + "mg) 기준으로 " + str(printVCSolution) + "하게 섭취하셨습니다."

    
    resultArr = [totalSolution, ratioSolution, resultSolution, cal_vC_Solution]
    result = "\n".join(resultArr)

    print(result)

    return result


#------------------------------------------------------------------------Test Func------------------------------------------------------------------------#


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




#------------------------------------------------------------------------엑셀 저장 함수------------------------------------------------------------------------#


def to_excel(user_id, food_calculate):
    df = None

    now = str(datetime.today().strftime("%Y-%m-%d"))

    try:
        df = pd.read_excel("./data/" + user_id + ".xlsx", engine='openpyxl')
    except Exception as e:
        df = pd.DataFrame(columns = ["날짜","음식","calorie","sodium","carbonhydrate","protein","fat","calcium", "vitamin C", "saturated Fat"])
    
    new_data = {
        "날짜" : now,
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


#------------------------------------------------------------------------ Port------------------------------------------------------------------------#


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, threaded = True)