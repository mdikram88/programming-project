import random

cards = ['A', 2, 3, 4, 5 ,6, 7, 8, 9, 10, 'J', 'Q' ,'K']
play = input("Do you want to play a game of Blackjack? Type 'y' or 'n': ").lower()
play_more = 'y'

def get_score(l):
    score = 0
    for ele in l:
        if ele in ['Q','K','J']:
            score += 10
        elif ele == 'A':
            score += 1
        else:
            score += ele
    if ('A' in l) and (score < 12):
        score += 10
    return score

def display(flag):

    if not flag:
        print(f"Your cards: {user_cards}")
        print(f"Computer First card : {computer_card[0]}")
    else:
        print(f"Your final cards: {user_cards}")
        print(f"Computer final card : {computer_card}")

while play == 'y':

    user_cards = [random.choice(cards) for _ in range(2)]
    computer_card = [random.choice(cards) for _ in range(2)]

    display(False)

    more_card = 'y'
    while more_card == 'y':

        more_card = input("Type 'y' to get another card, type 'n' to pass: ").lower()
        if more_card == 'y':
            user_cards.append(random.choice(cards))
            display(False)
            if get_score(user_cards) > 21:
                break

    while get_score(computer_card) < 17:
        computer_card.append(random.choice(cards))

    user_score =get_score(user_cards)
    computer_score = get_score(computer_card)

    display(True)

    print()
    if user_score == computer_score:
        print(f"It's a Draw!, your score: {user_score} and computer score: {computer_score}")
    elif ((user_score > computer_score) and (user_score < 21)) or (user_score == 21):
        print(f"You win!, your score: {user_score} and computer score: {computer_score}")
    else:
        print(f"Computer Win!, your score: {user_score} and computer score: {computer_score}")

    print()
    play = input("Do you want to play again? Type 'y' or 'n' : ").lower()

print("Good Bye!!")