class QuizBrain:
    def __init__(self, q_list):
        self.question_no = 0
        self.question_list = q_list
        self.score = 0

    def still_has_question(self):
        return self.question_no < len(self.question_list)

    def next_question(self):
        current_question = self.question_list[self.question_no]
        self.question_no += 1
        user_answer = input(f"Q.{self.question_no}: {current_question.text}. (True/False)?:")
        self.check_answer(user_answer, current_question.answer)

    def check_answer(self,answer, c_answer):
        if answer.lower() == c_answer.lower():
            self.score += 1
            print("You got it right")
        else:
            print("You got it wrong")
        print(f"The Correct answer was {c_answer}")
        print(f"You current score is {self.score}/{self.question_no}")
        print()
