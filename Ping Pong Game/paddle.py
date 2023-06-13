from turtle import Turtle


class Paddle(Turtle):
    def __init__(self, position):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=1, stretch_len=3.5)
        self.setheading(90)
        self.penup()
        self.goto(position)

    def move_up(self):
        if self.ycor() <= 260:
            self.forward(20)

    def move_down(self):
        if self.ycor() >= -260:
            self.backward(20)
