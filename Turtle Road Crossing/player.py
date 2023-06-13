from turtle import Turtle
STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280


class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.color("green")
        self.setheading(90)
        self.penup()
        self.goto(STARTING_POSITION)

    def move_up(self):
        if self.ycor() < 280:
            self.forward(MOVE_DISTANCE)

    def is_at_finish_line(self):
        if self.ycor() > 270:
            return True
        return False

    def go_to_start(self):
        self.goto(STARTING_POSITION)