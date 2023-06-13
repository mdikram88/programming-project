from turtle import Turtle, Screen

tim = Turtle()
screen = Screen()
screen.listen()


def move_forward():
    tim.forward(10)


def move_backward():
    tim.backward(10)


def move_right():
    tim.setheading(tim.heading() - 10)


def move_left():
    tim.setheading(tim.heading() + 10)


def clear():
    tim.clear()
    tim.penup()
    tim.home()
    tim.pendown()


screen.onkey(key="Up", fun=move_forward)
screen.onkey(key="Down", fun=move_backward)
screen.onkey(key="Right", fun=move_right)
screen.onkey(key="Left", fun=move_left)
screen.onkey(key="c", fun=clear)

screen.exitonclick()