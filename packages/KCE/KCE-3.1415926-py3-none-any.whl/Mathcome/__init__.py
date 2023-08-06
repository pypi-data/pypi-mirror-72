class KCE():

    teachers = {"김호숙" : ["1", "5", "9"], "김용주" : ["3", "4", "7", "8"], "윤상현" : ["2", "6", "10"]}
    function_description = {
        "move()":"앞으로 움직임(한 칸)",
        "turn_left()":"객체를 왼쪽으로 돌립니다.",
        "turn_right()":"객체를 오른쪽으로 돌립니다.",
        "turn_back()":"객체를 뒤로 돌립니다."
    }

    def __init__(self, classes="1"):
        self.classes = classes

    def teacher(self):
        for i in list(self.teachers.keys()):
            for j in self.teachers[i]:
                if j == self.classes:
                    return i
        return "%d 분반 존재하지 않습니다." % int(self.classes)

    def command(self):
        print("사용 가능한 함수의 이름입니다.")
        for i in list((self.function_description).keys()):
            print(i)


    def help(self, order):
        if len(list(self.function_description.keys())) >= int(order)+1 > 0:
            print(self.function_description[list(self.function_description.keys())[int(order)-1]])
        else:
            print("범위를 넘어섰습니다.")