import random
from hangman import *
#Pre-Setup of the game

lives = 6
word = random.choice(word_list)
#print(word)
length = len(word)
display = []


for i in range(length):
    display += "_"

print(logo)
print(stages[lives])

while True:

    if lives == 0:
        print(f"Opps! You ran out of lives, Correct Word is '{word}'")
        break

    if "_" not in display:
        print(f"Congratulations, You correctly guessed the word '{word}'")
        break

    print(" ".join(display))

    print(f"Current lives {lives}")
    guess = input("Guess a letter of the word : \n").lower()

    if guess in display:
        print(f"You have already guessed '{guess}', try another letter")
        continue

    flag = False
    for pos in range(length):
        if word[pos] == guess:
            display[pos] = guess
            flag = True

    if flag:
        print("You guessed Correctly!")
    else:
        print("Opps! incorrect letter")
        lives -= 1

    print(stages[lives])

print("GAME OVER")
