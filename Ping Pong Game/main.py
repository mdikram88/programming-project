from turtle import Turtle, Screen
from paddle import Paddle
from ball import Ball
from time import sleep
from score import Score


screen = Screen()
screen.tracer(0)
screen.title("Ping Pong Game")
screen.bgcolor("black")
screen.setup(height=600, width=800)

l_paddle = Paddle((-370, 0))
r_paddle = Paddle((360, 0))
ball = Ball()
l_score = Score((-30, 250))
r_score = Score((30, 250))

def paddle_controllers():
    screen.onkey(key="w", fun=l_paddle.move_up)
    screen.onkey(key="s", fun=l_paddle.move_down)
    screen.onkey(key="Up", fun=r_paddle.move_up)
    screen.onkey(key="Down", fun=r_paddle.move_down)

play = True

while play:

    screen.update()
    sleep(0.02)
    screen.listen()
    paddle_controllers()
    ball.move()

    if abs(ball.ycor()) >= 280:
        ball.wall_bounce()
    elif abs(r_paddle.xcor() - ball.xcor()) < 10 and abs(r_paddle.ycor() - ball.ycor()) < 40:
        ball.paddle_bounce()
    elif abs(l_paddle.xcor() - ball.xcor()) < 10 and abs(l_paddle.ycor() - ball.ycor()) < 40:
        ball.paddle_bounce()

    if ball.xcor() > 410:
        ball.refresh()
        l_score.update_score()

    elif ball.xcor() < -410:
        ball.refresh()
        r_score.update_score()





screen.exitonclick()
