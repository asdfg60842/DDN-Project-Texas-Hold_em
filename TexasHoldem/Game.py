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
        self.blind_val = int(input("블라인드 최소 베팅 금액을 입력하세요(빅 블라인드 기준) : "))
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
        self.players_bet_log = BetLog()
        self.dealer = -1
        self.num_round = -1
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
        self.init_round()
        self.game_process()
        

    def init_player(self):
        """ 플레이어 정보 초기화 함수 """
        self.players.append(Player(input("너의 이름은 : "), self.__START_MONEY))
        random.shuffle(TBG_NAME_LIST)
        for i in range(1, self.__NUM_PLAYER):
            self.players.append(Player(TBG_NAME_LIST[i], self.__START_MONEY))   
        random.shuffle(self.players)

    def init_round(self):
        """ 라운드 초기화 함수 """
        self.init_position()
        self.pot = Pot()
        self.game_deck.init_deck()
        self.game_deck.shuffled_deck()
        self.community_cards.init_community_cards()
        self.players_bet_log.init_round_log()
        self.num_round += 1

        for player in self.players:
            if (player.game_status == "Alive"):
                player.init_hand()
                player.init_history()
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
        """ 게임 라운드 한 사이클 """
        while True:
            self.deal_blind()
            self.deal_preflop()
            self.deal_flop()
            self.deal_turn()
            self.deal_river()
            self.show_down()
            print("승자는 총 {} 만큼의 상금을 얻었습니다!".format(self.pot.pot_money))
            self.init_round()        

    def deal_blind(self):
        self.small_blind = (self.dealer + 1) % self.current_num_player
        self.big_blind = (self.dealer + 2) % self.current_num_player

        # 블라인드 베팅
        sb = self.players[self.small_blind].bet(blind_bet = self.__BLIND_VAL // 2, game_state = "blind")
        bb = self.players[self.big_blind].bet(blind_bet = self.__BLIND_VAL, game_state = "blind")

        # 모든 플레이어 베팅 로그는 add_bet_log() 함수를 통해 저장됨
        self.players_bet_log.add_bet_log(nround = self.num_round, game_state = "blind", player_name = self.players[self.small_blind].name, bet = "small_blind", bet_amount = sb)
        self.players_bet_log.add_bet_log(nround = self.num_round, game_state = "blind", player_name = self.players[self.big_blind].name, bet = "big_blind", bet_amount = bb)
        
        # 임시 출력(결과 확인을 위함)
        print(self.players_bet_log.bet_log)
        print("Dealer : {}".format(self.players[self.dealer].name))
        print("SmallBlind : {}".format(self.players[self.small_blind].name))
        print("BigBlind : {}".format(self.players[self.big_blind].name))

    def deal_preflop(self):
        """ 프리플랍 단계 """
        # UTG(Under The Gun) : 빅 블라인드 바로 왼쪽 위치. 프리플랍에서 가장 처음 액션을 하는 플레이어
        under_the_gun = (self.big_blind + 1) % self.current_num_player

        # 카드 1장씩 모든 플레이어에게 총 2장 배분
        for i in range(2):
            # small_blind 부터 ~ 마지막 index 플레이어까지 카드 배분
            for j in range(self.small_blind, self.current_num_player):
                self.players[j].add_card(self.game_deck.pop_card())
            # 첫번째 index 플레이어 ~ 딜러까지 카드 배분
            for j in range(0, self.small_blind):
                self.players[j].add_card(self.game_deck.pop_card())

        # 베팅 기록을 위한 단계별 키(key) 생성
        self.players_bet_log.add_state_log(nround = self.num_round, game_state = "preflop")

        # UTG(언더 더 건) 부터 IP(인 포지션 : big_blind)까지 베팅
        self.bet_in_order(order = under_the_gun, state = "preflop")
        

    def deal_flop(self):
        """ 플랍 단계 """
        # burn_card() 함수 호출로 베팅 전 탑 카드를 버림
        self.game_deck.burn_card()

        # 모든 플레이어가 사용가능한 커뮤니티 카드 3장 배분
        for _ in range(3):
            self.community_cards.add_card(self.game_deck.pop_card())

        # 베팅 기록을 위한 단계별 키(key) 생성
        self.players_bet_log.add_state_log(nround = self.num_round, game_state = "flop")

        # OOP(아웃 오브 포지션 : small_blind)부터 IP(인 포지션 : dealer)까지 베팅
        self.bet_in_order(order = self.small_blind, state = "flop")

    def deal_turn(self):
        """ 턴 단계 """
        self.game_deck.burn_card()

        # 모든 플레이어가 사용가능한 커뮤니티 카드 1장 배분
        self.community_cards.add_card(self.game_deck.pop_card())
        self.players_bet_log.add_state_log(nround = self.num_round, game_state = "turn")
        self.bet_in_order(order = self.small_blind, state = "turn")

    # deal_turn() 함수와 동일한 동작을 하므로 주석 생략
    def deal_river(self):
        """ 리버 단계 """
        self.game_deck.burn_card()
        self.community_cards.add_card(self.game_deck.pop_card())
        self.players_bet_log.add_state_log(nround = self.num_round, game_state = "river")
        self.bet_in_order(order = self.small_blind, state = "river")

    def show_down(self):
        """ 쇼다운(승자 결정) 단계 """
        # 사이드 베팅을 진행한 플레이어가 있을때 함수 호출
        for player in self.players:
            if player.bet_status == "SideBet":
                self.sidepot_show_down()
    
    def sidepot_show_down(self):
        """ 사이드 베팅 쇼다운 """
        # 플레이어의 라운드 결과를 저장하는 리스트(이름, 총 베팅 금액, 최종 베팅 액션)
        round_result = []
        # 사이드 팟 분리
        # index 0부터 메인팟, 세컨팟, 서드팟 ,,, 
        side_pot = []
        # 폴드한 플레이어의 팟
        # index 0부터 메인팟, 세컨팟, 서드팟 ,,, 에 추가
        fold_pot = []
        # 사이드 팟의 최종 금액(사이드팟 + 폴드팟)
        final_pot = []
        
        side_bet_player = []
        default_bet_player = []
        
        for player in self.players:
            amount, player_status = player.get_bet_amount(get_all = True)
            round_result.append([player, amount, player_status])

            if player_status == "SideBet":
                if amount not in side_pot:
                    side_pot.append(amount)
                side_bet_player.append(player)
            elif player_status != "Fold":
                if amount not in side_pot:
                    side_pot.append(amount)
                side_bet_player.append(player)
                default_bet_player.append(player)
            elif player_status == "Fold":
                fold_pot.append([amount])
        
        side_pot.sort()
        for i in range(len(side_pot), 1, -1):
            side_pot[i] -= side_pot[i - 1]
        
        for i in range(len(fold_pot)):
            for j in range(len(side_pot)):
                if fold_pot[i][0] >= side_pot[j]:
                    fold_pot[i][0] -= side_pot[j]
                    fold_pot[i].append(side_pot[j])
                elif fold_pot[i][0] < side_pot[j]:
                    fold_pot[i].append(fold_pot[i][0])
                    fold_pot[i].pop(0)
                    break
                
            if 0 in fold_pot[i]:
                fold_pot[i].remove(0)
        
        # 사이드팟 중복 인원 수 카운트
        # 사이드팟에 해당하는 플레이어 수 만큼 곱 연산 후 폴드 팟 + 연산 하여 final_pot 완성
        # 이후 showdown으로 각 사이드팟에 해당하는 플레이어 비교
                    
        
    def bet_in_order(self, order, state = None):
        """ 순서대로 베팅 진행 """
        # 베팅 금액의 최솟값 지정 (처음 기본값은 블라인드 값)
        min_amount_val = self.__BLIND_VAL
        # 플레이어의 베팅 액션 저장 (Raise, Bet, Check 구분)
        action_val = None
        # 베팅을 다시해야하는 경우의 시작 순서
        bet_again = None
        # 게임 state에 걸린 pot
        state_pot = 0
        # bet_action_val : 플레이어의 액션 저장
        bet_action_val = None
        # bet_amount_val : 플레이어가 베팅한 금액 저장
        bet_amount_val = 0
        
        # 베팅 프로세스
        def bet_process(idx, action, min):
            action = self.players[idx].action_bet(game_state = state, std_bet_action = action, min_amount = min)
            amount = self.players[idx].bet(game_state = state, min_amount = min)
            self.players_bet_log.add_bet_log(nround = self.num_round, game_state = state, player_name = self.players[idx].name, \
                                            bet = action, bet_amount = amount)
            return action, amount
                
        # preflop : UTG(언더 더 건) ~ 마지막 index 플레이어까지 베팅
        # flop, turn, river : OOP(아웃 오브 포지션 : small_blind) ~ 마지막 index 플레이어까지 베팅
        for i in range(order, self.current_num_player):
            # 베팅 로그로부터 해당 단계에서 모든 플레이어의 베팅 액션 가져옴
            action_log = list(self.players_bet_log.bet_log[self.num_round][state][0]["bet1"].values())

            # 리스트의 길이만큼 반복 후 Raise 또는 Bet에 해당하는 값이 있으면(즉, 게임에서 Raise나 Bet을 플레이(선택)한 플레이어가 있으면) action_val에 저장
            for j in range(len(action_log)):
                if action_log[j].get("bet") == "Raise":
                    action_val = "Raise"
                elif action_log[j].get("bet") == "Bet":
                    action_val = "Bet"

            # bet_action_val : 플레이어의 액션 저장
            # bet_amount_val : 플레이어가 베팅한 금액 저장
            # preflop 베팅 제한사항 : 빅 블라인드를 제외한 모든 플레이어는 Check 할 수 없음
            if state == "preflop" and i == order:
                bet_action_val, bet_amount_val = bet_process(idx = i, action = "Call", min = min_amount_val)   
            # 공통 제한사항 : 만약 이전 플레이어가 Raise를 했을 경우 다음 플레이어는 Call/Bet/All-In/Fold의 액션 선택지를 가짐
            # Raise를 플레이(선택)한 플레이어의 이전에 베팅했던 플레이어는 다시 베팅을 진행해야함
            # 단, Bet을 플레이(선택)했을 경우 이전에 Raise한 플레이어도 다시 베팅을 진행해야함
            elif action_val == "Raise" or action_val == "Bet":
                bet_action_val, bet_amount_val = bet_process(idx = i, action = action_val, min = min_amount_val)
            # 가장 처음 베팅을 하게되는 OOP(아웃 오브 포지션 : small_blind)의 경우 Check가 가능함
            # 따라서 모든 플레이어가 Check를 했는지 또는 한 플레이어가 Raise를 했는지 판단하여 액션 선택지 호출
            else:
                is_check_available = 1
                for k in range(self.current_num_player):
                    try:
                        bet_list = self.players_bet_log.bet_log[self.num_round][state][0]["bet1"][self.players[k].name]["bet"]
                        if bet_list == "Check":
                            continue 
                        else:
                            is_check_available = 0
                            break
                    except KeyError:
                        break
                
                # preflop의 경우 빅블라인드를 제외하고 Check가 불가능함
                if is_check_available == 1 and state != "preflop":
                    bet_action_val, bet_amount_val = bet_process(idx = i, action = "Check", min = min_amount_val)
                # is_check_available == 0인 경우 Call 액션 선택지 호출
                else: 
                    bet_action_val, bet_amount_val = bet_process(idx = i, action = "Call", min = min_amount_val)
            
            # 플레이어 베팅 loop 에서 Fold나 Check를 플레이(선택)한 경우 베팅 금액을 입력하지 않기 때문에 최소 베팅금액인 min_amount_val 비교에서 제외
            # 즉, 플레이어 중 Raise 또는 Bet을 플레이(선택)한 플레이어가 베팅한 금액이 최소 베팅금액이 됨
            if bet_action_val != "Fold" and bet_action_val != "Check" and bet_action_val != None:
                if min_amount_val < bet_amount_val:
                    min_amount_val = bet_amount_val
            
            # Raise 또는 Bet을 플레이(선택)한 플레이어의 순서(index)를 저장
            if bet_action_val == "Raise" or bet_action_val == "Bet":
                bet_again = i

        # preflop : 첫번째 index 플레이어부터 IP(인 포지션 : big_blind)까지 베팅
        # flop, turn, river : 첫번째 index 플레이어부터 IP(인 포지션 : dealer)까지 베팅
        # 위의 for loop와 동일한 기능을 하므로 주석 생략
        for i in range(0, order):
            action_log = list(self.players_bet_log.bet_log[self.num_round][state][0]["bet1"].values())

            for j in range(len(action_log)):
                if action_log[j].get("bet") == "Raise":
                    action_val = "Raise"
                elif action_log[j].get("bet") == "Bet":
                    action_val = "Bet"
            
            if action_val == "Raise" or action_val == "Bet":
                bet_action_val, bet_amount_val = bet_process(idx = i, action = action_val, min = min_amount_val)
            # preflop에서 IP(인 포지션 : big_blind)인 빅블라인드는 Option(이전 베팅에서 Raise, Bet이 없을 경우 빅블라인드가 Raise와 Check 선택 가능)
            else:
                is_check_available = 1
                for k in range(self.current_num_player):
                    try:
                        bet_list = self.players_bet_log.bet_log[self.num_round][state][0]["bet1"][self.players[k].name]["bet"]
                        if bet_list == "Check": 
                            continue 
                        elif state == "preflop" and i == order - 1:
                            continue
                        else:
                            is_check_available = 0
                            break
                    except KeyError:
                        if state == "preflop" and i != order - 1:
                            is_check_available = 0
                            break
                        else:
                            break

                if is_check_available == 1:
                    bet_action_val, bet_amount_val = bet_process(idx = i, action = "Check", min = min_amount_val)
                else: 
                    bet_action_val, bet_amount_val = bet_process(idx = i, action = "Call", min = min_amount_val)
            
            if bet_action_val != "Fold" and bet_action_val != "Check" and bet_action_val != None:
                if min_amount_val < bet_amount_val:
                    min_amount_val = bet_amount_val
            
            if bet_action_val == "Raise" or bet_action_val == "Bet":
                bet_again = i

        # Raise 또는 Bet을 플레이(선택)한 플레이어의 인덱스를 기준으로 다시 베팅을 하는 함수 호출
        if bet_again != None:
            if bet_again == order:
                return
            else:
                self.bet_in_again(order1 = order, order2 = bet_again, state = state, min_amount_val = min_amount_val)
        # 다시 베팅을 진행하지 않는 경우 state에 걸린 pot을 라운드 전체 pot에 더한다
        else:
            self.players_bet_log.add_state_result_log(nround = self.num_round, game_state = state)
            
            for i in range(self.current_num_player):
                self.players_bet_log.add_bet_log(nround = self.num_round, game_state = state, player_name = self.players[i].name, \
                                                bet = self.players[i].bet_status, bet_amount = self.players[i].get_bet_amount(game_state = state), \
                                                bet_n = 1, str_bet_n = "result")
                state_pot += self.players[i].get_bet_amount(game_state = state)
            self.pot.pot_money += state_pot

    # 해당 함수를 조건부 재귀호출로 사용
    def bet_in_again(self, order1, order2, state, min_amount_val, n = 2):
        """ Raise, Bet이 있는 경우 다시 베팅 진행 """
        # Raise 또는 Bet을 플레이(선택)하는 플레이어의 인덱스 저장 변수
        bet_again = None
        # 게임 state에 걸린 pot
        state_pot = 0
        # 베팅 라운드 횟수를 기록하기 위한 str
        bet_num = "bet" + str(n)
        # 베팅 라운드가 증가하였으므로 bet_num을 키(key)로 하여 dict 생성
        self.players_bet_log.add_state_log_again(nround = self.num_round, game_state = state, str_bet_n = bet_num)
        
        # 베팅 프로세스
        def bet_again_process(idx, action, min):
            bet_action_val = self.players[idx].action_bet(game_state = state, std_bet_action = action, min_amount = min, again = True)
            bet_amount_val = self.players[idx].bet_again(game_state = state, min_amount = min)
            if bet_action_val != None:
                self.players_bet_log.add_bet_log(nround = self.num_round, game_state = state, player_name = self.players[idx].name, \
                                                bet = bet_action_val, bet_amount = bet_amount_val, bet_n = n - 1, str_bet_n = bet_num)
        
            if bet_action_val == "Raise" or bet_action_val == "Bet":
                if min < bet_amount_val:
                    min = bet_amount_val
                bet_again = i
            else:
                bet_again = None
            
            return min, bet_again

        # Raise 또는 Bet을 플레이(선택)한 플레이어가 있는 위치에 따라 베팅 순서가 분기됨
        if order1 < order2 :
            for i in range(order1, order2):
                min_amount_val, bet_again = bet_again_process(idx = i, action = "Bet", min = min_amount_val)
                    
        elif order1 > order2:
            for i in range(order1, self.current_num_player):
                min_amount_val, bet_again = bet_again_process(idx = i, action = "Bet", min = min_amount_val)

            for i in range(0, order2):
                min_amount_val, bet_again = bet_again_process(idx = i, action = "Bet", min = min_amount_val)

        # bet_again 변수에 int값이 저장되었을 경우 재귀호출
        if bet_again != None:
            self.bet_in_again(order1 = order2, order2 = bet_again, state = state, min_amount_val = min_amount_val, n = n + 1)
        else:
            self.players_bet_log.add_state_result_log(nround = self.num_round, game_state = state)
            
            for i in range(self.current_num_player):
                self.players_bet_log.add_bet_log(nround = self.num_round, game_state = state, player_name = self.players[i].name, \
                                                bet = self.players[i].bet_status, bet_amount = self.players[i].get_bet_amount(game_state = state), \
                                                bet_n = n, str_bet_n = "result")
                state_pot += self.players[i].get_bet_amount(game_state = state)
            self.pot.pot_money += state_pot

class Pot:
    def __init__(self):
        self.__pot_money = 0
    
    @property
    def pot_money(self):
        return self.__pot_money
    
    @pot_money.setter
    def pot_money(self, val):
        self.__pot_money = val

class BetLog:
    """ Player 베팅 기록 클래스 """
    def __init__(self):
        self.__bet_log = []

    def init_round_log(self):
        """ 새 라운드마다 호출되는 함수 """
        self.__bet_log.append({"blind" : [{ "bet1" : {} }] })

    def add_state_log(self, nround, game_state, bet_n = "bet1"):
        """ 각 게임 단계를 key로 하는 list안의 dict 생성 """
        self.__bet_log[nround][game_state] = [{ bet_n : {} }]

    def add_bet_log(self, nround, game_state, player_name, bet, bet_amount, bet_n = 0, str_bet_n = "bet1"):
        """ 각 플레이어의 이름을 key로 하는 dict 생성 """
        self.__bet_log[nround][game_state][bet_n][str_bet_n][player_name] = \
        { 
            "state" : game_state,
            "bet" : bet, 
            "bet_amount" : bet_amount
        }
    
    def add_state_log_again(self, nround, game_state, str_bet_n):
        """ 각 게임 단계의 2차 3차 베팅이 진행되었을 경우 list안에 dict 추가 """
        self.__bet_log[nround][game_state].append({ str_bet_n : {} })
        
    def add_state_result_log(self, nround, game_state):
        self.__bet_log[nround][game_state].append({ "result" : {} })
    
    @property
    def bet_log(self):
        return self.__bet_log
    