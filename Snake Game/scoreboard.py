from turtle import Turtle
from time import sleep
ALIGNMENT = "center"
FONT1 = "Arial", 15, "bold"
FONT2 = "Arial", 12, "normal"

class ScoreBoard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        with open("score.txt", "r") as f:
            self.highest_score = int(f.read())
        self.penup()
        self.hideturtle()
        self.color("white")
        self.display()

    def update(self):
        self.score += 1
        self.display()

    def display(self):
        self.clear()
        self.goto(0, 270)
        self.write(f"Score: {self.score}", align=ALIGNMENT, font=FONT1)
        self.goto(0, 255)
        self.write(f"Highest Score: {self.highest_score}", align=ALIGNMENT, font=FONT2)

    def reset(self):
        if self.highest_score < self.score:
            self.highest_score = self.score
        with open("score.txt", "w") as f:
            f.write(f"{self.highest_score}")
        self.score = 0
        self.home()
        self.write("GAME OVER", align=ALIGNMENT, font=FONT1)
        sleep(2)
        self.display()

