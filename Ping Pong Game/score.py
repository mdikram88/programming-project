from turtle import Turtle
FONT = "Arial", 30, "bold"


class Score(Turtle):
    def __init__(self, posi):
        super().__init__()
        self.score = -1
        self.hideturtle()
        self.color("white")
        self.pensize(3)
        self.score_position = posi
        self.update_score()

    def update_score(self):
        self.clear()
        self.penup()
        self.goto(0, -300)
        self.pendown()
        self.goto(0, 300)
        self.penup()
        self.goto(self.score_position)
        self.score += 1
        self.write(f"{self.score}", align='center', font=FONT)
