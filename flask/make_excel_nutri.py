from datetime import datetime
import pandas as pd

df = None
now = str(datetime.now())

nutri_column = ["날짜",
        "UserID",
        "이름",
        "나이",
        "성별",
        "키",
        "몸무게"]


for nutri in range(7):
    nutri_column.append("제품명"+str(nutri+1))
    nutri_column.append("제조회사"+str(nutri+1))
    nutri_column.append("복용기간"+str(nutri+1))
    nutri_column.append("복용빈도"+str(nutri+1))
    nutri_column.append("1회복용분량"+str(nutri+1))

print(nutri_column)    

df = pd.DataFrame(columns=nutri_column)
df.to_excel('/home/user/jiyoung/share_data/1년섭취빈도조사_식이보충제.xlsx', sheet_name='nutri', index=False)
print(df)