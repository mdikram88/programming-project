from turtle import Turtle
import random
COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 5
RANDOM_LIST_CHANCE = [1]


class CarManager:
    def __init__(self):
        self.num = 1
        self.random_chance_list = RANDOM_LIST_CHANCE
        self.car_speed = STARTING_MOVE_DISTANCE
        self.all_cars = []

    def create_car(self):
        chance = random.randint(1, max(RANDOM_LIST_CHANCE) + 5)
        if chance in RANDOM_LIST_CHANCE:
            new_car = Turtle("square")
            new_car.shapesize(stretch_len=2, stretch_wid=1)
            new_car.penup()
            new_car.color(random.choice(COLORS))
            random_y = random.randint(-230, 230)
            new_car.goto(300, random_y)
            self.all_cars.append(new_car)

    def move_car(self):
        for car in self.all_cars:
            car.backward(self.car_speed)

    def increase_speed(self):

        self.car_speed += MOVE_INCREMENT
        self.num += 1
        self.random_chance_list.append(self.num)
