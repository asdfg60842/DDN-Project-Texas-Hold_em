import random

class Community:
    """ Community 클래스 """
    def __init__(self):
        self.community_cards = []

    def add_card(self, aCard):
        self.community_cards.append(aCard)

class Card:
    """ Card 클래스 """
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

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
        for i in (0, 4):
            for j in (0, 13):
                self.deck_cards.append(Card(i, j))

    def shuffled_deck(self):
        random.shuffle(self.deck_cards)

    def pop_card(self, trash_val = 0):
        if trash_val == 1:
            return
        else:
            return self.deck_cards.pop()