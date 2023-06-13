import turtle
import pandas

data = pandas.read_csv("50_states.csv")
state_list = data["state"].to_list()
state_x = data["x"].to_list()
state_y = data["y"].to_list()


screen = turtle.Screen()
screen.title("US State Game")
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)

name = turtle.Turtle()
name.hideturtle()
name.penup()

# To co-ordinates on screen
# def get_on_click(x,y):
#     print(x,y)
# turtle.onscreenclick(get_on_click)

no_of_correct_states = 0
ans_state_list = []

while no_of_correct_states < 50:

    ans_state = screen.textinput(title=f"{no_of_correct_states}/50 States", prompt="What's another state name?").title()
    if ans_state == "Exit":
        missed_state = list(set(state_list) - set(ans_state_list))
        missed_state_dict = {"Missed State": missed_state}
        missed_state_data = pandas.DataFrame(missed_state_dict)
        missed_state_data.to_csv("states_to_learn.csv")
        break

    if ans_state in state_list and ans_state not in ans_state_list:
        ans_state_list.append(ans_state)
        index = state_list.index(ans_state)
        name.goto(state_x[index], state_y[index])
        name.write(ans_state, align='center', font=('Arial', 8, 'bold'))
        no_of_correct_states += 1


