import random
from additionals import *
num = random.randint(1,100)

print(logo)
print("Welcome to the Number Guessing Game!")
print("I am Thinking of a natural number between 1 to 100 ")
level = input("Choose your difficulty level. Type 'easy' or 'medium' or 'hard': ").lower()


if level == 'easy':
    attempts = 10
elif level == 'medium':
    attempts = 8
elif level == 'hard':
    attempts = 5
else:
    print("Invalid option")
    print("Program exited")

play = 'yes'
while play == 'yes':

    print(f"You have {attempts} attempts remaining to guess the number.")
    guess = int(input("Make a guess: "))
    if guess == num:
        print()
        print("Bingo!You guessed Correctly.")
        play = 'no'
    elif guess > num:
        attempts -= 1
        print("Too High")
    else:
        attempts -= 1
        print("Too Low")

    if attempts > 0:
        print("Guess Again")
    else:
        print()
        print("You Lost")
        print(f"You ran out of guesses, Correct number is {num}")
        play = 'no'

