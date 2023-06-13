from turtle import Turtle, Screen
import random

COLOR_SET = ["red", "orange", "blue", "yellow", "green"]
START_Y = -80
ALIGNMENT = 'center'
FONT = ('Arial', 12, 'normal')
win = False

line = Turtle()
line.hideturtle()


def finish_line():
    line.penup()
    line.goto(220, -250)
    line.setheading(90)
    line.pendown()
    line.forward(500)
    line.penup()

screen = Screen()
screen.setup(width=500, height=400)
screen.title("Turtle Racing Game")
user_guess = screen.textinput(title="Choose color", prompt="Who will win (red, orange, blue, yellow, green)").lower()
finish_line()

players = [Turtle(shape="turtle") for i in range(5)]
for i in range(5):
    players[i].penup()
    players[i].color(COLOR_SET[i])
    players[i].goto(-220, START_Y + i * 40)


while not win:
    player = random.choice(players)
    player.forward(3)
    if player.xcor() > 220:
        win = True
        winner = player.pencolor()


line.home()
if user_guess == winner.lower():
    line.write("You Won!!", align=ALIGNMENT, font=FONT)
else:
    line.write(f"You Lost!, Player: {winner} wins!", align=ALIGNMENT, font=FONT)

screen.exitonclick()