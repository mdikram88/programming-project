from turtle import Turtle
FONT = ("Courier", 24, "normal")
ALIGNMENT = 'left'


class ScoreBoard:
    def __init__(self):
        self.score = 1
        self.level = Turtle()
        self.border = Turtle()
        self.border.pensize(2)
        self.create_border()

    def create_border(self):
        self.border.penup()
        self.border.goto(-310, 255)
        self.border.pendown()
        self.border.goto(310, 255)
        self.border.penup()
        self.border.goto(-310, -255)
        self.border.pendown()
        self.border.goto(310, -255)
        self.draw_level()

    def draw_level(self):
        self.level.clear()
        self.level.penup()
        self.level.hideturtle()
        self.level.goto(-280, 255)
        self.level.write(f"Level: {self.score}", align=ALIGNMENT, font=FONT)

    def increase_level(self):
        self.score += 1
        self.draw_level()

    def game_over(self):
        self.level.home()
        self.level.write("GAME OVER", align='center', font=('Arial', 20, 'bold'))