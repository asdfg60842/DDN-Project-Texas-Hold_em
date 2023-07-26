betting_history = [['blind', 'blind', 5], ['preflop', 'Raise', 10]]
game_state = "preflop"
min_amount = 20
for state, _, amount in betting_history:
    print("단계 : {}, 돈 : {}".format(state, amount))
    if state == "blind" and game_state == "preflop":
        diff = min_amount - amount
        print("{} {}여기서 돈이 빠져야 될거 아니야 씨벌 그럼 diff가 얼마야 {}".format(state, amount, diff))
    elif state == game_state:
        diff -= min_amount - amount
        print("{} {} 여기서 돈이 빠져야 될거 아니야 씨벌 그럼 diff가 얼마야 {}".format(state, amount, diff))
        
print(diff)
                    