import random

class Community:
    """ Community 클래스 """
    def __init__(self):
        self.__community_cards = []

    def init_community_cards(self):
        self.__community_cards = []

    def add_card(self, aCard):
        self.__community_cards.append(aCard)

    @property
    def community_cards(self):
        return self.__community_cards

class Card:
    """ Card 클래스 """
    def __init__(self, suit, rank):
        self.__suit = suit
        self.__rank = rank

    @property
    def suit(self):
        return self.__suit
    
    @property
    def rank(self):
        return self.__rank

class Deck:
    """ Deck 클래스 """
    def __init__(self):
        self.deck_cards = []

    def init_deck(self):
        self.deck_cards = []

        for i in range(0, 4):
            for j in range(1, 14):
                self.deck_cards.append(Card(i, j))

    def shuffled_deck(self):
        shuffled_cards = []

        #write some codes for shuffle deck
        for i in range(len(self.deck_cards)):
            if len(self.deck_cards) > 1:
                c = random.choice(self.deck_cards)
                shuffled_cards.append(c)
                self.deck_cards.remove(c)
            else:
                c = self.deck_cards.pop()
                shuffled_cards.append(c)
        self.deck_cards = shuffled_cards

    def pop_card(self):
        return self.deck_cards.pop()
    
    def burn_card(self):
        self.deck_cards.pop()