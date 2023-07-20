from Player import *
from Card import *
import random 

TBG_NAME_LIST = ["안병훈", "차희용", "이정우", "김민서", "김동원", "김영일", "권성우", "송정근", "이동규", "이승준"]

class Start:
    """ 게임 시작 클래스 """
    # 생성자 호출 시 게임 설정 함수 호출하여 Game 클래스의 객체를 반환값으로 받음
    def __init__(self):
        self.set_game = self.game_setup()
    
    # 게임 설정 함수
    # 게임 인원, 블라인드 최솟값, 초기 시드머니, 게임 종료 기준을 입력 받음
    def game_setup(self):
        self.num_people = int(input("게임 인원을 입력하세요 : "))
        self.blind_val = int(input("블라인드 최소 배팅 금액을 입력하세요 : "))
        self.money = int(input("초기 시작 금액을 입력하세요 : "))
        self.game_type = input("게임 타입을 입력하세요 : ")

        return Game(num_people = self.num_people, blind_val = self.blind_val, money = self.money, game_type = self.game_type)

class Game:
    """ Game 클래스 """

    # Start 클래스의 game_setup() 함수를 통해 입력 받은 값을 전달 받음
    def __init__(self, num_people, blind_val, money, game_type):
        # Private, Const 값
        self.__NUM_PEOPLE = num_people
        self.__BLIND_VAL = blind_val
        self.__START_MONEY = money
        self.__GAME_TYPE = game_type
        
        # 게임에 필요한 요소 선언 및 초기화
        self.game_deck = Deck()
        self.dealer = -1
        self.players = []
        self.community_card = []
        
        # 게임 시작 시퀀스 실행
        self.start_sequence()

    def start_sequence(self):
        """ 
        게임 시작 시퀀스 
        게임 시작 전 플레이어 정보, 라운드 초기화
        """
        self.init_player()
        #self.init_position()
        self.init_round()
        self.game_process()
        

    def init_player(self):
        """ 플레이어 정보 초기화 함수 """
        self.players.append(Player(input("너의 이름은 : "), self.__START_MONEY))
        random.shuffle(TBG_NAME_LIST)
        for i in range(self.__NUM_PEOPLE - 1):
            self.players.append(ComputerAI(TBG_NAME_LIST[i], self.__START_MONEY))   

        #for i in range(self.__NUM_PEOPLE):
        #    print(self.players[i].name)
        #print()

        random.shuffle(self.players)
        
        #for i in range(self.__NUM_PEOPLE):
        #    print(self.players[i].name)

    def init_round(self):
        """ 라운드 초기화 함수 """
        self.pot = Pot()
        self.dealer += 1
        self.game_deck.init_deck()
        self.game_deck.shuffled_deck()

    #def init_position(self):
    #    """ 블라인드 초기화 함수 """
    #    pass
    
    #def reinit_position(self):
    #    """ 블라인드 재설정 함수 """
    #    pass

    def game_process(self):
        """ 게임 라운드 한 사이클"""
        while True:
            self.deal_preflop()
            self.deal_flop()
            self.deal_turn()
            self.deal_river()
            self.show_down()

            self.init_round()

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

class Pot:
    def __init__(self):
        self.pot_money = 0