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

        self.__round_result = []
        self.whole_cards = []
        self.ranking = []

    def init_hand(self):
        self.__hand = []

    def init_bet_status(self):
        self.__bet_status = None

    def add_card(self, aCard):
        self.__hand.append(aCard)

    def show_down(self, community_cards):
        self.whole_cards.append(self.__hand)
        self.whole_cards.append(community_cards)

        self.whole_cards.sort(key = lambda own_card: own_card.rank)

        # 족보 판단하는 변수 - 해당 족보의 갯수와 숫자를 저장 ex) 7, 5 투페어: is_pair = [2, 7, 5]
        is_straightflush = [0]
        is_fourcard = [0]
        is_flush = [0]
        is_straight = [0]
        is_triple = [0]
        is_pair = [0]

        # 스티플, 플러쉬 판단
        def straightflush_flush_func(card_list):
            # 문양 갯수 세는 변수
            suit_num = [0, 0, 0, 0]

            for i in range(7):
                suit_num[card_list[i].suit] += 1
            for i in range(4):
                if suit_num[i] >= 5: is_flush[0] = 1

                flush_list = []
                for j in range(7):
                    if card_list[j].suit == i: flush_list.append(card_list[j])
                straight_func(flush_list)
                if is_straight[0] == 1:
                    is_straightflush = is_straight
                    is_straightflush[0] = 1

                for j in range(len(flush_list) - 1, -1, -1):
                    is_flush.append(flush_list[j].rank)

        # 스트레이트 판단
        def straight_func(card_list):
            continuity = 1

            for i in range(7):
                if card_list[i].rank == card_list[i - 1].rank + 1: continuity += 1
                elif card_list[i].rank != card_list[i - 1].rank: continuity = 1

                if continuity >= 5:
                    is_straight[0] = 1
                    is_straight[1] = card_list[i].rank
                    for j in range(1, 5):
                        is_straight.append(card_list[i - j].rank)

        # 페어, 트리플, 포카드 판단
        def pair_triple_fourcard_func(card_list):
            counter = {}
            whole_list = []
            for i in range(7):
                whole_list.append(card_list[i].rank)

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

            if is_pair[0] == 1:
                for i in range(6, -1, -1):
                    if card_list[i].rank != is_pair[1]:
                        is_pair.append(card_list[i])
            if is_pair[0] == 2:
                for i in range(6, -1, -1):
                    if card_list[i].rank != is_pair[1] and card_list[i].rank != is_pair[2]:
                        is_pair.append(card_list[i])
            if is_triple[0] == 1:
                for i in range(6, -1, -1):
                    if card_list[i].rank != is_tirple[1]:
                        is_triple.append(card_list[i])
            if is_fourcard[0] == 1:
                for i in range(6, -1, -1):
                    if card_list[i].rank != is_fourcard[1]:
                        is_fourcard.append(card_list[i])

        straightflush_flush_func(self.whole_cards)
        straight_func(self.whole_cards)
        pair_triple_fourcard_func(self.whole_cards)

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
        if is_straightflush[0] == 1:
            self.ranking = [8, is_straightflush[1]]
        elif is_fourcard[0] == 1:
            self.ranking = [7, is_fourcard[1], fourcard[2]]
        elif is_triple[0] == 1 and is_pair[0] >= 1:
            self.ranking = [6, is_triple[1], is_pair[1]]
        elif is_triple[0] == 2:
            self.ranking = [6, is_triple[1], is_triple[2]]
        elif is_flush[0] == 1:
            self.ranking = [5, is_flush[1]]
        elif is_straight[0] == 1:
            self.ranking = [4, is_straight[1]]
        elif is_triple[0] == 1:
            self.ranking = [3, is_triple[1], is_triple[2]]
        elif is_pair[0] == 3:
            self.ranking = [2, is_pair[1], is_pair[2], is_pair[3]]
        elif is_pair[0] == 2:
            self.ranking = [2, is_pair[1], is_pair[2], is_pair[3]]
        elif is_pair[0] == 1:
            self.ranking = [1, is_pair[1], is_pair[2], is_pair[3], is_pair[4]]
        else:
            self.ranking = [0]
            for i in range(6, 1, -1):
                self.ranking.append(self.whole_cards[i].rank)



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