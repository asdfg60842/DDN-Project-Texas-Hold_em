class Game:
    """ Game 클래스 """

    def __init__(self, num_people, blind_val, money, game_type):
        self.NUM_PEOPLE = num_people
        self.BLIND_VAL = blind_val
        self.MONEY = money
        self.GAME_TYPE = game_type

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

