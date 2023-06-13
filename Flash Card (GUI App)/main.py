from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
TITLE_FONT = ('Arial', 30, "italic")
WORD_FONT = ('Arial', 40, "bold")
current_card = {}

# -------------------------------- PRE-SETUP -------------------------------- #
try:
    data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("./data/french_words.csv")
to_learn = data.to_dict(orient="records")
words_learnt = []

# -----------------------------  RANDOM WORD DISPLAY ------------------------- #


def next_card():

    global current_card
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_view, image=card_front)
    canvas.itemconfig(title, text="French")
    canvas.itemconfig(word, text=current_card["French"])
    window.after(3000, func=flip_card)


def flip_card():

    canvas.itemconfig(card_view, image=card_back)
    canvas.itemconfig(title, text="English")
    canvas.itemconfig(word, text=current_card["English"])


def is_known():

    words_learnt.append(current_card)
    to_learn.remove(current_card)
    new_data = pandas.DataFrame(to_learn)
    new_data.to_csv("./data/words_to_learn.csv", index=False)

    next_card()


# ------------------------------------ UI SETUP ------------------------------ #
window = Tk()
window.config(bg=BACKGROUND_COLOR)
window.config(padx=40, pady=40)
window.title("Flash card")


# Canvas

canvas = Canvas(width=800, height=530, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
card_view = canvas.create_image(400, 265, image=card_front)
canvas.grid(column=0, row=0, columnspan=3)

title = canvas.create_text(400, 130, text="Title", font=TITLE_FONT)
word = canvas.create_text(400, 265, text="Word", font=WORD_FONT)

# Buttons

checkmark_image = PhotoImage(file="./images/right.png")
right_button = Button(image=checkmark_image, highlightthickness=0, command=is_known)
right_button.grid(column=2, row=1)

cross_image = PhotoImage(file="./images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(column=0, row=1)

next_card()



window.mainloop()
