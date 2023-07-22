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
        self.num_player = int(input("게임 인원을 입력하세요 : "))
        self.blind_val = int(input("블라인드 최소 배팅 금액을 입력하세요(빅 블라인드 기준) : "))
        self.money = int(input("초기 시작 금액을 입력하세요 : "))
        self.game_type = input("게임 타입을 입력하세요 : ")

        return Game(num_player = self.num_player, blind_val = self.blind_val, money = self.money, game_type = self.game_type)

class Game:
    """ Game 클래스 """

    # Start 클래스의 game_setup() 함수를 통해 입력 받은 값을 전달 받음
    def __init__(self, num_player, blind_val, money, game_type):
        # Private, Const 값
        self.__NUM_PLAYER = num_player
        self.__BLIND_VAL = blind_val
        self.__START_MONEY = money
        self.__GAME_TYPE = game_type
        
        # 게임에 필요한 요소 선언 및 초기화
        self.game_deck = Deck()
        self.community_cards = Community()
        self.dealer = -1
        self.current_num_player = self.__NUM_PLAYER
        self.players = []
        
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
        for i in range(self.__NUM_PLAYER - 1):
            self.players.append(ComputerAI(TBG_NAME_LIST[i], self.__START_MONEY))   

        #for i in range(self.__NUM_PLAYER):
        #    print(self.players[i].name)
        #print()

        random.shuffle(self.players)
        
        #for i in range(self.__NUM_PLAYER):
        #    print(self.players[i].name)

    def init_round(self):
        """ 라운드 초기화 함수 """
        self.init_position()
        self.pot = Pot()
        self.game_deck.init_deck()
        self.game_deck.shuffled_deck()
        self.community_cards.init_community_cards()

        for player in self.players:
            if (player.game_status == "Alive"):
                player.init_hand()
                player.init_bet_status()
            elif (player.game_status == "Die"):
                self.players.remove(player)
                self.current_num_player -= 1
                

    def init_position(self):
        """ 블라인드 초기화 함수 """
        if (self.dealer != len(self.players)):
            self.dealer += 1
        else:
            self.dealer = 0
    
    def game_process(self):
        """ 게임 라운드 한 사이클"""
        while True:
            self.deal_blind()
            self.deal_preflop()
            self.deal_flop()
            self.deal_turn()
            self.deal_river()
            self.show_down()

            self.init_round()        

    def deal_blind(self):
        self.small_blind = (self.dealer + 1) % self.current_num_player
        self.big_blind = (self.dealer + 2) % self.current_num_player

        self.players[self.small_blind].bet(blind_bet = self.__BLIND_VAL // 2)
        self.players[self.big_blind].bet(blind_bet = self.__BLIND_VAL)

    def deal_preflop(self):
        """ 프리플랍 단계 """
        blind_next = (self.big_blind + 1) % self.current_num_player

        for i in range(self.current_num_player * 2):
            self.players[i % self.current_num_player].add_card(self.game_deck.pop_card())

        for i in range(blind_next, self.current_num_player):
            self.players[i].bet()

        for i in range(0, blind_next):
            self.players[i].bet()

    def deal_flop(self):
        """ 플랍 단계 """
        self.game_deck.burn_card()

        for _ in range(3):
            self.community_cards.append(self.game_deck.pop_card())

        self.bet_in_order()

    def deal_turn(self):
        """ 턴 단계 """
        self.game_deck.burn_card()
        self.community_cards.append(self.game_deck.pop_card())
        self.bet_in_order()

    def deal_river(self):
        """ 리버 단계 """
        self.game_deck.burn_card()
        self.community_cards.append(self.game_deck.pop_card())
        self.bet_in_order()

    def show_down(self):
        """ 쇼다운(승자 결정) 단계 """

        pass
    
    def bet_in_order(self):
        """ 순서대로 배팅 진행 """
        for i in range(self.small_blind, self.current_num_player):
            self.players[i].bet()
        
        for i in range(0, self.small_blind):
            self.players[i].bet()

class Pot:
    def __init__(self):
        self.pot_money = 0