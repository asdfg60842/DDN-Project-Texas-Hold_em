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
        
class ShowDown:
    def __init__(self, hand, community_cards):
        self.whole_cards = []
        self.ranking = []
        
        self.whole_cards.append(hand)
        self.whole_cards.append(community_cards)
        self.whole_cards.sort(key = lambda own_card: own_card.rank)
        
    def show_down(self):
        # 족보 판단하는 변수 - 해당 족보의 갯수와 숫자를 저장 ex) 7, 5 투페어: self.is_pair = [2, 7, 5]
        self.self.is_straightflush = [0]
        self.is_fourcard = [0]
        self.is_flush = [0]
        self.is_straight = [0]
        self.is_triple = [0]
        self.is_pair = [0]

        self.straightflush_flush_func(self.whole_cards)
        self.straight_func(self.whole_cards)
        self.pair_triple_fourcard_func(self.whole_cards)

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
        if self.self.is_straightflush[0] == 1:
            self.ranking = [8, self.self.is_straightflush[1]]
        elif self.is_fourcard[0] == 1:
            self.ranking = [7, self.is_fourcard[1], self.is_fourcard[2]]
        elif self.is_triple[0] == 1 and self.is_pair[0] >= 1:
            self.ranking = [6, self.is_triple[1], self.is_pair[1]]
        elif self.is_triple[0] == 2:
            self.ranking = [6, self.is_triple[1], self.is_triple[2]]
        elif self.is_flush[0] == 1:
            self.ranking = [5, self.is_flush[1]]
        elif self.is_straight[0] == 1:
            self.ranking = [4, self.is_straight[1]]
        elif self.is_triple[0] == 1:
            self.ranking = [3, self.is_triple[1], self.is_triple[2]]
        elif self.is_pair[0] == 3:
            self.ranking = [2, self.is_pair[1], self.is_pair[2], self.is_pair[3]]
        elif self.is_pair[0] == 2:
            self.ranking = [2, self.is_pair[1], self.is_pair[2], self.is_pair[3]]
        elif self.is_pair[0] == 1:
            self.ranking = [1, self.is_pair[1], self.is_pair[2], self.is_pair[3], self.is_pair[4]]
        else:
            self.ranking = [0]
            for i in range(6, 1, -1):
                self.ranking.append(self.whole_cards[i].rank)
                
    # 스티플, 플러쉬 판단
    def straightflush_flush_func(self, card_list):
        # 문양 갯수 세는 변수
        suit_num = [0, 0, 0, 0]
        for i in range(7):
            suit_num[card_list[i].suit] += 1
        for i in range(4):
            if suit_num[i] >= 5: self.is_flush[0] = 1
            flush_list = []
            for j in range(7):
                if card_list[j].suit == i: flush_list.append(card_list[j])
            self.straight_func(flush_list)
            if self.is_straight[0] == 1:
                self.self.is_straightflush = self.is_straight
                self.self.is_straightflush[0] = 1
            for j in range(len(flush_list) - 1, -1, -1):
                self.is_flush.append(flush_list[j].rank)
                
    # 스트레이트 판단
    def straight_func(self, card_list):
        continuity = 1
        for i in range(7):
            if card_list[i].rank == card_list[i - 1].rank + 1: continuity += 1
            elif card_list[i].rank != card_list[i - 1].rank: continuity = 1
            if continuity >= 5:
                self.is_straight[0] = 1
                self.is_straight[1] = card_list[i].rank
                for j in range(1, 5):
                    self.is_straight.append(card_list[i - j].rank)
                    
    # 페어, 트리플, 포카드 판단
    def pair_triple_fourcard_func(self, card_list):
        counter = {}
        whole_list = []
        for i in range(7):
            whole_list.append(card_list[i].rank)
        for num in whole_list:
            try: counter[num] += 1
            except: counter[num] = 1
        for num in counter.keys:
            if counter[num] == 2:
                self.is_pair[0] += 1
                self.is_pair.insert(1, num)
            if counter[num] == 3:
                self.is_triple[0] += 1
                self.is_triple.insert(1, num)
            if counter[num] == 4:
                self.is_fourcard[0] += 1
                self.is_fourcard.append(num)
        if self.is_pair[0] == 1:
            for i in range(6, -1, -1):
                if card_list[i].rank != self.is_pair[1]:
                    self.is_pair.append(card_list[i])
        if self.is_pair[0] == 2:
            for i in range(6, -1, -1):
                if card_list[i].rank != self.is_pair[1] and card_list[i].rank != self.is_pair[2]:
                    self.is_pair.append(card_list[i])
        if self.is_triple[0] == 1:
            for i in range(6, -1, -1):
                if card_list[i].rank != self.is_triple[1]:
                    self.is_triple.append(card_list[i])
        if self.is_fourcard[0] == 1:
            for i in range(6, -1, -1):
                if card_list[i].rank != self.is_fourcard[1]:
                    self.is_fourcard.append(card_list[i])