class Player:
    """ Player 클래스 """
    def __init__(self, name, money, position = 0):
        self.name = name
        self.__current_money = money
        self.__position = position

        self.__hand = []
        self.__game_status = "Alive"
        self.__bet_status = None
        self.__betting_history = []
        self.__round_result = None
        self.whole_cards = []
        self.ranking = []

    def init_hand(self):
        self.__hand = []

    def init_bet_status(self):
        self.__bet_status = None

    def add_card(self, aCard):
        self.__hand.append(aCard)
        self.__round_result = []
        self.whole_cards = []
        self.ranking = []

    def show_down(self, community_cards):
        self.whole_cards.append(self.__hand)
        self.whole_cards.append(community_cards)

        self.whole_cards.sort(key = lambda own_card: own_card.rank)

        # 족보 판단하는 함수 - 해당 족보의 갯수와 숫자를 저장 ex) 7, 5 투페어: is_pair = [2, 7, 5]
        is_fourcard = [0]
        is_flush = [0]
        is_straight = [0]
        is_triple = [0]
        is_pair = [0]

        # 플러쉬 판단
        # 문양 갯수 세는 변수
        suit_num = [0, 0, 0, 0]

        for i in range(7):
            suit_num[self.whole_cards[i].suit] += 1
        for i in range(4):
            if suit_num[i] >= 5: is_flush[0] = 1
            if self.whole_cards[6].suit == i: is_flush[1] = self.whole_cards[6].rank
            elif self.whole_cards[5].suit == i: is_flush[1] = self.whole_cards[5].rank
            elif self.whole_cards[4].suit == i: is_flush[1] = self.whole_cards[4].rank

        # 스트레이트 판단
        whole_list = []
        whole_set_list = []
        for i in range(7):
            whole_list.append(self.whole_cards[i].rank)
        whole_set_list = list(set(self.whole_list))
        continuity = 1
        for i in range(1, len(whole_set_list)):
            if whole_set_list[i] == whole_set_list[i - 1] + 1: continuity += 1
            else: continuity = 1

            if continuity >= 5:
                is_straight[0] = 1
                is_straight[1] = whole_set_list[i]

        # 페어, 트리플, 포카드 판단
        counter = {}

        for num in whole_list:
            try: counter[num] += 1
            except: counter[num] = 1

        for num in counter.keys:
            if counter[num] == 2:
                is_pair[0] += 1
                is_pair.insert(1, num)
            if counter[num] == 3:
                is_triple[0] += 1
                is_triple.insert(1, num)
            if counter[num] == 4:
                is_fourcard[0] += 1
                is_fourcard.append(num)

        # return ranking
        # straight flush : 8
        # four card : 7
        # full house : 6
        # flush : 5
        # straight : 4
        # triple : 3
        # two pair : 2
        # one pair : 1
        # top : 0
        if is_flush[0] == 1 and is_straight[0] == 1:
            # 이렇게 하면 안됨
            # 스트레이트인 카드가 플러쉬이어야 해서 다시 비교해야됨 ㅠㅠ
            # A가 가장 큰 값으로 설정해서 로티플도 추가해야됨
            return []
        elif is_fourcard[0] == 1:
            self.ranking = [7, is_fourcard[1]]
        elif is_triple[0] == 1 and is_pair[0] >= 1:
            self.ranking = [6, is_triple[1], is_pair[1]]
        elif is_triple[0] == 2:
            self.ranking = [6, is_triple[1], is_triple[2]]
        elif is_flush[0] == 1:
            self.ranking = [5, is_flush[1]]
        elif is_straight[0] == 1:
            self.ranking = [4, is_straight[1]]
        elif is_triple[0] == 1:
            self.ranking = [3, is_triple[1]]
        # 페어가 3개인 경우 추가해야함
        elif is_pair[0] == 2:
            self.ranking = [2, is_pair[1], is_pair[2]]
        elif is_pair[0] == 1:
            self.ranking = [1, is_pair[1]]
        else:
            self.ranking = [0]
        # 각 족보에서 5장 이하인 것들은 족보를 제외한 탑 카드들 비교해야함

    def bet(self, blind_bet = None):
        """ Player 의 배팅 함수 """
        if (self.__bet_status != "Fold" and self.__bet_status != "All-In"):
            if (blind_bet != None):
                self.__betting_history.append(blind_bet)
                self.__current_money -= blind_bet
            else:
                select = int(input("배팅 하세요 : 1. 콜\t2. 레이즈\t3. 올인\t4. 폴드"))
                
                if (select == 1):
                    self.__bet_status = "Call"
                elif (select == 2):
                    self.__bet_status = "Raise"
                elif (select == 3):
                    self.__bet_status = "All-In"
                    self.__betting_history.append(self.__current_money)
                    self.__current_money -= self.__current_money
                elif (select == 4):
                    self.__bet_status = "Fold"
        elif (self.__bet_status == "All-In"):
            print("플레이어가 All-In 하여 다음 배팅 순서로 넘어갑니다.")
        elif (self.__bet_status == "Fold"):
            print("플레이어가 Fold 하여 다음 배팅 순서로 넘어갑니다.")

    @property
    def game_status(self):
        return self.__game_status

class ComputerAI(Player):
    """ Computer 클래스 """
    def __init__(self, name, money, position = 0):
        super().__init__(name, money, position)

    def bet(self, blind_bet = None):
        """ 컴퓨터 AI 의 배팅 함수 """
        pass