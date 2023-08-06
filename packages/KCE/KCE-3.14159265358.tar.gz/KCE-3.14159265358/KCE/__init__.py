class KCE():

    teachers = {"김호숙" : [1, 5, 9], "김용주" : [3, 4, 7, 8], "윤상현" : [2, 6, 10]}
    function_description = {
        "_update_pos" : "생성자(__init__)에 있는 avenue와 street로 위치를 업데이트 합니다.",
        "set_trace(color=None)":"trace의 색을 변경 및 설정 할 수 있습니다.",
        "set_pause" : "각 움직임당 딜레이의 정도를 결정함",
        "get_pos":"개체의 위치를 알려줍니다.((x, y)의 형태로 알려줍니다.)",
        "turn_left()":"객체를 왼쪽으로 돌립니다.",
        "turn_right()":"객체를 오른쪽으로 돌립니다.",
        "turn_back()":"객체를 뒤로 돌립니다.",
        "move()":"앞으로 움직임(한 칸)",
        "front_is_clear()":"앞쪽에 벽이 있는지를 확인합니다.",
        "left_is_clear()":"왼쪽에 벽이 있는지를 확인합니다.",
        "right_is_clear()":"오른쪽에 벽이 있는지를 확인합니다.",
        "facing_north()":"객체가 앞쪽을 보고 있는지를 확인합니다.",
        "carries_beepers()":"현재 비퍼를 가지고 있는지를 확인합니다.",
        "on_beeper()":"객체가 비퍼 위에 있는지를 확인합니다.",
        "pick_beeper()":"바닥에 있는 비퍼를 줍습니다.",
        "drop_beeper()":"비퍼백(beeper bag)에서 바닥에 비퍼를 내려놓습니다."
    }
    function_help = {}

    for i in list(function_description.keys()):
        function_help[function_description[i]] = i

    All_Command=[
        "Q",
        "teacher",
        "command",
        "command_help*",
        "Function",
        "Function_help*",
        "factorial*",
        "find_max",
        "find_min",
        "isPrime"
    ]

    def __init__(self, classes=1):
        self.classes = classes
        print("설정 완료\nQ() 함수를 사용해 보세요\n참고 :: 설명에 있는 모든 함수는 Robot class에 포함된 함수만을 설명해 놓은 것 입니다.")

    def teacher(self):
        for i in list(self.teachers.keys()):
            for j in self.teachers[i]:
                if j == self.classes:
                    print(str(self.classes) + " 분반의 CS1 과목 담당 선생님의 성함입니다.")
                    print(str(self.classes) + " 분반 : " + i) ; return
        return "%d 분반 존재하지 않습니다." % int(self.classes)

    def command(self):
        print("package cs1robots에서 사용 가능한 함수의 이름입니다.\n함수 번호 : 함수 이름\n")
        for i in range(len(list((self.function_description).keys()))):
            print(str(i+1)+" : "+list((self.function_description).keys())[i])
        print("\n 각 함수의 기능을 보려면 command_help(함수 번호)를 사용하세요")

    def Q(self):
        print("Class KCE에 있는 모든 함수 입니다.\n*이 붙은 것은 입력값이 필요\n")
        for i in range(len(self.All_Command)):
            print(str(i+1) + " : " + self.All_Command[i])

    def Function(self):
        print("cs1robots에서 사용할 수 있는 기능의 목록입니다.\n기능 번호 : 기능 설명\n")
        for i in range(len(list(self.function_description.keys()))):
            print(str(i+1) + " : " + list(self.function_help.keys())[i])
        print("\n 각 기능을 사용하는 함수를 보려면 Function_help(기능 번호)를 사용하세요")

    def Function_help(self, order=1):
        if len(list(self.function_help.keys())) >= int(order) > 0:
            print(list(self.function_help.keys())[int(order)-1] + " : " + self.function_help[list(self.function_help.keys())[int(order)-1]])
        else:
            print("범위를 넘어섰습니다.")

    def command_help(self, order=1):
        if len(list(self.function_description.keys())) >= int(order) > 0:
            print(list(self.function_description.keys())[int(order)-1]+" : "+self.function_description[list(self.function_description.keys())[int(order)-1]])
        else:
            print("범위를 넘어섰습니다.")

    def factorial(self, n=2):
        prod = 1
        for i in range(1, n+1):
            prod *= i
        return prod

    def find_max(self, list):
        max = -99999999999999999999999
        for i in list:
            if max < i:
                max = i
        return max

    def find_min(self, list):
        min = 99999999999999999999999
        for i in list:
            if min > i:
                min = i
        return min

    def isPrime(self, p):
        for i in range(int(p**(1/2))):
            if p % i == 0: return False
        return True

    def countPrime(self, numbers):
        count = 0
        for i in numbers:
            if self.isPrime(i): count += 1
        return count