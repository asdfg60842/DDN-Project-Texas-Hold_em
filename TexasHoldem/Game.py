from Player import *
import random 

TBG_NAME_LIST = ["안병훈", "차희용", "이정우", "김민서", "김동원", "김영일", "권성우", "송정근", "이동규", "이승준"]

class Start:
    """ 게임 시작 클래스 """
    def __init__(self):
        self.set_game = self.game_setup()
    
    def game_setup(self):
        self.num_people = int(input("게임 인원을 입력하세요 : "))
        self.blind_val = int(input("블라인드 최소 배팅 금액을 입력하세요 : "))
        self.money = int(input("초기 시작 금액을 입력하세요 : "))
        self.game_type = input("게임 타입을 입력하세요 : ")

        return Game(num_people = self.num_people, blind_val = self.blind_val, money = self.money, game_type = self.game_type)

class Game:
    """ Game 클래스 """

    def __init__(self, num_people, blind_val, money, game_type):
        self.__NUM_PEOPLE = num_people
        self.__BLIND_VAL = blind_val
        self.__START_MONEY = money
        self.__GAME_TYPE = game_type

        self.players = []
        self.community_card = []

        self.start_sequence()

    def start_sequence(self):
        """ 게임 시작 시퀀스 """
        self.init_player()
        self.init_position()
        self.init_round()
        self.game_loop()

    def init_player(self):
        """ 플레이어 초기화 함수 """
        self.players.append(Player(input("너의 이름은 : "), self.__START_MONEY))
        random.shuffle(TBG_NAME_LIST)
        for i in range(self.__NUM_PEOPLE - 1):
            self.players.append(ComputerAI(TBG_NAME_LIST[i], self.__START_MONEY))   

        for i in range(self.__NUM_PEOPLE):
            print(self.players[i].name)

        print()

        random.shuffle(self.players)
        
        for i in range(self.__NUM_PEOPLE):
            print(self.players[i].name)

    def init_round(self):
        """ 라운드 초기화 함수 """
        pass

    def init_position(self):
        """ 블라인드 초기화 함수 """
        pass
    
    def reinit_position(self):
        """ 블라인드 재설정 함수 """
        pass

    def game_loop(self):
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

