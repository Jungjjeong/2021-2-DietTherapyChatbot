from survey import SurveyForm

class SurveyUser():

    def __init__(self, id, user_name):
        self.id = id
        self.user_name = user_name
        self.age = 0
        self.gender = ""
        self.height = 0
        self.weight = 0
        self.exercise = ""
        self.exerciseTime = ""
        self.exerciseNum = ""
        self.nutriSupplement = ""
        self.nutriIntake = ""
        self.survey = SurveyForm()

        self.solution_칼로리 = 0
        self.solution_탄수화물 = 0
        self.solution_단백질 = 0
        self.solution_지방 = 0
        self.solution_나트륨 = 0
        self.solution_비타민C = 0
        self.solution_포화지방산 = 0
        self.solution_칼슘 = 0

        self.solutionResultText = ""

    def __str__(self) -> str:
        value = """
        사용자 : {id}
        이름 : {name}
        나이 : {age}
        """.format(id = self.id, name = self.user_name, age=self.age)
        return value

    def __repr__(self) -> str:
        value = """
        사용자 : {id}
        이름 : {name}
        나이 : {age}
        """.format(id = self.id, name = self.user_name, age=self.age)
        return value

    def to_excel_format():
        """
        객체에 저장된 정보를 
        리스트 형태로 반환해주기
        """
        pass

    def get_user_info(self) -> list:
        return [
            self.id,
            self.user_name,
            self.age,
            self.gender,
            self.height,
            self.weight,
            self.exercise,
            self.exerciseTime,
            self.exerciseNum,
            self.nutriSupplement,
            self.nutriIntake,
        ]