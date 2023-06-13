from time import sleep
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import ScoreBoard

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

p1 = Player()
car_manager = CarManager()
scoreboard = ScoreBoard()
game_is_on = True


def controller():
    screen.listen()
    screen.onkey(key="Up", fun=p1.move_up)


while game_is_on:
    sleep(0.1)
    screen.update()
    controller()
    car_manager.create_car()
    car_manager.move_car()

    # Detect Collision with car
    for car in car_manager.all_cars:
        if car.distance(p1) < 20:
            scoreboard.game_over()
            game_is_on = False

    # Detect if turtle crossed the finishing line
    if p1.is_at_finish_line():
        p1.go_to_start()
        scoreboard.increase_level()
        car_manager.increase_speed()


screen.exitonclick()