class Player():
    """ Player 클래스 """
    def __init__(self, name, money, position = 0):
        self.name = name
        self.current_money = money
        self.position = position

        self.hand = []
        self.__game_status = "Alive"
        self.bet_status = None
        self.betting_history = []
        self.round_result = None
        self.whole_cards = []
        self.ranking = []

    def init_hand(self):
        self.hand = []

    def init_bet_status(self):
        self.bet_status = None

    def add_card(self, aCard):
        self.hand.append(aCard)

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
            if suit_num[i] >= 5: 
                is_flush[0] = 1
            if self.whole_cards[6].suit == i: 
                is_flush[1] = self.whole_cards[6].rank
            elif self.whole_cards[5].suit == i: 
                is_flush[1] = self.whole_cards[5].rank
            elif self.whole_cards[4].suit == i: 
                is_flush[1] = self.whole_cards[4].rank

        # 스트레이트 판단
        whole_list = []
        whole_set_list = []

        for i in range(7):
            whole_list.append(self.whole_cards[i].rank)

        whole_set_list = list(set(self.whole_list))
        continuity = 1

        for i in range(1, len(whole_set_list)):
            if whole_set_list[i] == whole_set_list[i - 1] + 1: 
                continuity += 1
            else: 
                continuity = 1

            if continuity >= 5:
                is_straight[0] = 1
                is_straight[1] = whole_set_list[i]

        # 페어, 트리플, 포카드 판단
        counter = {}

        for num in whole_list:
            try: 
                counter[num] += 1
            except: 
                counter[num] = 1

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

    def select_bet(self, game_state = None, std_bet_select = None, again = False):
        """ Player 의 배팅 선택 함수 """
        # 임시 출력(결과 확인을 위함)
        print()
        if again == True:
            print("누군가 Raise 하여 다시 배팅합니다.")
        print(self.betting_history)
        print("{} : {} 님의 배팅 순서입니다.".format(game_state, self.name))
        print("HAND : {} {}, {} {}".format(self.hand[0].suit, self.hand[0].rank, self.hand[1].suit, self.hand[1].rank))
        
        # 플레이어의 이전 선택지가 Fold 또는 All-In일 경우 배팅을 진행할 필요가 없기 때문에 None 리턴
        if self.bet_status == "Fold":
            print("플레이어가 Fold 하여 다음 순서로 넘어갑니다.")
            return
        elif self.bet_status == "All-In":
            print("플레이어가 All-In 하여 다음 순서로 넘어갑니다.")
            return
        
        # std_bet_select에 의해 선택지가 분기됨
        # 이 변수는 Game.py의 Game().bet_in_order()에 의해 기준값이 전달됨
        if std_bet_select == "Raise" or std_bet_select == "Bet":
            select = int(input("배팅하세요 : 1. Call\t2. Bet\t3. All-In\t4. Fold : "))
            return self.set_bet_status(bet = std_bet_select, val = select)
        elif std_bet_select == "Call":
            select = int(input("배팅하세요 : 1. Call\t2. Raise\t3. All-In\t4. Fold : "))
            return self.set_bet_status(bet = std_bet_select, val = select)
        elif std_bet_select == "Check":
            select = int(input("배팅하세요 : 1. Check\t2. Raise\t3. All-In\t4. Fold : "))
            return self.set_bet_status(bet = std_bet_select, val = select)
        print()
    
    def set_bet_status(self, bet, val):
        """ 플레이어가 Console로 입력한 값을 self.bet_status에 저장하고 str로 반환하는 함수 """
        if bet == "Check":
            if val == 1:
                self.bet_status = "Check"
                return "Check"
        else:
            if val == 1:
                self.bet_status = "Call"
                return "Call"
        
        if bet == "Raise" or bet == "Bet":
            if val == 2:
                self.bet_status = "Bet"
                return "Bet"
        else:
            if val == 2:
                self.bet_status = "Raise"
                return "Raise"
        
        if val == 3:
            self.bet_status = "All-In"
            return "All-In"
        elif val == 4:
            self.bet_status = "Fold"
            return "Fold"
        
    def bet(self, blind_bet = None, game_state = None, min_amount = None, again = False):
        """ Player 의 배팅 함수 """
        # 배팅의 기본값은 블라인드 값으로 설정
        if min_amount == None:
            min_amount = blind_bet

        if game_state == "blind":
            self.betting_history.append([game_state, "blind", blind_bet])
            self.current_money -= blind_bet
            self.position = blind_bet
            return blind_bet
        if self.bet_status == "Fold":
            self.betting_history.append([game_state, self.bet_status, None])
            return "Fold"
        elif self.bet_status == "Check":
            self.betting_history.append([game_state, self.bet_status, 0])
            return "Check"
        elif self.bet_status == "Call":
            # 다시 배팅을 진행하는지를 판단하는 again 변수로 Raise된 값에 이전 배팅한 값을 차감하여 배팅
            if again == True:
                extra_pay = min_amount - self.betting_history[len(self.betting_history) - 1][2]
                self.betting_history.append([game_state, self.bet_status, extra_pay])
                self.current_money -= extra_pay
            # 혹은 플레이어가 블라인드인 경우 preflop 단계에서 블라인드 값을 차감하고 배팅 진행
            elif self.position != 0 and game_state == "preflop":
                self.betting_history.append([game_state, self.bet_status, min_amount - self.position])
                self.current_money = min_amount - self.position
            else:
                self.betting_history.append([game_state, self.bet_status, min_amount])
                self.current_money -= min_amount
            return min_amount
        elif self.bet_status == "Raise" or self.bet_status == "Bet":
            # Call과 동일
            if again == True:
                bet_amount = int(input("배팅할 금액을 입력하세요(최소 금액 {} 초과) : ".format(min_amount)))
                while bet_amount < min_amount:
                    bet_amount = int(input("배팅할 금액은 {} 초과되어야 합니다. 다시 입력해주세요 : ".format(min_amount)))
                extra_pay = bet_amount - self.betting_history[len(self.betting_history) - 1][2]
                self.betting_history.append([game_state, self.bet_status, extra_pay])
                self.current_money -= extra_pay
            elif self.position != 0 and game_state == "preflop":
                bet_amount = int(input("배팅할 금액을 입력하세요(최소 금액 {} 초과) : ".format(min_amount)))
                while bet_amount < min_amount:
                    bet_amount = int(input("배팅할 금액은 {} 초과되어야 합니다. 다시 입력해주세요 : ".format(min_amount)))
                self.betting_history.append([game_state, self.bet_status, bet_amount - self.position])
                self.current_money = bet_amount - self.position
            else:
                bet_amount = int(input("배팅할 금액을 입력하세요(최소 금액 {} 초과) : ".format(min_amount)))
                while bet_amount < min_amount:
                    bet_amount = int(input("배팅할 금액은 {} 초과되어야 합니다. 다시 입력해주세요 : ".format(min_amount)))
                self.betting_history.append([game_state, self.bet_status, bet_amount])
                self.current_money -= bet_amount
            return bet_amount
        elif self.bet_status == "All-In":
            bet_amount = self.current_money
            self.betting_history.append([game_state, self.bet_status, bet_amount])
            self.current_money -= bet_amount
            return bet_amount

    @property
    def game_status(self):
        return self.__game_status

class ComputerAI(Player):
    """ Computer 클래스 """
    def __init__(self, name, money, position = 0):
        super().__init__(name, money)

    def bet(self, blind_bet = None, game_state = None):
        """ 컴퓨터 AI 의 배팅 함수 """
        if game_state == "blind":
            self.betting_history.append(blind_bet)
            self.current_money -= blind_bet
            return blind_bet