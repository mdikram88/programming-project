from tkinter import *
from quiz_brain import QuizBrain
THEME_COLOR = "#375362"
RED = "#f88"
GREEN = "#58ff58"
FONT = "Arial", 20, "italic"
SCORE_FONT = "Arial", 15, "normal"


class QuitInterface:

    def __init__(self, quiz_brain: QuizBrain):

        self.quiz = quiz_brain
        # window
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        # Canvas
        self.canvas = Canvas(width=300, height=250)
        self.canvas.grid(column=0, row=1, columnspan=2, pady=50)

        self.question_text = self.canvas.create_text(150, 125,
                                                     width=280,
                                                     text="Question",
                                                     fill=THEME_COLOR,
                                                     font=FONT)

        # label
        self.score_label = Label(text=f"Score: 0", fg="white", bg=THEME_COLOR, font=SCORE_FONT)
        self.score_label.grid(column=1, row=0, sticky="e")

        # Buttons
        true_img = PhotoImage(file="./images/true.png")
        false_img = PhotoImage(file="./images/false.png")
        self.true_button = Button(image=true_img, highlightthickness=0, command=self.true_pressed)
        self.false_button = Button(image=false_img, highlightthickness=0, command=self.false_pressed)
        self.true_button.grid(column=0, row=2)
        self.false_button.grid(column=1, row=2)

        self.get_next_question()
        self.window.mainloop()

    def get_next_question(self):
        self.canvas.config(bg="white")

        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.canvas.itemconfig(self.question_text, text="The Quiz is Complete")
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")

    def true_pressed(self):
        status = self.quiz.check_answer('True')
        self.display(status)

    def false_pressed(self):
        status = self.quiz.check_answer('False')
        self.display(status)

    def display(self, status):
        if status:
            self.canvas.config(bg=GREEN)
        else:
            self.canvas.config(bg=RED)
        self.score_label.config(text=f"Score: { self.quiz.score}")
        self.window.after(1000, self.get_next_question)
