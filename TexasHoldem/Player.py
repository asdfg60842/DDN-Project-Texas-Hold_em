class Player:
    """ Player 클래스 """
    def __init__(self, name, money, position):
        self.__name = name
        self.__current_money = money
        self.__position = position
        self.__hand = []
        self.__round_result = None

    def betting(self):
        pass

class ComputerAI(Player):
    """ Computer 클래스 """
    def __init__(self, name, money, position):
        pass

class Community:
    """ Community 클래스 """
    def __init__(self):
        pass

    def add_card(self):
        pass

class Card:
    """ Card 클래스 """
    def __init__(self):
        pass

class Deck:
    """ Deck 클래스 """
    def __init__(self):
        self.deck_card = []

    def init_deck(self):
        pass

    def shuffled_card(self):
        pass

    def pop_card(self):
        pass