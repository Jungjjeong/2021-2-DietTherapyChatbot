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
age = 0
gender = ""
height = 0
weight = 0
exercise = ""
exerciseTime = ""
exerciseNum = ""

@app.route("/")
def hello():
    return "Chatbot server"



#------------------------------------------------------------------------1년 솔루션(서울대)------------------------------------------------------------------------#

@app.route("/getAge", methods = ["GET", "POST"]) 
def getAge():
    print("나이 정보 받는 함수")
    global age
    req = request.get_json()

    print(req)

    ageReq =  req["action"]["detailParams"]["sys_number_age"]["origin"] #나이 **세
    print(ageReq)


    res = {
        "version" : "2.0",
        "template":{
            "outputs": [
                {
                    "simpleText": {
                        "text" : "입력하신 나이는 " + ageReq + "입니다.😊\n\n사용자님의 성별을 입력해 주세요. \nex)남자"
                    }
                }
            ]
        }
    }


    age = int(ageReq.replace("세",""))
    return jsonify(res)



@app.route("/getGender", methods = ["GET", "POST"]) 
def Gender():
    print("성별 정보 받는 함수")
    global gender
    req = request.get_json()

    print(req)

    gender =  req["action"]["detailParams"]["성별"]["value"] #성별
    print(gender)


    res = {
        "version" : "2.0",
        "template":{
            "outputs": [
                {
                    "simpleText": {
                        "text" : "입력하신 성별은 " + gender + "입니다.😊\n\n사용자님의 키를 입력해 주세요. \nex)165cm"
                    }
                }
            ]
        }
    }


    print(age, gender)
    return jsonify(res)



@app.route("/getHeight", methods = ["GET", "POST"]) 
def Height():
    print("키 정보 받는 함수")
    global height
    req = request.get_json()

    print(req)

    heightReq =  req["action"]["detailParams"]["sys_unit_length"]["origin"] #키 **cm
    print(heightReq)


    res = {
        "version" : "2.0",
        "template":{
            "outputs": [
                {
                    "simpleText": {
                        "text" : "입력하신 키는 " + heightReq + "입니다.😊\n\n사용자님의 몸무게를 입력해 주세요. \nex)55kg"
                    }
                }
            ]
        }
    }

    height = int(heightReq.replace("cm",""))
    print(age, gender, height)
    return jsonify(res)



@app.route("/getWeight", methods = ["GET", "POST"]) 
def Weight():
    print("몸무게 정보 받는 함수")
    global weight
    req = request.get_json()

    print(req)

    weightReq =  req["action"]["detailParams"]["sys_unit_weight"]["origin"] #몸무게 **kg
    print(weightReq)


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
                                "title": "나이",
                                "description": str(age) + "세"
                            },
                            {
                                "title": "성별",
                                "description": gender
                            },
                            {
                                "title": "키",
                                "description": str(height) + "cm"
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

    weight = int(weightReq.replace("kg",""))
    print(age, gender, height, weight)
    print(res)

    return jsonify(res)


@app.route("/getExercise", methods = ["GET", "POST"]) 
def Exercise():
    print("1회 운동시간 정보 받는 함수")
    global exercise
    req = request.get_json()

    print(req)

    exerciseReq =  req["action"]["detailParams"]["sys_number_ordinal"]["origin"] #운동 번호
    print(exerciseReq)

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

    print(age, gender, height, weight, exercise)
    return jsonify(res)



@app.route("/getExerciseTime", methods = ["GET", "POST"]) 
def ExerciseTime():
    print("1회 운동 시간 정보 받는 함수")
    global exerciseTime
    req = request.get_json()

    print(req)

    exerciseTime =  req["action"]["detailParams"]["sys_unit_duration"]["origin"] #1회 운동 시간
    print(exerciseTime)


    res = {
        "version" : "2.0",
        "template":{
            "outputs": [
                {
                    "simpleText": {
                        "text" : "입력하신 1회 운동 시간은 " + exerciseTime + "입니다.\n\n해당 운동의 주당 운동 횟수를 입력해주세요.\nex)3회"
                    }
                }
            ]
        }
    }

    print(age, gender, height, weight, exercise ,exerciseTime)
    return jsonify(res)


@app.route("/getExerciseNum", methods = ["GET", "POST"]) 
def ExerciseNum():
    print("주당 운동 횟수 정보 받는 함수")
    global exerciseNum
    req = request.get_json()

    print(req)

    exerciseNum =  req["action"]["detailParams"]["횟수"]["value"] #주당 운동 횟수
    print(exerciseNum)


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
                                "description": exercise
                            },
                            {
                                "title": "1회운동시간",
                                "description": exerciseTime
                            },
                            {
                                "title": "주당운동횟수",
                                "description": exerciseNum
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

    print(age, gender, height, weight, exercise ,exerciseTime, exerciseNum)
    return jsonify(res)


#------------------------------------------------------------------------1일 솔루션(의대)------------------------------------------------------------------------#


# 사진 전송 요구 + 사진 클라우드 링크 받아오는 함수 
@app.route("/getPhoto", methods = ["GET", "POST"]) 
def start():
    print("사진 정보 받는 함수")
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
            ]
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


@app.route("/solution",methods = ["GET","POST"])
def solution():
    global food_name
    global age
    df = None
    
    print("솔루션 제공 함수")

    req = request.get_json()
    print(req)

    user_id = req["userRequest"]["user"]["id"]
    print(user_id)

    food_type = req["action"]["detailParams"]["솔루션"]["value"]
    print(food_type)

    #나이에 맞는 기준량
    if age >= 19 and age < 30:
        print("19~29") 
        calorie = 2600 #칼로리(kcal)
        sodium = 1500 #나트륨(mg)
        carbohydrate = 130 #탄수화물(g)
        protein = 65 #단백질(g)
        fat = round(float(food_detail[8]) / task2 * task3, 2) #지방(g)
        kal = 800 #칼슘
        vC = 100 #비타민 C
        saturatedFat = round(float(food_detail[16]) / task2 * task3, 2) #포화지방산
    elif age >= 30 and age < 50:
        print("30~49")
        calorie = 2500 #칼로리(kcal)
        sodium = 1500 #나트륨(mg)
        carbohydrate = 130 #탄수화물(g)
        protein = 65 #단백질(g)
        fat = round(float(food_detail[8]) / task2 * task3, 2) #지방(g)
        kal = 800 #칼슘
        vC = 100 #비타민 C
        saturatedFat = round(float(food_detail[16]) / task2 * task3, 2) #포화지방산
    elif age >= 50 and age < 65:
        print("50~64")
        calorie = 2200 #칼로리(kcal)
        sodium = 1500 #나트륨(mg)
        carbohydrate = 130 #탄수화물(g)
        protein = 60 #단백질(g)
        fat = round(float(food_detail[8]) / task2 * task3, 2) #지방(g)
        kal = 750 #칼슘
        vC = 100 #비타민 C
        saturatedFat = round(float(food_detail[16]) / task2 * task3, 2) #포화지방산
    elif age >= 65 and age < 75:
        print("65~74")
        calorie = 2000 #칼로리(kcal)
        sodium = 1300 #나트륨(mg)
        carbohydrate = 130  #탄수화물(g)
        protein = 60 #단백질(g)
        fat = round(float(food_detail[8]) / task2 * task3, 2) #지방(g)
        kal = 700 #칼슘
        vC = 100 #비타민 C
        saturatedFat = round(float(food_detail[16]) / task2 * task3, 2) #포화지방산
    elif age >= 75:
        print("75 이상")
        calorie = 1900 #칼로리(kcal)
        sodium = 1100 #나트륨(mg)
        carbohydrate = 130 #탄수화물(g)
        protein = 60 #단백질(g)
        fat = round(float(food_detail[8]) / task2 * task3, 2) #지방(g)
        kal = 700 #칼슘
        vC = 100 #비타민 C
        saturatedFat = round(float(food_detail[16]) / task2 * task3, 2) #포화지방산
    else:
        print("나이 미입력")

    calculate = [calorie, sodium, carbohydrate, protein, fat, kal, vC, saturatedFat]


    answer = "3끼를 기준으로 솔루션을 제공합니다."

    try:
        df = pd.read_excel("./data/" + user_id + ".xlsx", engine='openpyxl')
    except Exception as e:
        answer = "입력된 식단 정보가 없습니다./n식단 입력 후 다시 시도해주세요."



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
        }
    }

    food_name = food_type
    return jsonify(res)






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






#------------------------------------------------------------------------ Port------------------------------------------------------------------------#


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, threaded = True)