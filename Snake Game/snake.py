from turtle import Turtle
import random
MOVE_DISTANCE = 20
ALIGNMENT = "center"
FONT = "Arial", 18, "bold"


class Snake:
    def __init__(self):
        self.snake = []
        self.create_snake()
        self.head = self.snake[0]
        self.food = Turtle()
        self.food.penup()
        self.food.color("red")
        self.food.hideturtle()

    def create_snake(self):

        for i in range(3):
            block = Turtle("square")
            block.color("white")
            block.speed("fastest")
            block.penup()
            dis = -i * 20
            block.goto(dis, 0)
            self.snake.append(block)

    def move(self):
        for snake_block in range(len(self.snake) - 1, 0, -1):
            x = self.snake[snake_block - 1].xcor()
            y = self.snake[snake_block - 1].ycor()
            self.snake[snake_block].goto(x, y)
        self.snake[0].forward(MOVE_DISTANCE)

    def turn_up(self):
        if self.snake[0].heading() != 270:
            self.snake[0].setheading(90)

    def turn_left(self):
        if self.snake[0].heading() != 0:
            self.snake[0].setheading(180)

    def turn_right(self):
        if self.snake[0].heading() != 180:
            self.snake[0].setheading(0)

    def turn_down(self):
        if self.snake[0].heading() != 90:
            self.snake[0].setheading(270)

    def is_hit(self):
        if abs(self.snake[0].xcor()) >= 300 or abs(self.snake[0].ycor()) >= 300:
            return True
        for block in self.snake[1:]:
            if self.head.distance(block.pos()) < 10:
                return True
        return False

    def grow(self):
        block = Turtle("square")
        block.color("white")
        block.speed("fastest")
        block.penup()
        block.goto(self.snake[-1].pos())
        self.snake.append(block)

    def reset(self):
        for block in self.snake:
            block.goto(-1000, -1000)
        self.snake.clear()
        self.create_snake()
        self.head = self.snake[0]