from additionals import *
import random

def check_ans(x, y):
    if x['follower_count'] > y['follower_count']:
        return 'a'
    return 'b'

def display(opt1,opt2):
    print(f"Compare A: {a['name']}, {a['description']}, from {a['country']}")
    print(vs)
    print(f"Against B: {b['name']}, {b['description']}, from {b['country']}")
    return input("Who has more followers, Type 'A' or 'B' : ").lower()

#Pre-setup
print(logo)
score = 0
play = 'yes'
b = random.choice(data)
while play == 'yes':
    a = b
    b = random.choice(data)
    ans = display(a,b)
    if check_ans(a,b) == ans:
        score += 1
        print(f"You are right, Your Current Score : {score}")
    else:
        print(f"Sorry, You loss, Final Score : {score}")
        play = 'no'