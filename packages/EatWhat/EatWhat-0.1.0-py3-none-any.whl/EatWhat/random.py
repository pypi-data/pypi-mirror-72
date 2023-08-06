import random
from EatWhat.osprofile import OSProfile


DEFAULT_OPTIONS = {
    "random-options": [
        "冒菜",
        "盅盅面",
        "乡村基",
        "大米先生",
        "啾啾家",
        "猪脚饭",
        "沸腾鸡",
        "远一点的大米先生",
        "远一点的乡村基",
        "大盘鸡",
        "凉皮",
        "秦功道凉皮",
        "煎饼果子",
        "炒菜",
        "肯德基",
        "吃屁吧你",
        "口也shi了雷"
    ]
}


class EatWhatRandom(OSProfile):

    def __init__(self):
        super().__init__(appname="EatWhat", profile="random-options", options=DEFAULT_OPTIONS)

    def random(self):
        options = self.read_profile()['random-options']

        choice = random.choice(options)

        print(f"用餐建议:  {choice}")

        if choice == '猪脚饭':
            print("什么！打死不吃猪脚饭? 行吧，换一个")
            self.random()


if __name__ == "__main__":
    ew = EatWhat()
    ew.random()
