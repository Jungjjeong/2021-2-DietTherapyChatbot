
class SurveyForm():

    def __init__(self):
        self.exercise = []
        self.exerciseTime = []
        self.exerciseNum = []
        self.exerciseIdx = 0

        self.nutriSupplement = []
        self.nutriCompany = []
        self.nutriTerm = []
        self.nutriFrequency = []
        self.nutriIntake = []
        self.nutriIdx = 0

        self.foodFrequency = []
        self.foodEntity = []
        self.idx = 0

    def to_csv_string(self):
        # 입력된 정보를 csv 파일에 추가할 수 있는 형태로 반환
        pass