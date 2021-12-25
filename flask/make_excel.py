from datetime import datetime
from itertools import count
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://user:0000@cluster0.uio0y.mongodb.net/myFirstDatabase?retryWrites=true&w=majority") # DB연결
db = cluster["DietTherapy"]
음식영양성분 = db["음식영양성분"]
음식섭취양 = db["음식섭취양"]
식이빈도조사_음식섭취양 = db["식이빈도조사_음식섭취양"]

df = None
now = str(datetime.now())

excel_column = ["날짜",
        "UserID",
        "이름",
        "나이",
        "성별",
        "키",
        "몸무게",
        "운동",
        "운동 시간",
        "운동 횟수",
        "영양제",
        "영양제섭취"]

all = 식이빈도조사_음식섭취양.find()

for food in all:
    excel_column.append(food["음식종류"] + "_freqperday")
    excel_column.append(food["음식종류"] + "_portion")

print(excel_column)    

try:
    df = pd.read_excel("./data/1년섭취빈도조사.xlsx", engine='openpyxl')
except:
    df = pd.DataFrame(columns=excel_column)
    df.to_excel("./data/1년섭취빈도조사.xlsx",index=False)
