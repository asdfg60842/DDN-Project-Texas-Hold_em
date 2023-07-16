from Player import *

class Game:
    """ Game 클래스 """

    def __init__(self, num_people, blind_val, money, game_type):
        self.__NUM_PEOPLE = num_people
        self.__BLIND_VAL = blind_val
        self.__START_MONEY = money
        self.__GAME_TYPE = game_type

        self.players = []
        self.community_card = []

    def start_sequence(self):
        """ 게임 시작 시퀀스 """
        pass

    def init_player(self):
        """ 플레이어 초기화 함수 """
        pass

    def init_round(self):
        """ 라운드 초기화 함수 """
        pass

    def init_position(self):
        """ 블라인드 초기화 함수 """
        pass
    
    def reinit_position(self):
        """ 블라인드 재설정 함수 """
        pass

    def deal_preflop(self):
        """ 프리플랍 단계 """
        pass

    def deal_flop(self):
        """ 플랍 단계 """
        pass

    def deal_turn(self):
        """ 턴 단계 """
        pass

    def deal_river(self):
        """ 리버 단계 """
        pass

    def show_down(self):
        """ 쇼다운(승자 결정) 단계 """
        pass

