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

    def init_hand(self):
        self.__hand = []

    def init_bet_status(self):
        self.__bet_status = None

    def add_card(self, aCard):
        self.__hand.append(aCard)

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