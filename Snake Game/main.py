from turtle import Screen
from food import Food
from snake import Snake
from scoreboard import ScoreBoard
from time import sleep
time_speed = 0.5

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.tracer(0)
screen.title("My Snake Game")

snake = Snake()
food = Food()
score = ScoreBoard()
prev_score = score.score
screen.update()


def snake_control():
    screen.onkey(key="Up", fun=snake.turn_up)
    screen.onkey(key="Left", fun=snake.turn_left)
    screen.onkey(key="Right", fun=snake.turn_right)
    screen.onkey(key="Down", fun=snake.turn_down)


play = True
while play:
    sleep(0.1)
    screen.listen()
    snake_control()
    screen.update()
    snake.move()

    # increasing speed as per score
    if (score.score % 5 == 0) and (score.score != prev_score):
        time_speed /= 1.5
        prev_score = score.score

    # detect Collision with food
    if snake.head.distance(food) < 15:
        snake.grow()
        score.update()
        food.refresh()


    # detect Collision with wall or body
    if snake.is_hit():
        score.reset()
        snake.reset()

screen.exitonclick()
