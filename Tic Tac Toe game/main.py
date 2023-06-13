from extras import LOGO, Board
from random import randint
from time import sleep

over = True
player1 = True


def display_board():

    """For Displaying the Tic Tac Toe Board"""

    for row in Board:
        print(" | ".join(row))


def is_winner():

    """To check if there is a winner at the current stage of game"""

    # Left Diagonal
    if Board[0][0] == Board[1][1]:
        if Board[1][1] == Board[2][2]:
            if Board[0][0] == "X":
                return "p1"
            elif Board[0][0] == "O":
                return "p2"

    # Top Horizontal line
    if Board[0][0] == Board[0][1]:
        if Board[0][1] == Board[0][2]:
            if Board[0][0] == "X":
                return "p1"
            elif Board[0][0] == "O":
                return "p2"

    # Left Vertical Line
    if Board[0][0] == Board[1][0]:
        if Board[1][0] == Board[2][0]:
            if Board[0][0] == "X":
                return "p1"
            elif Board[0][0] == "O":
                return "p2"

    # 2nd Vertical line
    if Board[1][1] == Board[0][1]:
        if Board[1][1] == Board[2][1]:
            if Board[1][1] == "X":
                return "p1"
            elif Board[0][0] == "O":
                return "p2"

    # 2nd Horizontal Line
    if Board[1][1] == Board[1][0]:
        if Board[1][1] == Board[1][2]:
            if Board[1][1] == "X":
                return "p1"
            elif Board[0][0] == "O":
                return "p2"

    # Right Diagonal
    if Board[1][1] == Board[2][0]:
        if Board[1][1] == Board[0][2]:
            if Board[1][1] == "X":
                return "p1"
            elif Board[0][0] == "O":
                return "p2"

    # 3rd Vertical Line
    if Board[0][2] == Board[1][2]:
        if Board[0][2] == Board[2][2]:
            if Board[0][2] == "X":
                return "p1"
            elif Board[0][0] == "O":
                return "p2"

    # 3rd Horizontal Line
    if Board[2][0] == Board[2][1]:
        if Board[2][0] == Board[2][2]:
            if Board[2][0] == "X":
                return "p1"
            elif Board[0][0] == "O":
                return "p2"


def is_draw():
    """To check if Game is finished with a draw"""
    c = 0
    for row in Board:
        if "_" not in row:
            c += 1
    if c == 3:
        return True
    return False


def is_empty(a, b):
    """To check if a position in board Empty"""
    return Board[a][b] == "_"


def is_over():
    """To check if game is over either because of winner or draw"""

    winner = is_winner()
    if winner:
        if winner == "p1":
            print("Player 1 Won the Game")
        else:
            print("Player 2 Won the Game")
        return True

    if is_draw():
        print("It's a Draw!")
        return True
    return False


def get_move():
    """To get the next move for computer player"""
    return randint(0, 2), randint(0, 2)


# Setting up the Display
print(LOGO)
print("Welcome to the Game!")


display_board()
print()
print("Tip: to select a box, give command like '1,1', "
      "\nwhich means first box of the first row will be selected.")

print()
game_type = input("Press '1' for One player\nPress '2' for two players : ")

if game_type not in ["1", "2"]:
    print("Invalid Input")

if game_type in ["1", "2"]:
    print("Player 1 has 'X' and Player 2 has 'O'")
    start = input("Start Game? 'Y' / 'N': ").lower()
    print()

    if start == "y":
        over = False
    elif start != "n":
        print("Invalid Input")

# Starting game is all input are valid

while not over:

    display_board()
    if is_over():
        over = True
        print("Game is Over!")
        break

    correct = False

    if player1:
        while not correct:
            try:
                x, y = input("Player 1: ").split(",")
                x, y = int(x), int(y)
                if is_empty(x-1, y-1):
                    Board[x - 1][y - 1] = "X"
                    player1 = not player1
                    correct = True
                else:
                    print("Already Taken! Try again..")
            except ValueError:
                print("Invalid key, Accepted Command format '1, 1' or '1,1'")
            except IndexError:
                print("Choose accept number range is 1 to 3 ")

    else:
        # If player is playing with Computer
        if game_type == "1":

            x, y = get_move()
            while not is_empty(x, y):
                x, y = get_move()

            print(f"Player 2: {x}, {y}")
            Board[x][y] = "O"
            player1 = not player1
            sleep(1)
        # If Game is 2 Human Players
        else:
            while not correct:
                try:
                    x, y = input("Player 2: ").split(",")
                    x, y = int(x), int(y)
                    if is_empty(x-1, y-1):
                        Board[x - 1][y - 1] = "O"
                        player1 = not player1
                        correct = True
                    else:
                        print("Already Taken! Try again..")
                except ValueError:
                    print("Invalid key, Accepted Command format '1, 1' or '1,1'")
                except IndexError:
                    print("Choose number range is 1 to 3 Only")
