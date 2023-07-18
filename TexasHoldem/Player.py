class Player:
    """ Player 클래스 """
    def __init__(self, name, money, position = 0):
        self.name = name
        self.__current_money = money
        self.__position = position

        self.__hand = []
        self.__betting_history = []
        self.__round_result = None
        

    def betting(self):
        """ Player 의 배팅 함수 """
        pass

class ComputerAI(Player):
    """ Computer 클래스 """
    def __init__(self, name, money, position = 0):
        super().__init__(name, money, position)

    def betting(self):
        """ 컴퓨터 AI 의 배팅 함수 """
        pass