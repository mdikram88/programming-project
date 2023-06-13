from turtle import Turtle


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.move_distance = 5
        self.move_heading = 45
        self.shape("circle")
        self.color("white")
        self.penup()
        self.refresh()

    def move(self):
        self.forward(self.move_distance)

    def refresh(self):
        self.move_heading = self.move_heading + 90
        self.home()
        self.setheading(self.move_heading)

    def wall_bounce(self):
        self.setheading(-self.heading())

    def paddle_bounce(self):
        self.setheading(-self.heading())
        self.move_distance *= -1
