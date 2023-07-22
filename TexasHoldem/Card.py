import random

class Community:
    """ Community 클래스 """
    def init(self):
        self.community_cards = []

    def init_community_cards(self):
        self.community_cards = []

    def add_card(self, aCard):
        self.community_cards.append(aCard)

    @property
    def community_cards(self):
        return self.community_cards

class Card:
    """ Card 클래스 """
    def __init__(self, suit, rank):
        self.__suit = suit
        self.__rank = rank

    @property
    def suit(self):
        return self.suit
    
    @property
    def rank(self):
        return self.rank

class Deck:
    """ Deck 클래스 """
    def __init__(self):
        self.deck_cards = []

    def init_deck(self):
        for suit in (0, 4):
            for rank in (1, 14):
                self.deck_cards.append(Card(suit, rank))

    def shuffled_deck(self):
        random.shuffle(self.deck_cards)

    def pop_card(self, trash_val = 0):
        if trash_val == 1:
            return
        else:
            return self.deck_cards.pop()