class Mathcome():
    person = ""

    def __init__(self, person="양태빈"):
        self.person = person

    def KYU(self):
        map = {"강혜빈":"", "김리온":"", "김연웅":"", "신병철":"", "안태현":"", "양태빈": "", "이진영":""}
        if self.person in list(map.keys()):
            return("\"" + str(self.person) + "\" 이라고...?\n\"" + str(map[self.person]) + "\"인 것 같아")
        else:
            return("그런 사람 몰라")

    def KHB(self):
        map = {"강혜빈":"저요? 음 저는 제가 굉장히 모순적인 사람이라고 생각합니다. 예민하면서도 무디고 뜨거우면서도 차갑고 냉정하면서도 정이 많고 시크하면서도 여립니다.",
               "김리온":"우리 리온이는 나의 자부심.성향이 거의 반대인 것 같지만 지오디 노래 중에 반대가 끌리는 이유라는 노래가 있습니다. 반대라서 옆에 오래 두고 싶은 친구",
               "김연웅":"울 여눙... 여눙이는 나의 욕심. 여눙이 보면서 느낀 게 많아서 욕심도 조금씩 생김.",
               "신병철":"쌤 ㅜㅜ 쌤은 내 중심!! 내가 뭘 하던지 휘어지거나 부러지지 않게 내가 내 중심을 지킬 수 있게 해준 사람이 쌤♥ 그리고 내 롤모델",
               "안태현":"우리 탱탱쓰 탱탱쓰는 내 자존심. 우리 중에서 리온이 빼고 제일 덜 미친 자라서 내 자존심",
               "양태빈":"하.... 넌 내 근심. 밥은 잘 먹는지 또 숙제 미리 안 해서 밤 새는지 또 사고 치는지 걱정이 된다. 근심아.",
               "이진영":"우리 진진이 내 밥심!!!!! 우리 진진이 데리고 여기저기 맛난 식당 가서 밥 먹이고 싶아!!! 우리 자기 항상 안 아팠으면 좋겠고 우리 자기 너무 착한 자기ㅜㅜ 예쁜 것만 보고 살았으면 좋겠는 우리 자기♥"}
        if self.person in list(map.keys()):
            return ("\"" + str(self.person) + "\" 이라고...?\n\"" + str(map[self.person])+"\"")
        else:
            return ("그런 사람 몰라")

    def LJY(self):
        map = {"강혜빈":"날 너무 좋아해", "김리온":"리오니 너무 바빠...", "김연웅":"여눙이 눈치 없어", "신병철":"사랑해여", "안태현":"안국이는 방치가 심해", "양태빈": "ㅋ", "이진영":"ㅎ"}
        if self.person in list(map.keys()):
            return ("\"" + str(self.person) + "\" 이라고...?\n\"" + str(map[self.person])+"\"")
        else:
            return ("그런 사람 몰라")

    def KLO(self):
        map = {"강혜빈":"", "김리온":"", "김연웅":"", "신병철":"", "안태현":"", "양태빈": "", "이진영":""}
        if self.person in list(map.keys()):
            return ("\"" + str(self.person) + "\" 이라고...?\n\"" + str(map[self.person])+"\"")
        else:
            return ("그런 사람 몰라")

    def ATG(self):
        map = {"강혜빈":"", "김리온":"", "김연웅":"", "신병철":"", "안태현":"", "양태빈": "", "이진영":""}
        if self.person in list(map.keys()):
            return ("\"" + str(self.person) + "\" 이라고...?\n\"" + str(map[self.person])+"\"")
        else:
            return ("그런 사람 몰라")

    def SBC(self):
        map = {"강혜빈":"", "김리온":"", "김연웅":"", "신병철":"", "안태현":"", "양태빈": "", "이진영":""}
        if self.person in list(map.keys()):
            return ("\"" + str(self.person) + "\" 이라고...?\n\"" + str(map[self.person])+"\"")
        else:
            return ("그런 사람 몰라")

    def YTB(self):
        map = {"강혜빈":"덕질 좋아하는 착한 친구", "김리온":"착하고 친절한 친구", "김연웅":"공부 열심히 하는 착한 친구", "신병철":"열정적이시고 착한 선생님", "안태현":"머슴...?", "양태빈": "난데요", "이진영":"노래 잘 부르는 나쁜 시키"}
        if self.person in list(map.keys()):
            return ("\"" + str(self.person) + "\" 이라고...?\n\"" + str(map[self.person])+"\"")
        else:
            return ("그런 사람 몰라")
