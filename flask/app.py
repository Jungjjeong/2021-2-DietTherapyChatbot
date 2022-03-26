from stat import SF_ARCHIVED
from flask import Flask, json, request, jsonify
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.core.indexes.api import get_objs_combined_axis
from pymongo import MongoClient
from fractions import Fraction
import re

#from torch import bernoulli


from user import SurveyUser
app = Flask(__name__)

cluster = MongoClient("mongodb+srv://user:0000@cluster0.uio0y.mongodb.net/myFirstDatabase?retryWrites=true&w=majority") # DB연결

# cluster = MongoClient("mongodb+srv://HyobinLim:qwe123@cluster0.z4pao.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")


db = cluster["DietTherapy"]
음식영양성분 = db["음식영양성분"]
음식섭취양 = db["음식섭취양"]
식이빈도조사_음식섭취양 = db["식이빈도조사_음식섭취양3"]
식이빈도조사_단위영양성분 = db["식이빈도조사_단위영양성분2"]
user_dict = {} # SurveyUser 객체가 들어감. 

food_name = ""
user_name = ""
age = 0
gender = ""
height = 0
weight = 0
exerciseTypeNum = 0
exerciseWeight = 0
exerciseIndex = 0
exercise = ""
exerciseTimeHour = ""
exerciseTimeMin = ""
exerciseNum = ""
nutriTypeNum = 0
nutriIdx = 0
nutriSupplement = ""
nutriCompany = ""
nutriTerm = ""
nutriFrequency = ""
nutriIntake = ""
PAL = 0
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
solution_포화지방산_상위 = []

solutionResultText = ""

@app.route("/")
def hello():
    return "Chatbot server"

#------------------------------------------------------------------------1년 솔루션(서울대)------------------------------------------------------------------------#

@app.route("/getUserName", methods = ["GET", "POST"]) 
def getUserName():
    #print("이름 정보 받는 함수")

    req = request.get_json()

    #print(req)

    user_id = req["userRequest"]["user"]["id"]
    user_name =  req["action"]["detailParams"]["userName"]["value"] 

    user = SurveyUser(user_id, user_name)
    # print(user)
    # print(type(user))
    user_dict[user_id] = user

    res = {
        "version" : "2.0",
        "template":{
            "outputs": [
                {
                    "simpleText": {
                        "text" : "입력하신 이름은 " + user_dict[user_id].user_name + "입니다. 😊\n\n사용자님의 만 나이를 입력해 주세요.\n(*단위 필수 입력)\nex) 24세"
                    }
                }
            ]
        }
    }

    #print(user_dict)
    print(user_dict[user_id])
    print("이름 : ", user_name)
    return jsonify(res)


@app.route("/getAge", methods = ["GET", "POST"]) 
def getAge():

    global age
    req = request.get_json()

    #print(req)

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
                            "text" : "입력하신 나이는 " + ageReq + "입니다. 😊\n\n사용자님의 성별을 선택해 주세요."
                        }
                    }
                ], "quickReplies": [
                    {
                        "messageText" : "남자",
                        "action": "message",
                        "label" : "남자"
                    },{
                        "messageText" : "여자",
                        "action": "message",
                        "label" : "여자"
                    }
                ]
        }
    }

    # print(user_dict)
    print("나이 : ", age)
    return jsonify(res)



@app.route("/getGender", methods = ["GET","POST"])
def getGender():
    req = request.get_json()

    #print(req)

    user_id = req["userRequest"]["user"]["id"]
    gender =  req["action"]["detailParams"]["성별"]["value"] #성별

    user_dict[user_id].gender = gender

    res = {
        "version" : "2.0",
        "template":{
            "outputs": [
                {
                    "simpleText": {
                        "text" : "입력하신 성별은 " + gender + "입니다. 😊\n\n사용자님의 키를 입력해 주세요.\n(*단위 필수 입력)\nex) 165cm"
                    }
                }
            ]
        }
    }

    print("성별 : ", gender)

    return jsonify(res)



@app.route("/getHeight", methods = ["GET", "POST"]) 
def getHeight():
    req = request.get_json()

    #print(req)

    user_id = req["userRequest"]["user"]["id"]
    heightReq =  req["action"]["detailParams"]["sys_unit_length"]["origin"] #키 **cm


    height = int(heightReq.replace("cm",""))
    user_dict[user_id].height = height

    res = {
        "version" : "2.0",
        "template":{
            "outputs": [
                {
                    "simpleText": {
                        "text" : "입력하신 키는 " + heightReq + "입니다. 😊\n\n사용자님의 몸무게를 입력해 주세요.\n(*단위 필수 입력, 소수 첫째 자리에서 반올림 해주세요.) \nex) 55.4kg -> 55kg"
                    }
                }
            ]
        }
    }

    print("키 : ", height)

    return jsonify(res)



@app.route("/getWeight", methods = ["GET", "POST"]) 
def getWeight():
    req = request.get_json()

    #print(req)

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

    #print(user_dict[user_id])
    print("몸무게 : ", weight)
    return jsonify(res)


@app.route("/getExerciseType", methods = ["GET", "POST"]) 
def getExerciseType():
    print("운동 개수를 받는 함수")

    req = request.get_json()

    # print(req)

    user_id = req["userRequest"]["user"]["id"]
    exerciseReq =  req["action"]["detailParams"]["운동"]["value"] #운동 개수
    exerciseTypeNum = int(exerciseReq.replace("개",""))
    print(exerciseTypeNum)
    user_dict[user_id].exerciseTypeNum = exerciseTypeNum
    
    res = {
            "version" : "2.0",
            "template":{
                "outputs": [
                    {
                        "simpleText": {
                            "text" : "입력하신 운동 개수는 " + exerciseReq + "입니다. \n\n맞으면 '맞습니다' 틀리면 '재입력'을 눌러 다시 진행해주세요."
                        }
                    }
                ], "quickReplies": [
                    {
                        "messageText" : "운동이미지",
                        "action": "message",
                        "label" : "맞습니다"
                    },{
                        "messageText" : "운동량",
                        "action": "message",
                        "label" : "재입력"
                    }
                ]
            }
        }

    print(user_dict[user_id])
    return jsonify(res)
    

@app.route("/getExercise", methods = ["GET", "POST"]) 
def getExercise():
    print("운동 이름 받는 함수")
    exercise = ''
    req = request.get_json()

    # print(req)

    user_id = req["userRequest"]["user"]["id"]
    exerciseReq =  req["action"]["detailParams"]["sys_number_ordinal"]["origin"] #운동 번호
    
    if exerciseReq == "1번":  
        exercise = "산책이나 출퇴근 걷기"
        exerciseWeight = 3.5   # PAL 계산을 위한 운동별 가중치 값
    elif exerciseReq == "2번": 
        exercise = "실외 또는 실내 천천히 달리기"
        exerciseWeight = 7
    elif exerciseReq == "3번": 
        exercise = "실외 또는 실내 빨리 달리기"
        exerciseWeight = 8.3
    elif exerciseReq == "4번": 
        exercise = "등산"
        exerciseWeight = 6.5
    elif exerciseReq == "5번": 
        exercise = "야외 또는 실내 자전거 타기"
        exerciseWeight = 7.3
    elif exerciseReq == "6번": 
        exercise = "테니스, 스쿼시, 라켓볼"
        exerciseWeight = 5.8
    elif exerciseReq == "7번": 
        exercise = "수영"
        exerciseWeight = 6.4
    elif exerciseReq == "8번": 
        exercise = "에어로빅, 댄스"
        exerciseWeight = 4.8
    elif exerciseReq == "9번": 
        exercise = "골프"
        exerciseWeight = 7
    elif exerciseReq == "10번": 
        exercise = "스키"
        exerciseWeight = 3.8
    elif exerciseReq == "11번": 
        exercise = "볼링"
        exerciseWeight = 4
    elif exerciseReq == "12번": 
        exercise = "탁구"
        exerciseWeight = 5.5
    elif exerciseReq == "13번": 
        exercise = "배드민턴"
        exerciseWeight = 2.4
    elif exerciseReq == "14번": 
        exercise = "요가, 스트레칭"
        exerciseWeight = 3.5
    elif exerciseReq == "15번": 
        exercise = "웨이트 트레이닝"
        exerciseWeight = 3.8
    elif exerciseReq == "16번": 
        exercise = "윗몸 일으키기"
        exerciseWeight = 3.8
    elif exerciseReq == "17번": 
        exercise = "팔굽혀펴기"
        exerciseWeight = 3.8
    elif exerciseReq == "18번": 
        exercise = "줄넘기"
        exerciseWeight = 8.8
    elif exerciseReq == "19번": 
        exercise = "아이스 스케이팅"
        exerciseWeight = 7
    elif exerciseReq == "20번": 
        exercise = "롤러 스케이팅"
        exerciseWeight = 7
    elif exerciseReq == "21번": 
        exercise = "태권도, 유도, 가라데 등의 무술"
        exerciseWeight = 10.3
    elif exerciseReq == "22번": 
        exercise = "태극권, 기체조"
        exerciseWeight = 3
    elif exerciseReq == "23번": 
        exercise = "단전호흡, 명상"
        exerciseWeight = 1
    elif exerciseReq == "24번": 
        exercise = "복싱, 다이어트 복싱"
        exerciseWeight = 10.3
    elif exerciseReq == "25번": 
        exercise = "아쿠아로빅"
        exerciseWeight = 5.3

    user_dict[user_id].exercise = exercise
    user_dict[user_id].exerciseWeight = exerciseWeight


    res = {
        "version" : "2.0",
        "template":{
            "outputs": [
                    {
                        "simpleText": {
                            "text" : "입력하신 번호는 " + exerciseReq + "이므로, 선택 운동은 " + exercise + "입니다.\n\n해당 운동의 1회 운동 시간을 입력해주세요. \n먼저 시간 단위를 선택해주세요 \nex) 1시간20분 -> 1시간 \nex) 0시간30분 -> 0시간"
                        }
                    }
                ], "quickReplies": [
                    {
                        "messageText" : "0시간",
                        "action": "message",
                        "label" : "0시간"
                    },{
                        "messageText" : "1시간",
                        "action": "message",
                        "label" : "1시간"
                    },{
                        "messageText" : "2시간",
                        "action": "message",
                        "label" : "2시간"
                    },{
                        "messageText" : "3시간",
                        "action": "message",
                        "label" : "3시간"
                    },{
                        "messageText" : "4시간",
                        "action": "message",
                        "label" : "4시간"
                    },{
                        "messageText" : "5시간",
                        "action": "message",
                        "label" : "5시간"
                    }
                ]
        }
    }

    print(user_dict[user_id])
    return jsonify(res)


@app.route("/getExerciseTimeHour", methods = ["GET", "POST"]) 
def getExerciseTimeHour():
    print("1회 운동 시간 (시간 단위) 정보 받는 함수")
    req = request.get_json()

    # print(req)

    user_id = req["userRequest"]["user"]["id"]
    exerciseTimeHour =  req["action"]["detailParams"]["운동시간"]["value"] #1회 운동 시간(시간단위)
    user_dict[user_id].exerciseTimeHour = exerciseTimeHour
    res = {

        "version" : "2.0",
        "template":{
            "outputs": [
                    {
                        "simpleText": {
                            "text" : "입력하신 1회 운동 시간은 " + exerciseTimeHour + "입니다.\n\n분 단위를 선택해주세요.\nex) 1시간20분 -> 20분 \nex) 0시간30분 -> 30분 "
                        }
                    }
                ], "quickReplies": [
                    {
                        "messageText" : "0분",
                        "action": "message",
                        "label" : "0분"
                    },{
                        "messageText" : "5분",
                        "action": "message",
                        "label" : "5분"
                    },{
                        "messageText" : "10분",
                        "action": "message",
                        "label" : "10분"
                    },{
                        "messageText" : "20분",
                        "action": "message",
                        "label" : "20분"
                    },{
                        "messageText" : "30분",
                        "action": "message",
                        "label" : "30분"
                    },{
                        "messageText" : "40분",
                        "action": "message",
                        "label" : "40분"
                    },{
                        "messageText" : "50분",
                        "action": "message",
                        "label" : "50분"
                    }
                ]
        }
    }

    print(user_dict[user_id])
    return jsonify(res)

@app.route("/getExerciseTimeMin", methods = ["GET", "POST"]) 
def getExerciseTimeMin():
    print("1회 운동 시간 (분단위) 정보 받는 함수")
    req = request.get_json()

    # print(req)

    user_id = req["userRequest"]["user"]["id"]
    exerciseTimeMin =  req["action"]["detailParams"]["운동분"]["value"] #1회 운동 시간(분단위)
    user_dict[user_id].exerciseTimeMin = exerciseTimeMin

    res = {

        "version" : "2.0",
        "template":{
            "outputs": [
                    {
                        "simpleText": {
                            "text" : "입력하신 총 시간은 " + user_dict[user_id].exerciseTimeHour + exerciseTimeMin + "입니다.\n\n해당 운동의 주간 운동 횟수를 선택해 주세요."
                        }
                    }
                ], "quickReplies": [
                    {
                        "messageText" : "1회",
                        "action": "message",
                        "label" : "1회"
                    },{
                        "messageText" : "2회",
                        "action": "message",
                        "label" : "2회"
                    },{
                        "messageText" : "3회",
                        "action": "message",
                        "label" : "3회"
                    },{
                        "messageText" : "4회",
                        "action": "message",
                        "label" : "4회"
                    },{
                        "messageText" : "5회",
                        "action": "message",
                        "label" : "5회"
                    },{
                        "messageText" : "6회",
                        "action": "message",
                        "label" : "6회"
                    },{
                        "messageText" : "7회",
                        "action": "message",
                        "label" : "7회"
                    }
                ]
        }
    }

    return jsonify(res)

@app.route("/getExerciseNum", methods = ["GET", "POST"]) 
def getExerciseNum():
    print("주당 운동 횟수 정보 받는 함수")
    req = request.get_json()
    # print(req)

    user_id = req["userRequest"]["user"]["id"]
    exerciseNum =  req["action"]["detailParams"]["횟수"]["value"] #주당 운동 횟수
    print(exerciseNum)
    user_dict[user_id].exerciseNum = exerciseNum

    exerciseTime = user_dict[user_id].exerciseTimeHour + user_dict[user_id].exerciseTimeMin
    user_dict[user_id].exerciseTime = exerciseTime

    res = {
            "version" : "2.0",
            "template":{
                "outputs": [
                    {
                        "itemCard": {
                            "title": str(user_dict[user_id].exerciseIdx+1) + "번째 운동 정보",
                            "description": "입력된 정보를 확인해 주세요.\n맞으면 '맞습니다', 정보가 틀리면 '재입력'을 눌러 다시 진행해주세요.",
                            "itemList": [
                                {
                                    "title": "운동",
                                    "description": user_dict[user_id].exercise
                                },
                                {
                                    "title": "1회운동시간",
                                    "description": exerciseTime
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
                                    "messageText": "운동확인"
                                },
                                {
                                    "action":  "message",
                                    "label": "재입력",
                                    "messageText": "운동이미지"
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


@app.route("/getExerciseCheck", methods = ["GET", "POST"]) 
def getExerciseCheck():
    print("입력받은 운동 정보가 맞는지 확인하고 인덱스를 증가시키는 함수")
    req = request.get_json()
    # print(req)

    user_id = req["userRequest"]["user"]["id"]

    user_dict[user_id].exerciseIdx+=1
    #print(user_dict[user_id].exerciseIdx)
    #print(user_dict[user_id].exerciseTypeNum)

    user_dict[user_id].survey.exercise.append(user_dict[user_id].exercise)
    user_dict[user_id].survey.exerciseTime.append(user_dict[user_id].exerciseTime)
    user_dict[user_id].survey.exerciseNum.append(user_dict[user_id].exerciseNum)
    #print(user_dict[user_id].survey.exercise)
    #print(user_dict[user_id].survey.exerciseTime)
    #print(user_dict[user_id].survey.exerciseNum)

    if user_dict[user_id].exerciseIdx==user_dict[user_id].exerciseTypeNum:
        # print('if 들어옴')

        res = {
            "version" : "2.0",
            "template":{
                "outputs": [
                    {
                        "simpleText": {
                            "text" : "운동조사를 종료합니다.\n식품섭취빈도조사를 시작하려면 '시작하기' 버튼을 눌러주세요."
                        }
                    }
                ], "quickReplies": [
                    {
                        "messageText" : "식품섭취빈도조사",
                        "action": "message",
                        "label" : "시작하기"
                    }
                ]
            }
        }
        
    else:
        res = {
            "version" : "2.0",
            "template":{
                "outputs": [
                    {
                        "simpleText": {
                            "text" : str(user_dict[user_id].exerciseIdx) + "번째 운동조사가 완료되었습니다.\n추가 운동 입력을 위해 '추가운동입력' 버튼을 눌러주세요."
                        }
                    }
                ], "quickReplies": [
                    {
                        "messageText" : "운동이미지",
                        "action": "message",
                        "label" : "추가운동입력"
                    }
                ]
            }
        }
    
    exerciseTimeHour = int(user_dict[user_id].exerciseTimeHour.replace("시간",""))
    exerciseTimeMin = int(user_dict[user_id].exerciseTimeMin.replace("분",""))
    exerciseNum = int(user_dict[user_id].exerciseNum.replace("회",""))

    exerciseTimeTotal = (exerciseTimeHour*60 + exerciseTimeMin)*exerciseNum

    if user_dict[user_id].gender == '남자' :
        BEE = 293 - (3.8*user_dict[user_id].age) + (456.4*(user_dict[user_id].height/100)) + (10.12*user_dict[user_id].weight)
    elif user_dict[user_id].gender == '여자' :
        BEE = 247 - (2.67*user_dict[user_id].age) + (401.5*(user_dict[user_id].height/100)) + (8.6*user_dict[user_id].weight)

    PAL = ((user_dict[user_id].exerciseWeight-1) * ((1.15/0.9)*exerciseTimeTotal)/1440*7) / (BEE*7/(0.0175*1440*user_dict[user_id].weight))

    user_dict[user_id].PAL += PAL
   
    print(user_dict[user_id])
    print("운동 이름 : " + str(user_dict[user_id].exercise) + "운동 시간 (분으로 계산) : " + str(exerciseTimeTotal) + "BEE : " + str(BEE) + "PAL, PAL합 : " + str(PAL) + str(user_dict[user_id].PAL))
    return jsonify(res)


@app.route("/getNutriNum", methods = ["GET", "POST"]) 
def getNutriNum():
    print("영양제 가짓수 받는 함수")
    req = request.get_json()

    # print(req)

    user_id = req["userRequest"]["user"]["id"]
    nutriReq =  req["action"]["detailParams"]["nutriNum"]["value"] #영양제 종류(개수)
    # print(nutriReq)

    nutriTypeNum = int(nutriReq.replace("가지","")) #nutritype to num for loop
    # print(nutriTypeNum)

    user_dict[user_id].nutriTypeNum = nutriTypeNum

    res = {
            "version" : "2.0",
            "template":{
                "outputs": [
                    {
                        "simpleText": {
                            "text" : "섭취하신 식이보충제가 " + str(user_dict[user_id].nutriTypeNum) + "가지가 맞는지 확인해 주세요.\n\n맞으면 '맞습니다', 정보가 틀리면 '재입력'을 눌러 다시 진행해주세요."
                        }
                    }
                ], "quickReplies": [
                    {
                        "messageText" : "영양제이름",
                        "action": "message",
                        "label" : "맞습니다"
                    },{
                        "messageText" : "영양제종류입력",
                        "action": "message",
                        "label" : "재입력"
                    }
                ]
            }
        }    

    print(user_dict[user_id])
    print("영양제 개수 : ", nutriTypeNum)
    return jsonify(res)


@app.route("/getNutri", methods = ["GET", "POST"]) 
def getNutri():
    print("영양제 이름, 제조회사, 복용기간, 복용빈도, 복용분량 받는 함수")
    
    req = request.get_json()
    # print(req)
    user_id = req["userRequest"]["user"]["id"]


    nutriSupplement =  req["action"]["detailParams"]["nutri"]["value"] #영양제 이름
    nutriCompany = req["action"]["detailParams"]["nutriCompany"]["value"]
    nutriTerm = req["action"]["detailParams"]["nutriTerm"]["value"]
    nutriFrequency = req["action"]["detailParams"]["nutriFrequency"]["value"]
    nutriIntake = req["action"]["detailParams"]["nutriIntake"]["value"]

    print(nutriSupplement, nutriCompany, nutriTerm, nutriFrequency, nutriIntake)
    
    user_dict[user_id].nutriSupplement = nutriSupplement
    user_dict[user_id].nutriCompany = nutriCompany
    user_dict[user_id].nutriTerm = nutriTerm
    user_dict[user_id].nutriFrequency = nutriFrequency
    user_dict[user_id].nutriIntake = nutriIntake


    res = {
        "version" : "2.0",
        "template":{
            "outputs": [
                {
                    "itemCard": {
                        "title": str(user_dict[user_id].nutriIdx+1) + "번째 식이보충제 정보",
                        "description": "입력된 정보를 확인해 주세요.\n맞으면 '맞습니다', 정보가 틀리면 '재입력'을 눌러 다시 진행해주세요.",
                        "itemList": [
                            {
                                "title": "제품명",
                                "description": user_dict[user_id].nutriSupplement
                            },
                            {
                                "title": "제조회사",
                                "description": user_dict[user_id].nutriCompany
                            },
                            {
                                "title": "복용기간",
                                "description": user_dict[user_id].nutriTerm
                            },
                            {
                                "title": "복용빈도",
                                "description": user_dict[user_id].nutriFrequency
                            },
                            {
                                "title": "1회 복용분량",
                                "description": user_dict[user_id].nutriIntake
                            }
                        ],
                        "itemListAlignment" : "left",
                        "buttons": [
                            {
                                "action": "message",
                                "label": "맞습니다",
                                "messageText": "영양제사진전송"
                            },
                            {
                                "action":  "message",
                                "label": "재입력",
                                "messageText": "영양제이름"
                            }
                        ],
                        "buttonLayout" : "vertical"
                    }
                }
            ]
        }
    }

    print(user_dict[user_id])
    print("제품명 : " + str(user_dict[user_id].nutriSupplement) + "제조회사 : " + str(user_dict[user_id].nutriCompany) + "복용기간 : " + str(user_dict[user_id].nutriTerm) + "복용빈도 : " + str(user_dict[user_id].nutriFrequency) + "1회 복용분량 : " + str(user_dict[user_id].nutriIntake))
    return jsonify(res)


@app.route("/getNutriIndex", methods = ["GET", "POST"]) 
def getNutriIndex():
    print("입력받은 식이보충제 정보가 맞을 경우 인덱스를 증가시키는 함수")
    req = request.get_json()
    # print(req)

    user_id = req["userRequest"]["user"]["id"]

    user_dict[user_id].nutriIdx+=1
    print(user_dict[user_id].nutriIdx)
    print(user_dict[user_id].nutriTypeNum)

    user_dict[user_id].survey.nutriSupplement.append(user_dict[user_id].nutriSupplement)
    user_dict[user_id].survey.nutriCompany.append(user_dict[user_id].nutriCompany)
    user_dict[user_id].survey.nutriTerm.append(user_dict[user_id].nutriTerm)
    user_dict[user_id].survey.nutriFrequency.append(user_dict[user_id].nutriFrequency)
    user_dict[user_id].survey.nutriIntake.append(user_dict[user_id].nutriIntake)

    if user_dict[user_id].nutriIdx==user_dict[user_id].nutriTypeNum:
        add_nutri_result_to_excel(user_dict[user_id], user_id)

        res = {
            "version" : "2.0",
            "template":{
                "outputs": [
                    {
                        "simpleText": {
                            "text" : "식이보충제 조사를 종료합니다.\n모든 문항에 대한 검사가 완료되었습니다.\n감사합니다.\n\n결과 집계까지 시간이 소요되니 잠시 기다려주세요."
                        }
                    }
                ], "quickReplies": [
                    {
                        "messageText" : "1년섭취빈도조사종료",
                        "action": "message",
                        "label" : "종료"
                    }
                ]
            }
        }
    else:
        res = {
            "version" : "2.0",
            "template":{
                "outputs": [
                    {
                        "simpleText": {
                            "text" : str(user_dict[user_id].nutriIdx) + "번째 식이보충제 조사가 완료되었습니다.\n추가 식이보충제 입력을 위해 '추가식이보충제입력' 버튼을 눌러주세요."
                        }
                    }
                ], "quickReplies": [
                    {
                        "messageText" : "영양제이름",
                        "action": "message",
                        "label" : "추가식이보충제입력"
                    }
                ]
            }
        }
        
    print(user_dict[user_id])
    return jsonify(res)


import urllib.request
import requests
from PIL import Image

# 사진 전송 요구 + 사진 클라우드 링크 받아오는 함수 
@app.route("/getNutriPhoto", methods=["GET", "POST"])
def getnutriPhoto():
    print("식이보충제 사진을 받는 함수")
    
    req = request.get_json()
    # print(req)

    user_id = req["userRequest"]["user"]["id"]

    # photo_type = req["action"]["detailParams"]["image"]["value"]
    nutri_photo_type = req["action"]["detailParams"]["nutriImage"]['value']
    nutri_photo_json = json.loads(nutri_photo_type) # JSON 문자열을 Python 객체로 변환

    nutri_photo_url = nutri_photo_json["secureUrls"]
    nutri_u = nutri_photo_url[5:-1] # List( 자름
    # print(nutri_u)


    class AppURLopener(urllib.request.FancyURLopener):
        version = "Mozilla/5.0"
        
    urllib._urlopener = AppURLopener()

    img_path = "/home/user/jiyoung/share_data/pictures/" + str(datetime.now()) + user_dict[user_id].user_name
    # img_path = user_dict[user_id].user_name + str(datetime.now())

    urllib._urlopener.retrieve(nutri_u, img_path + ".jpg")
    # urlretrieve_img = Image.open("test.jpg") # 저장된 이미지 확인

    # upload = {'image': open('/home/user/jiyoung/flask/test.jpg', 'rb')} # 업로드하기위한 파일


    res = {
              "version": "2.0",
              "template": {
                "outputs": [
                  {
                    "simpleText": {
                       "text": "식이보충제 사진 전송이 완료되었습니다.\n사진전송완료 버튼을 눌러주세요."
                     }
                   }
                 ],
                  "quickReplies": [
                     {
                       "messageText": "영양제확인",
                       "action": "message",
                       "label": "사진전송완료"
                      }
                   ]
                 }
               }

    print(user_dict[user_id])
    return res


# ---------------------------------------식품섭취 빈도 시작 -----------------------------------------------

import constant

milkType4Solution = 0
fruitTypeWeight = 0

foodListForSurvey = list(식이빈도조사_음식섭취양.find().sort("순서" , 1)) # DB 순서가 바뀌지 않도록 정렬
# print(foodListForSurvey)

@app.route("/get1Frequency", methods = ["GET", "POST"])
def get1Frequency():

    print("일반음식, 우유, 과일, 술 별로 1년 섭취 빈도를 응답하고, 평균 섭취양 받는 함수")

    global milkType4Solution
    
    req = request.get_json()
    # print(req)
    user_id = req["userRequest"]["user"]["id"]

    nowFood = ''
    idx = user_dict[user_id].survey.idx

    if idx == 0:
        print("새로운 읍식 섭취 빈도 조사 시작")
        nowFood = foodListForSurvey[user_dict[user_id].survey.idx]

        return getFrequencyofRice(idx)

    else:
        reqEntity = req["action"]["detailParams"]["섭취양선택지"]["value"]

        if reqEntity == '돌아가기':
            print("돌아가기 선택")            

            if idx == 86: # 액상요구르트에서 돌아가기 누르는 경우
                getMilkBefore(user_id)
            else: # 일반적인 경우
                user_dict[user_id].survey.idx -= 1
                idx = user_dict[user_id].survey.idx

                beforeFood = foodListForSurvey[user_dict[user_id].survey.idx]
                dbResult = str(식이빈도조사_음식섭취양.find_one({"음식종류" : beforeFood ["음식종류"]},{"_id" : False, "음식종류" : False})).split("'")
                # print(dbResult)

                frequencyPerDay = user_dict[user_id].survey.foodFrequency[idx]
                portion = user_dict[user_id].survey.foodEntity[idx]
                weightval = dbResult[19]

                calculateSolutionBefore(user_id, frequencyPerDay = frequencyPerDay, portion= portion, foodName= beforeFood['음식종류'], weightval = weightval)

        idx = user_dict[user_id].survey.idx
        if idx == 2 or (idx >= 4 and idx <= 82) or (idx >= 87 and idx <= 88) or (idx >= 103 and idx <= 114): # 일반 음식 (쌀밥, 잡곡밥, 김밥, 우유, 과일, 커피, 술이 아닐때)

            beforeFood = foodListForSurvey[user_dict[user_id].survey.idx-1]

            reqEntity = req["action"]["detailParams"]["섭취양선택지"]["value"]
            dbResult = str(식이빈도조사_음식섭취양.find_one({"음식종류" : beforeFood ["음식종류"]},{"_id" : False, "음식종류" : False})).split("'")

            if reqEntity == '빈도선택1':
                user_dict[user_id].survey.foodEntity.append(dbResult[3])
                portion = dbResult[3]
            elif reqEntity == '빈도선택2':
                user_dict[user_id].survey.foodEntity.append(dbResult[7])
                portion = dbResult[7]
            elif reqEntity == '빈도선택3':
                user_dict[user_id].survey.foodEntity.append(dbResult[11])
                portion = dbResult[11]
            elif reqEntity == '빈도선택4':
                user_dict[user_id].survey.foodEntity.append("2")
                portion = "2"
            weightval = dbResult[19]
            #print(weightval)
            
            frequencyPerDay = user_dict[user_id].survey.foodFrequency[idx-1]

            if reqEntity != '돌아가기':
                print("음식종류, 섭취빈도, 섭취양 : ",beforeFood['음식종류'], frequencyPerDay, portion)
                calculateSolution(user_id, frequencyPerDay = frequencyPerDay, portion= portion, foodName= beforeFood['음식종류'], weightval = weightval)

            return getFrequencyofGeneral(idx)
        
        elif idx ==0 or idx == 1 or idx == 3: # 쌀밥, 잡곡밥, 김밥일 때
            beforeFood = foodListForSurvey[user_dict[user_id].survey.idx-1]

            reqEntity = req["action"]["detailParams"]["섭취양선택지"]["value"]
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
            elif reqEntity == '빈도선택4':
                user_dict[user_id].survey.foodEntity.append("2")
                portion = "2" 
            weightval = dbResult[19]
            #print(weightval)
            
            if idx != 0:
                frequencyPerDay = user_dict[user_id].survey.foodFrequency[idx-1]

            if reqEntity != '돌아가기':
                print("음식종류, 섭취빈도, 섭취양 : ",beforeFood['음식종류'], frequencyPerDay, portion)
                calculateSolution(user_id, frequencyPerDay = frequencyPerDay, portion= portion, foodName= beforeFood['음식종류'], weightval = weightval)

            return getFrequencyofRice(idx)

        elif idx == 83: # 우유일 때
            beforeFood = foodListForSurvey[user_dict[user_id].survey.idx-1]

            reqEntity = req["action"]["detailParams"]["섭취양선택지"]["value"]
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
            weightval = dbResult[19]
            #print(weightval)
            
            frequencyPerDay = user_dict[user_id].survey.foodFrequency[idx-1]

            if reqEntity != '돌아가기':
                print("음식종류, 섭취빈도, 섭취양 : ",beforeFood['음식종류'], frequencyPerDay, portion)
                calculateSolution(user_id, frequencyPerDay = frequencyPerDay, portion= portion, foodName= beforeFood['음식종류'], weightval = weightval)

            return getMilkType()

        elif idx == 86 : # 솔루션 계산을 위해 따로 계산 
            
            milkType4Solution = user_dict[user_id].survey.milkType4Solution
            beforeFoodIdx = 86 - milkType4Solution
            beforeFood = foodListForSurvey[beforeFoodIdx] # 선택한 우유일 때만 솔루션 계산
            print(milkType4Solution, beforeFoodIdx, beforeFood)
            #print(milkType4Solution)
            #print("beforefoodindex: ",beforeFoodIndex)

            reqEntity = req["action"]["detailParams"]["섭취양선택지"]["value"]
            dbResult = str(식이빈도조사_음식섭취양.find_one({"음식종류" : beforeFood ["음식종류"]},{"_id" : False, "음식종류" : False})).split("'")

            if reqEntity == '빈도선택1':
                user_dict[user_id].survey.foodEntity.append(dbResult[3])
                # user_dict[user_id].survey.foodEntity[beforeFoodIndex] = dbResult[3]
                portion = dbResult[3]
            elif reqEntity == '빈도선택2' :
                user_dict[user_id].survey.foodEntity.append(dbResult[7])
                portion = dbResult[7]
            elif reqEntity == '빈도선택3':
                user_dict[user_id].survey.foodEntity.append(dbResult[11])
                portion = dbResult[11]
            weightval = dbResult[19]
            #print(weightval)
            
            if beforeFoodIdx == 83:  # 일반우유
                user_dict[user_id].survey.foodEntity.append(0)
                user_dict[user_id].survey.foodEntity.append(0)
            elif beforeFoodIdx == 84: # 저지방우유
                user_dict[user_id].survey.foodEntity.append(0)

            print("우유 종류 : ", beforeFood)
            print("우유 frequency 저장 값 : ", user_dict[user_id].survey.foodFrequency[83], user_dict[user_id].survey.foodFrequency[84], user_dict[user_id].survey.foodFrequency[85])
            print("우유 entity 저장 값 : ", user_dict[user_id].survey.foodEntity[83], user_dict[user_id].survey.foodEntity[84], user_dict[user_id].survey.foodEntity[85])
            
            frequencyPerDay = user_dict[user_id].survey.milkFrequency
            user_dict[user_id].survey.milkEntity = portion
        
            if reqEntity != '돌아가기':
                print("음식종류, 섭취빈도, 섭취양 : ",beforeFood['음식종류'], frequencyPerDay, portion)
                calculateSolution(user_id, frequencyPerDay = frequencyPerDay, portion= portion, foodName= beforeFood['음식종류'], weightval = weightval)

            return getFrequencyofGeneral(idx)

        elif idx >= 89 and idx <= 101: # 과일 경우

            beforeFood = foodListForSurvey[user_dict[user_id].survey.idx-1]

            reqEntity = req["action"]["detailParams"]["섭취양선택지"]["value"]
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
            weightval = dbResult[19]
            #print(weightval)
            
            frequencyPerDay = user_dict[user_id].survey.foodFrequency[idx-1]

            if reqEntity != '돌아가기':
                print("음식종류, 섭취빈도, 섭취양 : ",beforeFood['음식종류'], frequencyPerDay, portion)
                calculateSolution(user_id, frequencyPerDay = frequencyPerDay, portion= portion, foodName= beforeFood['음식종류'], weightval = weightval)

            return getFruitType(idx)

        elif idx == 102: # 커피일 때
            beforeFood = foodListForSurvey[user_dict[user_id].survey.idx-1]

            reqEntity = req["action"]["detailParams"]["섭취양선택지"]["value"]
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

            weightval = dbResult[19]
            #print(weightval)
            
            frequencyPerDay = user_dict[user_id].survey.foodFrequency[idx-1]

            if reqEntity != '돌아가기':
                print("음식종류, 섭취빈도, 섭취양 : ",beforeFood['음식종류'], frequencyPerDay, portion)
                calculateSolution(user_id, frequencyPerDay = frequencyPerDay, portion= portion, foodName= beforeFood['음식종류'], weightval = weightval)

            return getFrequencyofCoffee(idx)


        elif idx >= 115: # 주류인 경우

            beforeFood = foodListForSurvey[user_dict[user_id].survey.idx-1]

            reqEntity = req["action"]["detailParams"]["섭취양선택지"]["value"]
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
            else:
                portion = calculateDrinkPortion(beforeFood ["음식종류"], reqEntity) # 각 주류 별로 초과 섭취량 portion 계산 필요
                user_dict[user_id].survey.foodEntity.append(portion)

            weightval = dbResult[19]
            #print(weightval)
            
            frequencyPerDay = user_dict[user_id].survey.foodFrequency[idx-1]

            if reqEntity != '돌아가기':
                print("음식종류, 섭취빈도, 섭취양 : ",beforeFood['음식종류'], frequencyPerDay, portion)
                calculateSolution(user_id, frequencyPerDay = frequencyPerDay, portion= portion, foodName= beforeFood['음식종류'], weightval = weightval)

            if user_dict[user_id].survey.idx == len(foodListForSurvey):
                # if user_dict[user_id].survey.idx == 4:
                    add_survey_result_to_excel2(user_dict[user_id], user_id)

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
                    
                    res = {
                        "version" : "2.0",
                        "template":{
                            "outputs": [
                                {
                                    "simpleText": {
                                        "text" : "식품 섭취 빈도 조사가 완료되었습니다.\n영양제 조사를 시작하려면 '영양제조사시작' 버튼을 눌러주세요."
                                    }
                                }
                            ], "quickReplies": [{
                                    "messageText" : "영양제",
                                    "action": "message",
                                    "label" : "영양제조사시작",
                                }
                            ]
                        }
                    }

                    return res

            return getFrequencyofDrink(idx)


def getFrequencyofGeneral(idx):

    req = request.get_json()
    user_id = req["userRequest"]["user"]["id"]

    # print(idx)
    nowFood = foodListForSurvey[user_dict[user_id].survey.idx]

    simpleText = "("+ str(idx+1) + "/119)'{foodName}'을(를) 최근 1년간 얼마나 자주 섭취했는지 선택해 주세요,\n선택지에 없을 경우, 최대한 비슷한 횟수를 선택해주세요.".format(foodName=nowFood["음식종류"])
    quickReplies = constant.GENERAL_FOOD_SURVEY_QUICKREPLIES

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


@app.route("/getGeneralEntity", methods = ["GET", "POST"])
def getGeneralEntity():

    global fruitTypeWeight

    fruitTypeWeight = 0 # 과일 가중치 계산 후 초기화 과정

    req = request.get_json()
    user_id = req["userRequest"]["user"]["id"]

    #print("1년 섭취 빈도 받기, 섭취량 시작 함수")
    frequency =  req["action"]["detailParams"]["식품섭취빈도조사선택지"]["value"] #식품섭취빈

    nowFood = foodListForSurvey[user_dict[user_id].survey.idx]
    beforeFood = foodListForSurvey[user_dict[user_id].survey.idx-1]

    dbResult = str(식이빈도조사_음식섭취양.find_one({"음식종류" : beforeFood ["음식종류"]},{"_id" : False, "음식종류" : False})).split("'")
    dbResult2 = str(식이빈도조사_음식섭취양.find_one({"음식종류" : nowFood ["음식종류"]},{"_id" : False, "음식종류" : False})).split("'")

    norm = dbResult2[23]
    #print("dbResult :\n\n", dbResult)

    simpleText = "선택하신 섭취 빈도는 {frequency} 입니다. \n'{foodName}'을(를) 1회 섭취하실 때, 평균 섭취량을 선택해 주세요.\n\n기준분량(1회 평균섭취량)은 \n\"{norm}\" 입니다. \n\n선택지에 없을 경우, 최대한 비슷한 횟수를 선택해주세요.".format(frequency = frequency, foodName=nowFood["음식종류"], norm = norm)
    quickReplies = makeQuickRepliesForFoodEntity(nowFood)
    frequencyPerDay = 0 # 하루 섭취량으로 변경

    
    if frequency == '거의 안 먹음':
        frequencyPerDay = 0
        simpleText = "선택하신 섭취 빈도는 {frequency} 입니다.\n다음 음식 조사를 위해 확인을 눌러주세요.".format(frequency = frequency)
        quickReplies = [{
                "messageText" : "빈도선택1",
                "action": "message",
                "label" : "확인"
            }]
    elif frequency == '1개월 1번':
        frequencyPerDay = 0.033
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

    #print(simpleText)
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

    user_dict[user_id].survey.idx += 1
    user_dict[user_id].survey.foodFrequency.append(frequencyPerDay)
    return res

def getFrequencyofRice(idx):
    req = request.get_json()
    user_id = req["userRequest"]["user"]["id"]

    nowFood = foodListForSurvey[user_dict[user_id].survey.idx]

    simpleText = "("+ str(idx+1) + "/119)'{foodName}'을(를) 최근 1년간 얼마나 자주 섭취했는지 선택해 주세요,\n선택지에 없을 경우, 최대한 비슷한 횟수를 선택해주세요.".format(foodName=nowFood["음식종류"])
    
    if idx == 0:
        quickReplies = constant.DEFAULT_RICE_FOOD_SURVEY_QUICKREPLIES
    else:
        quickReplies = constant.RICE_FOOD_SURVEY_QUICKREPLIES

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

@app.route("/getRiceEntity", methods = ["GET", "POST"])
def getRiceEntity():

    req = request.get_json()
    user_id = req["userRequest"]["user"]["id"]

    #print("1년 섭취 빈도 받기, 섭취량 시작 함수")
    frequency =  req["action"]["detailParams"]["밥빈도조사선택지"]["value"] #식품섭취빈도
    frequency = frequency.replace("밥 ","")


    nowFood = foodListForSurvey[user_dict[user_id].survey.idx]
    beforeFood = foodListForSurvey[user_dict[user_id].survey.idx-1]

    dbResult2 = str(식이빈도조사_음식섭취양.find_one({"음식종류" : nowFood ["음식종류"]},{"_id" : False, "음식종류" : False})).split("'")

    norm = dbResult2[23]
    #print("dbResult :\n\n", dbResult)

    simpleText = "선택하신 섭취 빈도는 {frequency} 입니다. \n'{foodName}'을(를) 1회 섭취하실 때, 평균 섭취량을 선택해 주세요.\n\n기준분량(1회 평균섭취량)은 \n\"{norm}\" 입니다. \n\n선택지에 없을 경우, 최대한 비슷한 횟수를 선택해주세요.".format(frequency = frequency, foodName=nowFood["음식종류"], norm = norm)
    quickReplies = makeQuickRepliesForAddFoodEntity(nowFood)

    frequencyPerDay = 0 # 하루 섭취량으로 변경

    if frequency == '거의 안 먹음':
        frequencyPerDay = 0
        simpleText = "선택하신 섭취 빈도는 {frequency} 입니다.\n다음 음식 조사를 위해 확인을 눌러주세요.".format(frequency = frequency)
        quickReplies = [{
                "messageText" : "빈도선택1",
                "action": "message",
                "label" : "확인"
            }]
    elif frequency == '1개월 1번':
        frequencyPerDay = 0.033
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

    #print(simpleText)
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

    user_dict[user_id].survey.idx += 1
    user_dict[user_id].survey.foodFrequency.append(frequencyPerDay)
    return res

def getMilkType():
    
    res = {
        "version" : "2.0",
        "template":{
            "outputs": [
                {
                    "simpleText": {
                        "text" : "평소 우유를 드실 때, 일반 우유와 저지방 우유 중 어떤 우유를 주로 드시는지 선택해주세요."
                    }
                }
            ], "quickReplies": [
                     {
                       "messageText": "일반우유",
                       "action": "message",
                       "label": "일반우유"
                      },{
                       "messageText": "저지방우유",
                       "action": "message",
                       "label": "저지방우유"
                      },{
                       "messageText": "반반",
                       "action": "message",
                       "label": "두가지를 비슷하게"
                      }
                   ]
        }
    }

    return res

@app.route("/getFrequencyofMilk", methods = ["GET", "POST"])
def getFrequencyofMilk():
    #print("우유 섭취빈도 시작 함수")

    req = request.get_json()
    user_id = req["userRequest"]["user"]["id"]

    milkType =  req["action"]["detailParams"]["우유종류"]["value"]
    print("우유종류 : ", milkType)

    if milkType =="일반우유":
        user_dict[user_id].survey.milkType4Solution = 3
    elif milkType == "저지방우유":
        user_dict[user_id].survey.idx += 1
        user_dict[user_id].survey.milkType4Solution = 2
        user_dict[user_id].survey.foodFrequency.append(0)
        user_dict[user_id].survey.foodEntity.append(0)
    elif milkType == "반반":
        user_dict[user_id].survey.idx += 2
        user_dict[user_id].survey.milkType4Solution = 1
        user_dict[user_id].survey.foodFrequency.append(0)
        user_dict[user_id].survey.foodFrequency.append(0)
        user_dict[user_id].survey.foodEntity.append(0)
        user_dict[user_id].survey.foodEntity.append(0)

    idx = user_dict[user_id].survey.idx

    nowFood = foodListForSurvey[user_dict[user_id].survey.idx]

    simpleText = "("+ str(idx+1) + "/119)'{foodName}'을(를) 최근 1년간 얼마나 자주 섭취했는지 선택해 주세요,\n선택지에 없을 경우, 최대한 비슷한 횟수를 선택해주세요.".format(foodName=nowFood["음식종류"])
    quickReplies = constant.MILK_FOOD_SURVEY_QUICKREPLIES

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

@app.route("/getMilkEntity", methods = ["GET", "POST"])
def getMilkEntity():

    req = request.get_json()
    user_id = req["userRequest"]["user"]["id"]

    #print("1년 우유 섭취 빈도 받기, 우유 섭취량 시작 함수")
    frequency =  req["action"]["detailParams"]["우유빈도조사선택지"]["value"] #우유섭취빈도
    frequency = frequency.replace("우유 ","")

    nowFood = foodListForSurvey[user_dict[user_id].survey.idx]
    beforeFood = foodListForSurvey[user_dict[user_id].survey.idx-1]

    dbResult2 = str(식이빈도조사_음식섭취양.find_one({"음식종류" : nowFood ["음식종류"]},{"_id" : False, "음식종류" : False})).split("'")

    norm = dbResult2[23]
    #print("dbResult :\n\n", dbResult2)

    simpleText = "선택하신 섭취 빈도는 {frequency} 입니다. \n'{foodName}'을(를) 1회 섭취하실 때, 평균 섭취량을 선택해 주세요.\n\n기준분량(1회 평균섭취량)은 \n\"{norm}\" 입니다. \n\n선택지에 없을 경우, 최대한 비슷한 횟수를 선택해주세요.".format(frequency = frequency, foodName=nowFood["음식종류"], norm = norm)
    #print(simpleText)
    quickReplies = makeQuickRepliesForFoodEntity(nowFood)

    frequencyPerDay = 0 # 하루 섭취량으로 변경

    if frequency == '거의 안 먹음':
        frequencyPerDay = 0
        simpleText = "선택하신 섭취 빈도는 {frequency} 입니다.\n다음 음식 조사를 위해 확인을 눌러주세요.".format(frequency = frequency)
        quickReplies = [{
                "messageText" : "빈도선택1",
                "action": "message",
                "label" : "확인"
            }]
    elif frequency == '1개월 1번':
        frequencyPerDay = 0.033
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

    user_dict[user_id].survey.foodFrequency.append(frequencyPerDay)
    user_dict[user_id].survey.milkFrequency = frequencyPerDay

    if user_dict[user_id].survey.idx == 83 : # 우유 다음 음식으로 인덱스값 조정, 일반우유
        user_dict[user_id].survey.idx += 3
        user_dict[user_id].survey.foodFrequency.append(0) # 다른 우유에 대해 엑셀값 0으로 지정
        user_dict[user_id].survey.foodFrequency.append(0)

    elif user_dict[user_id].survey.idx == 84: # 저지방우유
        user_dict[user_id].survey.idx += 2
        user_dict[user_id].survey.foodFrequency.append(0)

    elif user_dict[user_id].survey.idx == 85: # 반반우유
        user_dict[user_id].survey.idx += 1

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

def getMilkBefore(user_id):
    print("액상요구르트에서 돌아가기를 선택했을 때 인덱스 조정, 우유 계산 초기화 함수")

    solutionIdx = 0
    milkType4Solution = user_dict[user_id].survey.milkType4Solution
    
    user_dict[user_id].survey.idx -= 3 # 우유 종류 질문으로 돌아갈 수 있도록 인덱스 조정

    solutionIdx = 86 - milkType4Solution    

    beforeFood = foodListForSurvey[solutionIdx]
    dbResult = str(식이빈도조사_음식섭취양.find_one({"음식종류" : beforeFood ["음식종류"]},{"_id" : False, "음식종류" : False})).split("'")
    print(dbResult)

    frequencyPerDay = user_dict[user_id].survey.milkFrequency
    portion = user_dict[user_id].survey.milkEntity
    weightval = 1

    calculateSolutionBefore(user_id, frequencyPerDay = frequencyPerDay, portion= portion, foodName= beforeFood['음식종류'], weightval = weightval)


#@app.route("/getFruitType", methods = ["GET", "POST"])
def getFruitType(idx):

    req = request.get_json()
    user_id = req["userRequest"]["user"]["id"]

    nowFood = foodListForSurvey[user_dict[user_id].survey.idx]


    res = {
        "version" : "2.0",
        "template":{
            "outputs": [
                {
                    "simpleText": {
                             "text" :"'{foodName}'을(를) 주로 제철에 드시는지, 계절과 무관하게 드시는지 선택해주세요.".format(foodName=nowFood["음식종류"])
                    }
                }
            ], "quickReplies": [
                {
                    "messageText" : "제철",
                    "action": "message",
                    "label" : "제철"
                },{
                    "messageText" : "무관",
                    "action": "message",
                    "label" : "무관"
                }
            ]
        }
    }

    return res

@app.route("/getFrequencyofFruit", methods = ["GET", "POST"])
def getFrequencyofFruit():

    global fruitTypeWeight

    req = request.get_json()
    user_id = req["userRequest"]["user"]["id"]

    #print("과일 섭취빈도 시작 함수")
    fruitType =  req["action"]["detailParams"]["과일종류"]["value"]
    print("과일 제철/무관 선택 : ", fruitType)

    idx = user_dict[user_id].survey.idx
    nowFood = foodListForSurvey[user_dict[user_id].survey.idx]

    if fruitType == "제철":
        fruitTypeWeight = calculateFruitTypeWeight("제철", nowFood["음식종류"])
    elif fruitType == "무관":
        fruitTypeWeight = calculateFruitTypeWeight("무관", nowFood["음식종류"])
    
    print("과일 제철 시 가중치 값 : ", fruitTypeWeight)

    simpleText = "("+ str(idx+1) + "/119)'{foodName}'을(를) 최근 1년간 얼마나 자주 섭취했는지 선택해 주세요,\n선택지에 없을 경우, 최대한 비슷한 횟수를 선택해주세요.".format(foodName=nowFood["음식종류"])
    quickReplies = constant.FRUIT_FOOD_SURVEY_QUICKREPLIES

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

@app.route("/getFruitEntity", methods = ["GET", "POST"])
def getFruitEntity():

    req = request.get_json()
    user_id = req["userRequest"]["user"]["id"]

    #print("1년 과일 섭취 빈도 받기, 과일 섭취량 시작 함수")
    frequency =  req["action"]["detailParams"]["과일빈도조사선택지"]["value"] #과일섭취빈도
    frequency = frequency.replace("과일 ","")

    nowFood = foodListForSurvey[user_dict[user_id].survey.idx]
    beforeFood = foodListForSurvey[user_dict[user_id].survey.idx-1]

    dbResult = str(식이빈도조사_음식섭취양.find_one({"음식종류" : beforeFood ["음식종류"]},{"_id" : False, "음식종류" : False})).split("'")
    dbResult2 = str(식이빈도조사_음식섭취양.find_one({"음식종류" : nowFood ["음식종류"]},{"_id" : False, "음식종류" : False})).split("'")

    norm = dbResult2[23]
    #print("dbResult :", dbResult)

    simpleText = "선택하신 섭취 빈도는 {frequency} 입니다. \n'{foodName}'을(를) 1회 섭취하실 때, 평균 섭취량을 선택해 주세요.\n\n기준분량(1회 평균섭취량)은 \n\"{norm}\" 입니다. \n\n선택지에 없을 경우, 최대한 비슷한 횟수를 선택해주세요.".format(frequency = frequency, foodName=nowFood["음식종류"], norm = norm)
    #print(simpleText)

    quickReplies = makeQuickRepliesForFoodEntity(nowFood)
    frequencyPerDay = 0 # 하루 섭취량으로 변경

    if frequency == '거의 안 먹음':
        frequencyPerDay = 0
        simpleText = "선택하신 섭취 빈도는 {frequency} 입니다.\n다음 음식 조사를 위해 확인을 눌러주세요.".format(frequency = frequency)
        quickReplies = [{
                "messageText" : "빈도선택1",
                "action": "message",
                "label" : "확인"
            }]
    elif frequency == '1개월 1번':
        frequencyPerDay = 0.033
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

def getFrequencyofCoffee(idx):

    #print("1년 커피 빈도 시작")

    req = request.get_json()
    user_id = req["userRequest"]["user"]["id"]

    nowFood = foodListForSurvey[user_dict[user_id].survey.idx]

    simpleText = "("+ str(idx+1) + "/119)'{foodName}'을(를) 최근 1년간 얼마나 자주 섭취했는지 선택해 주세요.\n선택지에 없을 경우, 최대한 비슷한 횟수를 선택해주세요.\n*단, 커피를 1일 3회보다 자주 드셨다면, \"1일 3회 초과\"를 선택해주세요.".format(foodName=nowFood["음식종류"])
    quickReplies = constant.COFFEE_FOOD_SURVEY_QUICKREPLIES

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

@app.route("/getCoffeeOver", methods = ["GET", "POST"])
def getCoffeeOver():

    req = request.get_json()
    user_id = req["userRequest"]["user"]["id"]

    #print("커피 초과 섭취량 선택지 주는 함수")

    nowFood = foodListForSurvey[user_dict[user_id].survey.idx]

    foodname = nowFood["음식종류"]

    simpleText = foodname + "의 1일 섭취빈도를 선택해주세요."

    quickReplies = [
        {
            "messageText" : "커피 1일 4번",
            "action": "message",
            "label" : "1일 4번"
        },{
            "messageText" : "커피 1일 5번",
            "action": "message",
            "label" : "1일 5번"
        },{
            "messageText" : "커피 1일 6번",
            "action": "message",
            "label" : "1일 6번"
        },{
            "messageText" : "커피 1일 7번",
            "action": "message",
            "label" : "1일 7번"
        },{
            "messageText" : "커피 1일 8번",
            "action": "message",
            "label" : "1일 8번"
        }
    ]
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

@app.route("/getCoffeeEntity", methods = ["GET", "POST"])
def getCoffeeEntity():

    req = request.get_json()
    user_id = req["userRequest"]["user"]["id"]

    #print("1년 커피 섭취 빈도 받기, 커피 섭취량 시작 함수")
    frequency =  req["action"]["detailParams"]["커피빈도조사선택지"]["value"] #커피섭취빈도
    frequency = frequency.replace("커피 ","")

    nowFood = foodListForSurvey[user_dict[user_id].survey.idx]
    beforeFood = foodListForSurvey[user_dict[user_id].survey.idx-1]

    dbResult = str(식이빈도조사_음식섭취양.find_one({"음식종류" : beforeFood ["음식종류"]},{"_id" : False, "음식종류" : False})).split("'")
    dbResult2 = str(식이빈도조사_음식섭취양.find_one({"음식종류" : nowFood ["음식종류"]},{"_id" : False, "음식종류" : False})).split("'")

    norm = dbResult2[23]
    #print("dbResult :", dbResult)

    simpleText = "선택하신 섭취 빈도는 {frequency} 입니다. \n'{foodName}'을(를) 1회 섭취하실 때, 평균 섭취량을 선택해 주세요.\n\n기준분량(1회 평균섭취량)은 \n\"{norm}\" 입니다. \n\n선택지에 없을 경우, 최대한 비슷한 횟수를 선택해주세요.".format(frequency = frequency, foodName=nowFood["음식종류"], norm = norm)
    #print(simpleText)
    quickReplies = makeQuickRepliesForFoodEntity(nowFood)
    frequencyPerDay = 0 # 하루 섭취량으로 변경

    if frequency == '거의 안 먹음':
        frequencyPerDay = 0
        simpleText = "선택하신 섭취 빈도는 {frequency} 입니다.\n다음 음식 조사를 위해 확인을 눌러주세요.".format(frequency = frequency)
        quickReplies = [{
                "messageText" : "빈도선택1",
                "action": "message",
                "label" : "확인"
            }]
    elif frequency == '1개월 1번':
        frequencyPerDay = 0.033
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
    elif frequency == '1일 4번':
        frequencyPerDay = 4
    elif frequency == '1일 5번':
        frequencyPerDay = 5
    elif frequency == '1일 6번':
        frequencyPerDay = 6
    elif frequency == '1일 7번':
        frequencyPerDay = 7
    elif frequency == '1일 8번':
        frequencyPerDay = 8


    user_dict[user_id].survey.idx += 1

    user_dict[user_id].survey.foodFrequency.append(frequencyPerDay)

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

def getFrequencyofDrink(idx):

    req = request.get_json()
    user_id = req["userRequest"]["user"]["id"]

    nowFood = foodListForSurvey[user_dict[user_id].survey.idx]

    simpleText = "("+ str(idx+1) + "/119)'{foodName}'을(를) 최근 1년간 얼마나 자주 섭취했는지 선택해 주세요.\n선택지에 없을 경우, 최대한 비슷한 횟수를 선택해주세요.".format(foodName=nowFood["음식종류"])
    quickReplies = constant.DRINK_FOOD_SURVEY_QUICKREPLIES

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

@app.route("/getDrinkEntity", methods = ["GET", "POST"])
def getDrinkEntity():

    req = request.get_json()
    user_id = req["userRequest"]["user"]["id"]

    #print("1년 술 섭취 빈도 받기, 술 섭취량 시작 함수")
    frequency =  req["action"]["detailParams"]["술빈도조사선택지"]["value"] #술섭취빈도
    frequency = frequency.replace("술 ","")

    nowFood = foodListForSurvey[user_dict[user_id].survey.idx]
    beforeFood = foodListForSurvey[user_dict[user_id].survey.idx-1]

    dbResult = str(식이빈도조사_음식섭취양.find_one({"음식종류" : beforeFood ["음식종류"]},{"_id" : False, "음식종류" : False})).split("'")
    dbResult2 = str(식이빈도조사_음식섭취양.find_one({"음식종류" : nowFood ["음식종류"]},{"_id" : False, "음식종류" : False})).split("'")

    norm = dbResult2[23]
    #print("dbResult :", dbResult)

    simpleText = "선택하신 섭취 빈도는 {frequency} 입니다. \n'{foodName}'을(를) 1회 섭취하실 때, 평균 섭취량을 선택해 주세요.\n\n기준분량(1회 평균섭취량)은 \n\"{norm}\" 입니다. \n\n선택지에 없을 경우, 최대한 비슷한 횟수를 선택해주세요.".format(frequency = frequency, foodName=nowFood["음식종류"], norm = norm)
    #print(simpleText)
    quickReplies = makeQuickRepliesForDrinkEntity(nowFood)
    frequencyPerDay = 0 # 하루 섭취량으로 변경

    if frequency == '거의 안 먹음':
        frequencyPerDay = 0
        simpleText = "선택하신 섭취 빈도는 {frequency} 입니다.\n다음 음식 조사를 위해 확인을 눌러주세요.".format(frequency = frequency)
        quickReplies = [{
                "messageText" : "빈도선택1",
                "action": "message",
                "label" : "확인"
            }]
    elif frequency == '1개월 1번':
        frequencyPerDay = 0.033
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

@app.route("/getDrinkOver", methods = ["GET", "POST"])
def getDrinkOver():
    print("술 초과 섭취량 선택지 주는 함수")

    req = request.get_json()
    user_id = req["userRequest"]["user"]["id"]


    beforeFood = foodListForSurvey[user_dict[user_id].survey.idx-1]

    foodname = beforeFood["음식종류"]

    simpleText = foodname + "의 1회 평균 섭취량을 선택해주세요."
    if beforeFood["음식종류"] == "맥주":
        simpleText += "\n(맥주 1컵 = 200ml, 맥주 1병 = 500ml, 맥주 1병 = 2.5컵)"
    elif beforeFood["음식종류"] == "막걸리":
        simpleText += "\n(막걸리 1사발 = 210ml, 막걸리 1병 = 750ml, 막걸리 1병 -> 약 4사발, 막걸리 2병 -> 약 7사발, 막걸리 3병 -> 약 11사발)"
    elif beforeFood["음식종류"] == "포도주":
        simpleText += "\n(포도주 1병 = 750ml, 포도주 1병 = 6잔)"

    quickReplies = makeQuickRepliesForOverDrinkEntity(beforeFood)

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
# def add_survey_result_to_excel(user: SurveyUser):

#     now = str(datetime.now())
#     excel_row = []

#     excel_row.append(now)
#     for info in user.get_user_info():
#         excel_row.append(info)

#     for frequency, entity in zip(user.survey.foodFrequency, user.survey.foodFrequency):
#         excel_row.append(frequency)
#         excel_row.append(entity)

#     while len(excel_row) < 260:
#         excel_row.append("응답 없음")

#     df = None
#     df = pd.read_excel("./data/1년섭취빈도조사.xlsx", engine='openpyxl')
#     df = df.append(pd.Series(excel_row, index=df.columns) , ignore_index=True)
#     df.to_excel("./data/1년섭취빈도조사.xlsx", index=False)

def add_survey_result_to_excel2(user: SurveyUser, user_id):

    now = str(datetime.now())
    excel_row = []

    excel_row.append(now)
    for info in user.get_user_info():
        excel_row.append(info)
    
    print(excel_row)

    for frequency, entity in zip(user.survey.foodFrequency, user.survey.foodFrequency):
        excel_row.append(frequency)
        excel_row.append(entity)

    for name, time, number in zip(user.survey.exercise, user.survey.exerciseTime, user.survey.exerciseNum):
        excel_row.append(name)
        excel_row.append(time)
        excel_row.append(number)

    while len(excel_row) < 260:
        excel_row.append("응답 없음")

    df = None
    df = pd.read_excel("./data/1년섭취빈도조사_운동량포함_data.xlsx", engine='openpyxl')
    # print(df.columns)


    df = df.append(pd.Series(excel_row, index=df.columns) , ignore_index=True)
    df.to_excel("./data/1년섭취빈도조사_운동량포함_data.xlsx", index=False)


def add_nutri_result_to_excel(user: SurveyUser, user_id):

    now = str(datetime.now())
    excel_row = []

    excel_row.append(now)
    for info in user.get_user_info():
        excel_row.append(info)

    for name, company, term, frequency, intake in zip(user.survey.nutriSupplement, user.survey.nutriCompany, user.survey.nutriTerm,  user.survey.nutriFrequency,  user.survey.nutriIntake):
        excel_row.append(name)
        excel_row.append(company)
        excel_row.append(term)
        excel_row.append(frequency)
        excel_row.append(intake)

    while len(excel_row) < 42:
        excel_row.append("응답 없음")

    df2 = None
    df2 = pd.read_excel("/home/user/jiyoung/share_data/1년섭취빈도조사_식이보충제.xlsx", engine='openpyxl')
    df2 = df2.append(pd.Series(excel_row, index=df2.columns) , ignore_index=True)
    df2.to_excel("/home/user/jiyoung/share_data/1년섭취빈도조사_식이보충제.xlsx", index=False)


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

def makeQuickRepliesForAddFoodEntity(food): # 선택지가 4개인 음식(쌀밥, 잡곡밥, 김밥)
    quickReplies = []

    for k,v in food.items():
        if k == "선택1" or k == "선택2" or k == "선택3":
            quickReplies.append({
                "messageText" : "빈도{k}".format(k = k),
                "action": "message",
                "label" : "{v}{단위}".format(v = v, 단위=food["단위"])
            })

    quickReplies.append({
            "messageText" : "빈도선택4",
            "action": "message",
            "label" : "2{단위}".format(단위=food["단위"])
    })
    return quickReplies

def makeQuickRepliesForDrinkEntity(food):
    quickReplies = []

    for k,v in food.items():
        if k == "선택1" or k == "선택2" or k == "선택3":
            quickReplies.append({
                "messageText" : "빈도{k}".format(k = k),
                "action": "message",
                "label" : "{v}{단위}".format(v = v, 단위=food["단위"])
            })

    quickReplies.append({
            "messageText" : "초과",
            "action": "message",
            "label" : "초과"
            })


    return quickReplies

def makeQuickRepliesForOverDrinkEntity(food): # 주류별 초과 섭취양 quickreplies
   
    if food["음식종류"] == "소주":
        quickReplies = [{
            "messageText" : "1병 반",
            "action": "message",
            "label" : "1병 반"
            },{
            "messageText" : "2병",
            "action": "message",
            "label" : "2병"
            },{
            "messageText" : "2병 반",
            "action": "message",
            "label" : "2병 반"
            },{
            "messageText" : "3병",
            "action": "message",
            "label" : "3병"
            },{
            "messageText" : "3병 반",
            "action": "message",
            "label" : "3병 반"
            },{
            "messageText" : "4병",
            "action": "message",
            "label" : "4병"
            }

        ]

    elif food["음식종류"] == "맥주":
        quickReplies= [{
            "messageText" : "1병",
            "action": "message",
            "label" : "1병"
            },{
            "messageText" : "1병 반",
            "action": "message",
            "label" : "1병 반"
            },{
            "messageText" : "2병",
            "action": "message",
            "label" : "2병"
            },{
            "messageText" : "2병 반",
            "action": "message",
            "label" : "2병 반"
            },{
            "messageText" : "3병",
            "action": "message",
            "label" : "3병"
            },{
            "messageText" : "3병 반",
            "action": "message",
            "label" : "3병 반"
            },{
            "messageText" : "4병",
            "action": "message",
            "label" : "4병"
            },{
            "messageText" : "4병 반",
            "action": "message",
            "label" : "4병 반"
            },{
            "messageText" : "5병",
            "action": "message",
            "label" : "5병"
            }
        ]

    elif food["음식종류"] == "막걸리":
        quickReplies = [{
            "messageText" : "3사발",
            "action": "message",
            "label" : "3사발"
            },{
            "messageText" : "4사발",
            "action": "message",
            "label" : "4사발"
            },{
            "messageText" : "5사발",
            "action": "message",
            "label" : "5사발"
            },{
            "messageText" : "6사발",
            "action": "message",
            "label" : "6사발"
            },{
            "messageText" : "7사발",
            "action": "message",
            "label" : "7사발"
            },{
            "messageText" : "8사발",
            "action": "message",
            "label" : "8사발"
            },{
            "messageText" : "9사발",
            "action": "message",
            "label" : "9사발"
            },{
            "messageText" : "10사발",
            "action": "message",
            "label" : "10사발"
            },{
            "messageText" : "11사발",
            "action": "message",
            "label" : "11사발"
            }

        ]

    elif food["음식종류"] == "포도주":
        quickReplies = [{
            "messageText" : "3잔",
            "action": "message",
            "label" : "3잔"
            },{
            "messageText" : "4잔",
            "action": "message",
            "label" : "4잔"
            },{
            "messageText" : "5잔",
            "action": "message",
            "label" : "5잔"
            },{
            "messageText" : "6잔",
            "action": "message",
            "label" : "6잔"
            },{
            "messageText" : "7잔",
            "action": "message",
            "label" : "7잔"
            },{
            "messageText" : "8잔",
            "action": "message",
            "label" : "8잔"
            },{
            "messageText" : "9잔",
            "action": "message",
            "label" : "9잔"
            },{
            "messageText" : "10잔",
            "action": "message",
            "label" : "10잔"
            }

        ]


    return quickReplies

def calculateFruitTypeWeight(fruitType, fruitName): # 과일별 제철 섭취 시 가중치 값
    
    if fruitType == "제철":
        if fruitName == "딸기":
            return 2.43/12
        elif fruitName == "토마토, 방울토마토":
            return 4.39/12
        elif fruitName == "참외":
            return 2.73/12
        elif fruitName == "수박":
            return 2.29/12
        elif fruitName == "복숭아":
            return 2.08/12
        elif fruitName == "포도":
            return 2.21/12
        elif fruitName == "사과":
            return 4.51/12
        elif fruitName == "배":
            return 4.8/12
        elif fruitName == "감, 곶감":
            return 1.98/12
        elif fruitName == "귤":
            return 3.79/12
        elif fruitName == "바나나":
            return 5.25/12
        elif fruitName == "오렌지":
            return 2.71/12
        elif fruitName == "키위":
            return 3.44/12
    else:
        return 1
        
def calculateDrinkPortion(drinkName, reqEntity):

    if drinkName == "소주":
        if reqEntity == "1병 반":
            return "1.5"
        elif reqEntity == "2병":
            return "4"
        elif reqEntity == "2병 반":
            return "2.5"
        elif reqEntity == "3병":
            return "3"
        elif reqEntity == "3병 반":
            return "3.5"
        elif reqEntity == "4병":
            return "4"
    elif drinkName == "맥주":
        if reqEntity == "1병":
            return "2.5"
        elif reqEntity == "1병 반":
            return "3.75"
        elif reqEntity == "2병":
            return "5"
        elif reqEntity == "2병 반":
            return "6.25"
        elif reqEntity == "3병":
            return "7.5"
        elif reqEntity == "3병 반":
            return "8.75"
        elif reqEntity == "4병":
            return "10"
    elif drinkName == "막걸리":
        if reqEntity == "3사발":
            return "1.725"
        elif reqEntity == "4사발":
            return "2.3"
        elif reqEntity == "5사발":
            return "2.875"
        elif reqEntity == "6사발":
            return "3.45"
        elif reqEntity == "7사발":
            return "4.025"
        elif reqEntity == "8사발":
            return "4.6"
        elif reqEntity == "9사발":
            return "5.175"
        elif reqEntity == "10사발":
            return "5.75"
        elif reqEntity == "11사발":
            return "6.325"
    elif drinkName == "포도주":
        if reqEntity == "3잔":
            return "3"
        elif reqEntity == "4잔":
            return "4"
        elif reqEntity == "5잔":
            return "5"
        elif reqEntity == "6잔":
            return "6"
        elif reqEntity == "7잔":
            return "7"
        elif reqEntity == "8잔":
            return "8"
        elif reqEntity == "9잔":
            return "9"
        elif reqEntity == "10잔":
            return "10"
        

# 영양소 별 솔루션 계산 함수
def calculateSolution(user_id, frequencyPerDay, portion, foodName, weightval):
    dbResult = str(식이빈도조사_단위영양성분.find_one({"음식종류" : foodName},{"_id" : False, "음식종류" : False})).replace(':','').replace(',','').replace('}','').split("'")
    #print(dbResult)

    global fruitTypeWeight

    if fruitTypeWeight != 0:
        frequencyPerDay *= fruitTypeWeight

    # 솔루션을 위한 각 합 -> 이걸로 솔루션 제공 가능
    # print("soltuion", frequencyPerDay, portion, dbResult[2], weightval)
    칼로리 = frequencyPerDay * Fraction(portion) * float(dbResult[2]) * Fraction(weightval)
    user_dict[user_id].solution_칼로리 += 칼로리

    탄수화물 = frequencyPerDay * Fraction(portion) * float(dbResult[4]) * Fraction(weightval)
    user_dict[user_id].solution_탄수화물 += 탄수화물

    단백질 = frequencyPerDay * Fraction(portion) * float(dbResult[6]) * Fraction(weightval)
    user_dict[user_id].solution_단백질 += 단백질

    지방 = frequencyPerDay * Fraction(portion) * float(dbResult[8]) * Fraction(weightval)
    user_dict[user_id].solution_지방 += 지방
    
    나트륨 = frequencyPerDay * Fraction(portion) * float(dbResult[10]) * Fraction(weightval)
    user_dict[user_id].solution_나트륨 += 나트륨

    칼슘 = frequencyPerDay * Fraction(portion) * float(dbResult[12]) * Fraction(weightval)
    user_dict[user_id].solution_칼슘 += 칼슘

    비타민C = frequencyPerDay * Fraction(portion) * float(dbResult[14]) * Fraction(weightval)
    user_dict[user_id].solution_비타민C += 비타민C

    포화지방산 = frequencyPerDay * Fraction(portion) * float(dbResult[16])
    user_dict[user_id].solution_포화지방산 += 포화지방산
    user_dict[user_id].solution_포화지방산_상위.append([포화지방산, foodName])
    
    # print("칼로리 : " + str(frequencyPerDay * Fraction(portion) * float(dbResult[2]) * Fraction(weightval)))

    print(user_dict[user_id])

    print("\n<영양소 계산>")
    print("음식종류: ", foodName)
    print("칼로리, 탄수화물, 단백질, 지방, 나트륨, 칼슘, 비타민C, 포화지방산 :\n",칼로리,단백질,탄수화물,지방,나트륨,칼슘,비타민C,포화지방산)

    print("누적 - 칼로리, 탄수화물, 단백질, 지방, 나트륨, 칼슘, 비타민C, 포화지방산 :\n",user_dict[user_id].solution_칼로리, user_dict[user_id].solution_탄수화물, user_dict[user_id].solution_단백질, user_dict[user_id].solution_지방, user_dict[user_id].solution_나트륨, user_dict[user_id].solution_칼슘, user_dict[user_id].solution_비타민C,  user_dict[user_id].solution_포화지방산)


# 돌아가기 선택시 솔루션 값을 이전 값으로 조정하는 함수
def calculateSolutionBefore(user_id, frequencyPerDay, portion, foodName, weightval):
    dbResult = str(식이빈도조사_단위영양성분.find_one({"음식종류" : foodName},{"_id" : False, "음식종류" : False})).replace(':','').replace(',','').replace('}','').split("'")
    # print(dbResult)

    global fruitTypeWeight

    if fruitTypeWeight != 0:
        frequencyPerDay *= fruitTypeWeight

    # 솔루션을 위한 각 합 -> 이걸로 솔루션 제공 가능 
    # print("soltuion before", frequencyPerDay, portion, dbResult[2], weightval)
    칼로리 = frequencyPerDay * Fraction(portion) * float(dbResult[2]) * Fraction(weightval)
    user_dict[user_id].solution_칼로리 -= 칼로리

    탄수화물 = frequencyPerDay * Fraction(portion) * float(dbResult[4]) * Fraction(weightval)
    user_dict[user_id].solution_탄수화물 -= 탄수화물

    단백질 = frequencyPerDay * Fraction(portion) * float(dbResult[6]) * Fraction(weightval)
    user_dict[user_id].solution_단백질 -= 단백질

    지방 = frequencyPerDay * Fraction(portion) * float(dbResult[8]) * Fraction(weightval)
    user_dict[user_id].solution_지방 -= 지방
    
    나트륨 = frequencyPerDay * Fraction(portion) * float(dbResult[10]) * Fraction(weightval)
    user_dict[user_id].solution_나트륨-= 나트륨

    칼슘 = frequencyPerDay * Fraction(portion) * float(dbResult[12]) * Fraction(weightval)
    user_dict[user_id].solution_칼슘 -= 칼슘

    비타민C = frequencyPerDay * Fraction(portion) * float(dbResult[14]) * Fraction(weightval)
    user_dict[user_id].solution_비타민C -= 비타민C

    포화지방산 = frequencyPerDay * Fraction(portion) * float(dbResult[16])
    user_dict[user_id].solution_포화지방산 -= 포화지방산
    user_dict[user_id].solution_포화지방산_상위.pop()

    user_dict[user_id].survey.foodFrequency.pop()
    user_dict[user_id].survey.foodEntity.pop()

    if foodName == "일반우유" or foodName == "저지방우유" or foodName == "일반, 저지방우유 반반":
        user_dict[user_id].survey.foodFrequency.pop()
        user_dict[user_id].survey.foodFrequency.pop()
        user_dict[user_id].survey.foodEntity.pop()
        user_dict[user_id].survey.foodEntity.pop()
    
    print(user_dict[user_id])

    print("\n<돌아가기 선택 - 이전 영양소 계산값>")
    print("음식종류: ", foodName, frequencyPerDay, portion)
    print("칼로리, 탄수화물, 단백질, 지방, 나트륨, 칼슘, 비타민C, 포화지방산 :\n",칼로리,단백질,탄수화물,지방,나트륨,칼슘,비타민C,포화지방산)

    print("누적 - 칼로리, 탄수화물, 단백질, 지방, 나트륨, 칼슘, 비타민C, 포화지방산 :\n",user_dict[user_id].solution_칼로리, user_dict[user_id].solution_탄수화물, user_dict[user_id].solution_단백질, user_dict[user_id].solution_지방, user_dict[user_id].solution_나트륨, user_dict[user_id].solution_칼슘, user_dict[user_id].solution_비타민C,  user_dict[user_id].solution_포화지방산)


# 솔루션 그래프 + 줄글 제공
def provideSolution(user_id, energy, carbo, protein, fat, sodium, calcium, vitaminC, SFA):

    user_name = user_dict[user_id].user_name

    BMI = user_dict[user_id].weight / ((user_dict[user_id].height*0.01)**2)

    print("\n최종 - 칼로리, 탄수화물, 단백질, 지방, 나트륨, 칼슘, 비타민C, 포화지방산 :\n", energy, carbo, protein, fat, sodium, calcium, vitaminC, SFA)
    print("PAL , BMI : ",user_dict[user_id].PAL, BMI)

    first = [0, ""]
    second = [0, ""]

    for a in user_dict[user_id].solution_포화지방산_상위:
        if first[0] < a[0]:
            first = a
            continue
        if second[0] < a[0]:
            second = a
            continue

    firstSolution = "본 결과는 " + user_name + "님께서 기록하신 최근 1년 동안의 음식 섭취 빈도로 분석한 영양평가입니다. 식이보충제 정보는 반영되지 않았습니다.\n기록하신 최근 1년 동안의 식사섭취가 본인의 평소 식사와 같았는지 아니면 어떻게 달랐는지를 생각하면서 영양평가를 참고하시어 건강한 식생활을 유지하시기 바랍니다."
    print(firstSolution)

    secondSolution = "\n▶ 3대 열량영양소 섭취 비율입니다.\n한국인의 3대 열량 영양소의 권장 섭취 비율은 [탄수화물: 단백질: 지방 = 55-65: 7-20: 15-30] 입니다.\n귀하의 최근 1년 동안의 식품 섭취 빈도조사에 따른 평균 열량 영양소 섭취 비율은 다음과 같습니다."
    print(secondSolution)

    ratioSolution = calculateRatio(carbo, protein, fat)
    print(ratioSolution)

    thirdSolution = "\n▶ 영양소별 평가 결과입니다."
    print(thirdSolution)

    nutriSolution = ""
    intakeSolution = ""
    totalSolution = ""
    foodSolution = ""

    resultEnergy = calculateEnergy(user_id, energy)
    valEnergy = resultEnergy[1]
    energyPercent = resultEnergy[2]

    if resultEnergy[0] == "부족":
        nutriSolution += "- 열량 | " + str(round(energy)) + "kcal | 부족⬇️ : 열량은 에너지필요추정량(" + str(valEnergy) + "kcal)의 " + str(energyPercent) + "% 수준으로 부족하게 섭취하셨습니다.\n"
        if BMI < 27.5:
            intakeSolution += "- ⬆️식사량 늘리기\n"
            totalSolution += "평소에도 기록하신 것과 동일하게 식사하신다면 전체적인 식사량을 늘리시기 바랍니다.\n"
    elif resultEnergy[0] == "적절":
        nutriSolution += "- 열량 | " + str(round(energy)) + "kcal | 적절✅ : 열량은 에너지필요추정량(" + str(valEnergy) + "kcal)의 " + str(energyPercent) + "% 수준으로 적절하게 섭취하셨습니다.\n"
    elif resultEnergy[0] == "초과":
        nutriSolution += "- 열량 | " + str(round(energy)) + "kcal | 과다⬆️ : 열량은 에너지필요추정량(" + str(valEnergy) + "kcal)의 " + str(energyPercent) + "% 수준으로 초과하여 섭취하셨습니다.\n"
        intakeSolution += "- ⬇️식사량 줄이기\n"
        totalSolution += "평소에도 기록하신 것과 동일하게 식사하신다면 전체적인 식사량을 줄이시기 바랍니다.\n"

    resultProtein = calculateProtein(user_id, protein)
    valProtein = resultProtein[1]

    if resultProtein[0] == "부족":
        nutriSolution += "- 단백질 | " + str(round(protein)) + "g | 부족⬇️ : 단백질은 권장섭취량(" + str(valProtein) + "g) 미만으로 부족하게 섭취하셨습니다.\n"
        intakeSolution += "- ⬆️단백질 섭취량 늘리기\n"
        totalSolution += "단백질이 풍부한 음식을 섭취하시기 바랍니다.\n"
        foodSolution += "\n* 단백질 급원식품: 돼지고기, 달걀, 닭고기, 소고기, 두부, 우유, 대두 등"
    elif resultProtein[0] == "비교적 적절":
        nutriSolution += "- 단백질 | " + str(round(protein)) + "g | 비교적 적절✅ : 단백질은 권장섭취량(" + str(valProtein) + "g)을 고려할 때 비교적 적절하게 섭취하셨습니다.\n"
    elif resultProtein[0] == "적절":
        nutriSolution += "- 단백질 | " + str(round(protein)) + "g | 적절✅ : 단백질은 권장섭취량(" + str(valProtein) + "g)을 충족하여 적절하게 섭취하셨습니다.\n"

    resultSFA = calculateSFA(SFA, energy)
    valSFA = resultSFA[1]
    SFARatio = round(resultSFA[2],1)

    if resultSFA[0] == "적절":
        nutriSolution += "- 포화지방 | " + str(SFARatio) + "% | 적절✅ : 포화지방은 에너지적정비율(" + str(valSFA) + "%) 미만으로 적절하게 섭취하셨습니다.\n"
    elif resultSFA[0] == "비교적 적절":
        nutriSolution += "- 포화지방 | " + str(SFARatio) + "% | 비교적 적절✅) : 포화지방은 에너지적정비율(" + str(valSFA) + "%)을 고려할 때 비교적 적절하게 섭취하셨습니다.\n"
    elif resultSFA[0] == "초과":
        nutriSolution += "- 포화지방 | " + str(SFARatio) + "% | 과다⬆️ : 포화지방은 에너지적정비율(" + str(valSFA) + "%)을 초과하여 섭취하셨습니다.\n"
        intakeSolution += "- ⬇️포화지방 섭취량 줄이기\n"
        totalSolution += first[1] + ", " + second[1] + " 등 포화지방이 많은 음식을 적게 드시기 바랍니다.\n"

    resultSodium = calculateSodium(user_id, sodium)
    valSodium = resultSodium[1]

    if resultSodium[0] == "적절":
        nutriSolution += "- 나트륨 | " + str(round(sodium)) + "mg | 적절✅ : 나트륨은 만성질환위험감소섭취량(" + str(valSodium) + "mg) 미만으로 적절하게 섭취하셨습니다. \n"
    elif resultSodium[0] == "비교적 적절":
        nutriSolution += "- 나트륨 | " + str(round(sodium)) + "mg | 비교적 적절✅ : 나트륨은 만성질환위험감소섭취량(" + str(valSodium) + "mg)을 고려할 때 비교적 적절하게 섭취하셨습니다.\n"
    elif resultSodium[0] == "초과":
        nutriSolution += "- 나트륨 | " + str(round(sodium)) + "mg | 과다⬆️ : 나트륨은 만성질환위험감소섭취량(" + str(valSodium) + "mg)을 초과하여 섭취하셨습니다.\n"
        if resultEnergy[0] != "부족":
            intakeSolution += "- ⬇️나트륨 섭취량 줄이기\n"
            totalSolution += "나트륨 섭취량을 줄이기 위하여 저나트륨 음식섭취를 추천드립니다. \n"

    resultCalcium = calculateCalcium(user_id, calcium)
    valCalcium = resultCalcium[1]
    upperCalcium = resultCalcium[2]
    calciumPercent = resultCalcium[3]

    if resultCalcium[0] == "부족":
        nutriSolution += "- 칼슘 | " + str(round(calcium)) + "mg | 부족⬇️ : 칼슘은 권장섭취량(" + str(valCalcium) + "mg)의 " + str(calciumPercent) + "% 수준으로 부족하게 섭취하셨습니다. \n"
        intakeSolution += "- ⬆️칼슘 섭취량 늘리기\n"
        totalSolution += "칼슘이 충분한 음식을 섭취하시기 바랍니다.\n"
        foodSolution += "\n* 칼슘 급원식품: 저지방 유제품, 멸치, 두부, 두유, 시래기 등"
    elif resultCalcium[0] == "비교적 적절":
        nutriSolution += "- 칼슘 | " + str(round(calcium)) + "mg | 비교적 적절✅ : 칼슘은 권장섭취량(" + str(valCalcium) + "mg)의 " + str(calciumPercent) + "% 수준으로 비교적 적절하게 섭취하셨습니다.\n"
    elif resultCalcium[0] == "권장 충족":
        nutriSolution += "- 칼슘 | " + str(round(calcium)) + "mg | 적절✅ : 칼슘은 권장섭취량(" + str(valCalcium) + "mg)의 " + str(calciumPercent) + "% 수준으로 충족하셨고 상한섭취량(" + str(upperCalcium) +"mg) 미만으로 적절하게 섭취하셨습니다.\n"
    elif resultCalcium[0] == "초과":
        nutriSolution += "- 칼슘 | " + str(round(calcium)) + "mg | 과다⬆️ : 칼슘은 상한섭취량(" + str(upperCalcium) + "mg)의 " + str(calciumPercent) + "% 수준으로 초과하여 섭취하셨습니다.\n"
        intakeSolution += "- ⬇️칼슘 섭취량 줄이기\n"

    resultVitaminC = calculateVitaminC(vitaminC)
    valVitaminC = resultVitaminC[1]
    upperVitaminC = resultVitaminC[2]
    vcPercent = resultVitaminC[3]

    if resultVitaminC[0] == "부족":
        nutriSolution += "- 비타민C | " + str(round(vitaminC)) + "mg | 부족⬇️ : 비타민C는 권장섭취량(" + str(valVitaminC) + "mg)의 " + str(vcPercent) + "% 수준으로 부족하게 섭취하셨습니다. \n"
        intakeSolution += "- ⬆️비타민C 섭취량 늘리기\n"
        totalSolution += "비타민C가 충분한 음식을 섭취하시기 바랍니다.\n"
        foodSolution += "\n* 비타민C 급원식품: 귤, 딸기, 시금치, 무, 오렌지 등"   
    elif resultVitaminC[0] == "비교적 적절":
        nutriSolution += "- 비타민C | " + str(round(vitaminC)) + "mg | 비교적 적절✅ : 비타민C는 권장섭취량(" + str(valVitaminC) + "mg)의 " + str(vcPercent) + "% 수준으로 비교적 적절하게 섭취하셨습니다.\n"
    elif resultVitaminC[0] == "권장 충족":
        nutriSolution += "- 비타민C | " + str(round(vitaminC)) + "mg | 적절✅ : 비타민C는 권장섭취량(" + str(valVitaminC) + "mg)의 " + str(vcPercent) + "% 수준으로 충족하셨고 상한섭취량(" + str(upperVitaminC) +"mg) 미만으로 적절하게 섭취하셨습니다.\n"
    elif resultVitaminC[0] == "초과":
        nutriSolution += "- 비타민C | " + str(round(vitaminC)) + "mg | 과다⬆️ : 비타민C는 상한섭취량(" + str(upperVitaminC) + "mg)의 " + str(vcPercent) + "% 수준으로 초과하여 섭취하셨습니다.\n"
        intakeSolution += "- ⬇️비타민C 섭취량 줄이기\n"

    print(nutriSolution)

    fourthSolution = "▶ 식사 섭취 조언입니다."

    if intakeSolution == "": # 모든 영양소가 적절일 때, 출력 안함
        fourthSolution = ""

    print(fourthSolution)
    print(intakeSolution)

    fifthSolution = "기입하신 내용을 기반으로 드리는 조언입니다."

    if totalSolution == "": # 모든 영양소가 적절일 때, 출력 안함
        fifthSolution = ""

    print(fifthSolution)
    print(totalSolution)

    print(foodSolution)


    resultArr = [firstSolution, secondSolution, ratioSolution, thirdSolution, nutriSolution, fourthSolution, intakeSolution, fifthSolution, totalSolution, foodSolution]
    result = "\n".join(resultArr)

    print(result)

    return result

def calculateRatio(carbo, protein, fat): # 탄단지 비율별 솔루션 계산

    # 탄단지 비율 구하기
    carboRatio = round((carbo * 4 / (carbo*4 + protein * 4 + fat * 9))*100)
    proteinRatio = round((protein *4 / (carbo*4 + protein * 4 + fat * 9))*100)
    fatRatio = round((fat*9 / (carbo*4 + protein * 4 + fat * 9))*100)

    print(carboRatio, proteinRatio, fatRatio)

    carboSolution = ""
    proteinSolution = ""
    fatSolution = ""

    if carboRatio < 55:
        carboSolution = "-탄수화물(부족⬇️):" + str(carboRatio) + "%\n"
    elif carboRatio >= 55 and carboRatio < 65:
        carboSolution = "-탄수화물(적절✅):" + str(carboRatio) + "%\n"
    else:
        carboSolution = "-탄수화물(과다⬆️):" + str(carboRatio) + "%\n"


    if proteinRatio < 7:
        proteinSolution = "-단백질(부족⬇️):" + str(proteinRatio) + "%\n"
    elif proteinRatio >= 7 and proteinRatio < 20:
        proteinSolution = "-단백질(적절✅):" + str(proteinRatio) + "%\n"
    else:
        proteinSolution = "-단백질(과다⬆️):" + str(proteinRatio) + "%\n"


    if fatRatio < 15:
        fatSolution = "-지방(부족⬇️):" + str(fatRatio) + "%\n"
    elif fatRatio >= 15 and fatRatio < 30:
        fatSolution = "-지방(적절✅):" + str(fatRatio) + "%\n"
    else:
        fatSolution = "-지방(과다⬆️):" + str(fatRatio) + "%\n"

    ratioSolution = carboSolution + proteinSolution + fatSolution

    return ratioSolution

def calculateEnergy(user_id, energy): # 영양소별 솔루션 계산 - 열량

    PA = 0

    if user_dict[user_id].gender == "남자":
        if user_dict[user_id].PAL >= 13.3 : PA = 1.48
        elif user_dict[user_id].PAL >= 11.2 : PA = 1.25
        elif user_dict[user_id].PAL >= 9.8 : PA = 1.11
        elif user_dict[user_id].PAL >= 7 : PA = 1

        EER = round( (662 - (9.53*user_dict[user_id].age) + (PA* ((15.91*user_dict[user_id].weight) + (539.6*user_dict[user_id].height/100)))))

    elif user_dict[user_id].gender == "여자":
        if user_dict[user_id].PAL >= 13.3 : PA = 1.45
        elif user_dict[user_id].PAL >= 11.2 : PA = 1.27
        elif user_dict[user_id].PAL >= 9.8 : PA = 1.12
        elif user_dict[user_id].PAL >= 7 : PA = 1

        EER = round( (354 - (6.91*user_dict[user_id].age) + (PA* ((9.36*user_dict[user_id].weight) + (726*user_dict[user_id].height/100)))))

    energyPercent = energy/EER *100

    if energyPercent < 90:
        return ["부족", EER, round(energyPercent)]
    elif 90 <= energyPercent and 110 >= energyPercent:
        return ["적절", EER, round(energyPercent)]
    else:
        return ["초과", EER, round(energyPercent)]


def calculateProtein(user_id, protein): # 영양소별 솔루션 계산 - 단백질
    
    if user_dict[user_id].gender == "남자":
        if user_dict[user_id].age >= 19 and user_dict[user_id].age <= 49:
            if protein < 58.5:
                return ["부족", 65]
            elif 58.5 <= protein and protein < 65:
                return ["비교적 적절",65]
            else:
                return ["적절",65]
        else:
            if protein < 54:
                return ["부족",60]
            elif 54 <= protein and protein < 60:
                return ["비교적 적절",60]
            else:
                return ["적절",60]

    elif user_dict[user_id].gender == "여자":
        if user_dict[user_id].age >= 19 and user_dict[user_id].age <= 29:
            if protein < 49.5:
                return ["부족",55]
            elif 49.5 <= protein and protein < 55:
                return ["비교적 적절",55]
            else:
                return ["적절",55]
        else:
            if protein < 45:
                return ["부족",50]
            elif 45 <= protein and protein < 50:
                return ["비교적 적절",50]
            else:
                return ["적절",50]
    
def calculateSFA(SFA, energy): # 영양소별 솔루션 계산 - 포화지방

    SFARatio = round((SFA * 9 / energy)*100, 2)

    print(SFARatio)

    if SFARatio < 7:
        return ["적절",7,SFARatio]
    elif SFARatio >= 7 and SFARatio <= 7.7:
        return ["비교적 적절",7,SFARatio]
    else:
        return ["초과",7,SFARatio]

def calculateSodium(user_id, sodium): # 영양소별 솔루션 계산 - 나트륨
    if user_dict[user_id].age >= 19 and user_dict[user_id].age <= 64:
        if sodium < 2300:
            return ["적절",2300]
        elif sodium >= 2300 and sodium <= 2530:
            return ["비교적 적절",2300]
        else:
            return ["초과",2300]

    elif user_dict[user_id].age >= 65 and user_dict[user_id].age <= 74:
        if sodium < 2100:
            return ["적절",2100]
        elif sodium >= 2100 and sodium <= 2310:
            return ["비교적 적절",2100]
        else:
            return ["초과",2100]
    
    elif user_dict[user_id].age >= 75:
        if sodium < 1700:
            return ["적절",1700]
        elif sodium >= 1700 and sodium <= 1870:
            return ["비교적 적절",1700]
        else:
            return ["초과",1700]

def calculateCalcium(user_id, calcium): # 영양소별 솔루션 계산 - 칼슘

    if user_dict[user_id].gender == "남자":
        if user_dict[user_id].age >= 19 and user_dict[user_id].age <= 49:

            calciumPercent = round((calcium/800*100))
            calciumUpperPercent = round((calcium/2500*100))

            if calcium < 720:
                return ["부족",800,2500,calciumPercent]
            elif 720 <= calcium and calcium < 800:
                return ["비교적 적절",800,2500,calciumPercent]
            elif 800 <= calcium and calcium < 2500:
                return ["권장 충족",800,2500,calciumPercent]
            else:
                return ["초과",800,2500,calciumUpperPercent]

        elif user_dict[user_id].age >= 50 and user_dict[user_id].age <= 64:

            calciumPercent = round((calcium/750*100))
            calciumUpperPercent = round((calcium/2000*100))

            if calcium < 675:
                return ["부족",750,2000,calciumPercent]
            elif 675 <= calcium and calcium < 750:
                return ["비교적 적절",750,2000,calciumPercent]
            elif 750 <= calcium and calcium < 2000:
                return ["권장 충족",750,2000,calciumPercent]
            else:
                return ["초과",750,2000,calciumUpperPercent]

        else:

            calciumPercent = round((calcium/700*100))
            calciumUpperPercent = round((calcium/2000*100))

            if calcium < 630:
                return ["부족",700,2000,calciumPercent]
            elif 630 <= calcium and calcium < 700:
                return ["비교적 적절",700,2000,calciumPercent]
            elif 700 <= calcium and calcium < 2000:
                return ["권장 충족",700,2000,calciumPercent]
            else:
                return ["초과",700,2000,calciumUpperPercent]

    elif user_dict[user_id].gender == "여자":
        if user_dict[user_id].age >= 19 and user_dict[user_id].age <= 49:

            calciumPercent = round((calcium/700*100))
            calciumUpperPercent = round((calcium/2500*100))

            if calcium < 630:
                return ["부족",700,2500,calciumPercent]
            elif 630 <= calcium and calcium < 700:
                return ["비교적 적절",700,2500,calciumPercent]
            elif 700 <= calcium and calcium < 2500:
                return ["권장 충족",700,2500,calciumPercent]
            else:
                return ["초과",700,2500,calciumUpperPercent]
        else:

            calciumPercent = round((calcium/800*100))
            calciumUpperPercent = round((calcium/2000*100))

            if calcium < 720:
                return ["부족",800,2000,calciumPercent]
            elif 720 <= calcium and calcium < 800:
                return ["비교적 적절",800,2000,calciumPercent]
            elif 800 <= calcium and calcium < 2000:
                return ["권장 충족",800,2000,calciumPercent]
            else:
                return ["초과",800,2000,calciumUpperPercent]

def calculateVitaminC(vc): # 영양소별 솔루션 계산 - 비타민C

    vcPercent = round((vc/100*100))
    vcUpperPercent = round((vc/2000*200))

    if vc < 90:
        return ["부족",100,2000,vcPercent]
    elif 90 <= vc and vc < 100:
        return ["비교적 적절",100,2000,vcPercent]
    elif 100 <= vc and vc < 2000:
        return ["권장 충족",100,2000,vcPercent]
    else:
        return ["초과",100,2000,vcUpperPercent]


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
    print("일간 식단 유저별 엑셀 저장 함수")
    
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