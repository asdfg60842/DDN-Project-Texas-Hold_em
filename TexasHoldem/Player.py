class Player():
    """ Player 클래스 """
    def __init__(self, name, money, position = 0):
        self.name = name
        self.current_money = money
        self.position = position

        self.hand = []
        self.__game_status = "Alive"
        self.bet_status = None
        self.round_result = None
        self.betting_history = []

    def init_hand(self):
        self.hand = []

    def init_history(self):
        self.position = 0
        self.bet_status = None
        self.round_result = None
        self.betting_history = []

    def add_card(self, aCard):
        self.hand.append(aCard)

    def action_bet(self, game_state = None, std_bet_action = None, min_amount = None, again = False):
        """ Player 의 베팅 선택 함수 """
        # 임시 출력(결과 확인을 위함)
        print()
        if again == True:
            print("누군가 Raise 하여 다시 베팅합니다.")
        print(self.betting_history)
        print("{} : {} 님의 베팅 순서입니다.\t현재 보유 머니 : {}".format(game_state, self.name, self.current_money))
        print("HAND : {} {}, {} {}".format(self.hand[0].suit, self.hand[0].rank, self.hand[1].suit, self.hand[1].rank))
        
        # 플레이어의 이전 선택지가 Fold 또는 All-In일 경우 베팅을 진행할 필요가 없기 때문에 None 리턴
        if self.bet_status == "Fold":
            print("플레이어가 Fold 하여 다음 순서로 넘어갑니다.")
            return None
        elif self.bet_status == "All-In":
            print("플레이어가 All-In 하여 다음 순서로 넘어갑니다.")
            return "All-In"
        elif self.bet_status == "SideBet":
            print("플레이어가 All-In(SideBet) 하여 다음 순서로 넘어갑니다.")
            return "SideBet"
        
        if min_amount != None and self.current_money < min_amount:
            print("현재 보유 금액이 최소 베팅 금액보다 작아 사이드 베팅이 가능합니다.")
            action = int(input("베팅하세요 : 1. Call(All-In)\t2. Fold : "))
            return self.set_bet_status(bet = std_bet_action, action_val = action, side_bet = True)
        
        # std_bet_action에 의해 선택지가 분기됨
        # 이 변수는 Game.py의 Game().bet_in_order()에 의해 기준값이 전달됨
        if std_bet_action == "Raise" or std_bet_action == "Bet":
            action = int(input("베팅하세요 : 1. Call\t2. Bet\t3. All-In\t4. Fold : "))
            return self.set_bet_status(bet = std_bet_action, action_val = action)
        elif std_bet_action == "Call":
            action = int(input("베팅하세요 : 1. Call\t2. Raise\t3. All-In\t4. Fold : "))
            return self.set_bet_status(bet = std_bet_action, action_val = action)
        elif std_bet_action == "Check":
            action = int(input("베팅하세요 : 1. Check\t2. Raise\t3. All-In\t4. Fold : "))
            return self.set_bet_status(bet = std_bet_action, action_val = action)
        print()
    
    def set_bet_status(self, bet, action_val, side_bet = False):
        """ 플레이어가 Console로 입력한 값을 self.bet_status에 저장하고 str로 반환하는 함수 """
        if side_bet == True:
            if action_val == 1:
                self.bet_status = "SideBet"
                return "SideBet"
            elif action_val == 2:
                self.bet_status = "Fold"
                return "Fold"
        else:
            if bet == "Check":
                if action_val == 1:
                    self.bet_status = "Check"
                    return "Check"
            else:
                if action_val == 1:
                    self.bet_status = "Call"
                    return "Call"
        
            if bet == "Raise" or bet == "Bet":
                if action_val == 2:
                    self.bet_status = "Bet"
                    return "Bet"
            else:
                if action_val == 2:
                    self.bet_status = "Raise"
                    return "Raise"
        
            if action_val == 3:
                self.bet_status = "All-In"
                return "All-In"
            elif action_val == 4:
                self.bet_status = "Fold"
                return "Fold"
        
    def bet(self, blind_bet = None, game_state = None, min_amount = None, again = False):
        """ Player 의 베팅 함수 """
        # 베팅의 기본값은 블라인드 값으로 설정
        if min_amount == None:
            min_amount = blind_bet
    
        if game_state == "blind":
            self.betting_history.append([game_state, "blind", blind_bet])
            self.current_money -= blind_bet
            self.position = blind_bet
            return blind_bet
            
        if self.bet_status == "Fold":
            self.betting_history.append([game_state, self.bet_status, 0])
            return 0
        elif self.bet_status == "Check":
            self.betting_history.append([game_state, self.bet_status, 0])
            return 0
        elif self.bet_status == "Call":
            if self.position != 0 and game_state == "preflop":
                diff = min_amount - self.position
                self.betting_history.append([game_state, self.bet_status, diff])
                self.current_money -= diff
            else:
                self.betting_history.append([game_state, self.bet_status, min_amount])
                self.current_money -= min_amount
                    
            return min_amount
        elif self.bet_status == "Raise" or self.bet_status == "Bet":
            if self.position != 0 and game_state == "preflop":
                bet_amount = int(input("베팅할 금액을 입력하세요(최소 금액 {} 초과) : ".format(min_amount)))
                while bet_amount < min_amount:
                    bet_amount = int(input("베팅할 금액은 {} 초과되어야 합니다. 다시 입력해주세요 : ".format(min_amount)))
                diff = bet_amount - self.position
                self.betting_history.append([game_state, self.bet_status, diff])
                self.current_money -= diff
            else:   
                bet_amount = int(input("베팅할 금액을 입력하세요(최소 금액 {} 초과) : ".format(min_amount)))
                while bet_amount < min_amount:
                    bet_amount = int(input("베팅할 금액은 {} 초과되어야 합니다. 다시 입력해주세요 : ".format(min_amount)))
                self.betting_history.append([game_state, self.bet_status, bet_amount])
                self.current_money -= bet_amount
                    
            return bet_amount
        elif self.bet_status == "All-In" or self.bet_status == "SideBet":
            bet_amount = self.current_money
            self.betting_history.append([game_state, self.bet_status, bet_amount])
            self.current_money -= bet_amount
            return bet_amount

    def bet_again(self, game_state = None, min_amount = None):
        """ Player 의 N차 배팅 함수 """
        if self.bet_status == "Fold":
            self.betting_history.append([game_state, self.bet_status, 0])
            return 0
        elif self.bet_status == "Call":
            diff = min_amount
            for state, _, amount in self.betting_history:
                if state == "blind" and game_state == "preflop":
                    diff -= amount
                elif state == game_state:
                    diff -= amount
            self.betting_history.append([game_state, self.bet_status, diff])
            self.current_money -= diff
            return min_amount
        elif self.bet_status == "Raise" or self.bet_status == "Bet":
            bet_amount = int(input("베팅할 금액을 입력하세요(최소 금액 {} 초과) : ".format(min_amount)))
            while bet_amount < min_amount:
                bet_amount = int(input("베팅할 금액은 {} 초과되어야 합니다. 다시 입력해주세요 : ".format(min_amount)))
                
            diff = bet_amount
            for state, _, amount in self.betting_history:
                if state == "blind" and game_state == "preflop":
                    diff -= amount
                elif state == game_state:
                    diff -= amount
            self.betting_history.append([game_state, self.bet_status, diff])
            self.current_money -= diff
            return bet_amount

    def get_bet_amount(self, game_state = None, get_all = False):
        """ Player 가 배팅한 금액 총합 """
        if get_all != True:
            state_amount = 0
            for state, _, amount in self.betting_history:
                if state == "blind" and game_state == "preflop":
                    state_amount += amount
                elif state == game_state:
                    state_amount += amount
        
            return state_amount
        else:
            round_amount = 0
            round_status = None
            for _, status, amount in self.betting_history:
                round_amount += amount
                round_status = status
                
            return round_amount, round_status
        
    @property
    def game_status(self):
        return self.__game_status

class ComputerAI(Player):
    """ Computer 클래스 """
    def __init__(self, name, money, position = 0):
        super().__init__(name, money)

    def bet(self, blind_bet = None, game_state = None):
        """ 컴퓨터 AI 의 베팅 함수 """
        if game_state == "blind":
            self.betting_history.append(blind_bet)
            self.current_money -= blind_bet
            return blind_bet