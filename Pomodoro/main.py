from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
BUTTON_FONT = (FONT_NAME, 12, 'normal')
CHECK_MARK = "✔"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = ''

# ---------------------------- TIMER RESET ------------------------------- # 

def reset():
    window.after_cancel(timer)
    title_label.config(text="Timer")
    canvas.itemconfig(timer_text, text="00:00")
    global reps
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():

    global reps
    reps += 1
    if reps in [1, 3, 5, 7]:
        secs = WORK_MIN*60
        title_label.config(text="Work")
    elif reps in [2, 4, 6]:
        secs = SHORT_BREAK_MIN*60
        title_label.config(text="Break", fg=PINK)
    elif reps == 8:
        secs = LONG_BREAK_MIN*60
        title_label.config(text="Break", fg=RED)

    count_down(math.ceil(secs))


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):

    global timer
    mins = count // 60
    secs = count % 60

    if secs == 0:
        secs = "00"
    elif secs < 10:
        secs = f"0{secs}"
    if mins < 10:
        mins = f"0{mins}"

    canvas.itemconfig(timer_text, text=f"{mins}:{secs}")
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    elif count == 0:
        start_timer()
    if reps % 2 == 0:
        check_mark.config(text=CHECK_MARK*(reps//2))


# ---------------------------- UI SETUP ------------------------------- #
# Setting up Window Screen
window = Tk()
window.config(padx=100, pady=50, bg=YELLOW)
window.title("Pomodoro")

# Making Canvas
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)


# Label
title_label = Label(text="Timer", font=(FONT_NAME, 35, "bold"), fg=GREEN, bg=YELLOW)
title_label.grid(column=1, row=0)

check_mark = Label(fg=GREEN, bg=YELLOW, font=('Arial', 18, 'normal'))
check_mark.config(pady=15)
check_mark.grid(column=1, row=3)

# Buttons
start_button = Button(text="Start", font=BUTTON_FONT, command=start_timer)
reset_button = Button(text="Reset", font=BUTTON_FONT, command=reset)
start_button.grid(column=0, row=3)
reset_button.grid(column=2, row=3)


window.mainloop()
