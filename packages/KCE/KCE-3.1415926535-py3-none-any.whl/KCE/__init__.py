class KCE():

    teachers = {"김호숙" : [1, 5, 9], "김용주" : [3, 4, 7, 8], "윤상현" : [2, 6, 10]}
    function_description = {
        "move(None)":"앞으로 움직임(한 칸)",
        "turn_left(None)":"객체를 왼쪽으로 돌립니다.",
        "turn_right(None)":"객체를 오른쪽으로 돌립니다.",
        "turn_back(None)":"객체를 뒤로 돌립니다."
    }
    function_help = {}

    for i in range(len(list(function_description.keys()))):
        function_help[function_description[list(function_description.keys())[i]]] = list(function_description.keys())[i]

    All_Command=[
        "Q",
        "teacher",
        "command",
        "command_help",
        "Function",
        "Function_help"
    ]

    def __init__(self, classes=1):
        self.classes = classes
        print("설정 완료\nQ() 함수를 사용해 보세요")

    def teacher(self):
        for i in list(self.teachers.keys()):
            for j in self.teachers[i]:
                if j == self.classes:
                    print(str(self.classes) + " 분반의 CS1 과목 담당 선생님의 성함입니다.")
                    print(str(self.classes) + " 분반 : " + i) ; return
        return "%d 분반 존재하지 않습니다." % int(self.classes)

    def command(self):
        print("package cs1robots에서 사용 가능한 함수의 이름입니다.\n")
        for i in range(len(list((self.function_description).keys()))):
            print(str(i+1)+" : "+list((self.function_description).keys())[i])

    def Q(self):
        print("Class KCE에 있는 모든 함수 입니다.\n")
        for i in range(len(self.All_Command)):
            print(str(i+1) + " : " + self.All_Command[i])

    def Function(self):
        for i in range(len(list(self.function_description.keys()))):
            print(str(i+1) + " : " + list(self.function_help.keys())[i])

    def Function_help(self, order):
        if len(list(self.function_help.keys())) >= int(order) > 0:
            print(list(self.function_help.keys())[int(order)-1] + " : " + self.function_help[list(self.function_help.keys())[int(order)-1]])
        else:
            print("범위를 넘어섰습니다.")

    def command_help(self, order):
        if len(list(self.function_description.keys())) >= int(order) > 0:
            print(list(self.function_description.keys())[int(order)-1]+" : "+self.function_description[list(self.function_description.keys())[int(order)-1]])
        else:
            print("범위를 넘어섰습니다.")