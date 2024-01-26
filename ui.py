from tkinter import *
from tkinter import messagebox
from quiz_brain import QuizBrain
from PIL import Image, ImageTk

THEME_COLOR = "#375362"

class QuizInterface:    #(QuizBrain):
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, background=THEME_COLOR)

        self.score_label = Label(text=f"Score: 0/1", bg=THEME_COLOR, fg="white")
        self.score_label.grid(column=5, row=0)

        right_image = PhotoImage(file="images/true.png")
        self.right_button = Button(image=right_image, bg=THEME_COLOR,
                                   highlightthickness=0, pady=50, command=self.true_pressed)
        self.right_button.grid(column=0, row=2, columnspan=2, sticky="w")

        wrong_image = PhotoImage(file="images/false.png")
        self.wrong_button = Button(image=wrong_image, bg=THEME_COLOR,
                                   highlightthickness=0, pady=50, command=self.false_pressed)
        self.wrong_button.grid(column=4, row=2, columnspan=2, sticky="e")

        self.canvas = Canvas(width=300, height=250, bg="white")
        self.question_text = self.canvas.create_text(
            150,
            125,
            width=280,
            text="Some question text",
            font=("Arial", 20, "italic"),
            fill=THEME_COLOR
        )
        self.canvas.grid(column=0, row=1, columnspan=6, pady=20)

        pause_image = Image.open("images/Pause-removebg-preview.png")
        play_image = Image.open("images/Play-removebg-preview.png")
        stop_image = Image.open("images/Stop-removebg-preview.png")
        reset_image = Image.open("images/reset_button3-removebg-preview.png")
        new_size = (20, 22)
        pause_image_new_size = pause_image.resize(new_size)
        play_image_new_size = play_image.resize(new_size)
        stop_image_new_size = stop_image.resize(new_size)
        reset_image_new_size = reset_image.resize(new_size)
        self.pause = ImageTk.PhotoImage(pause_image_new_size)
        self.play = ImageTk.PhotoImage(play_image_new_size)
        self.stop = ImageTk.PhotoImage(stop_image_new_size)
        self.reset = ImageTk.PhotoImage(reset_image_new_size)

        self.pause_state = True
        self.play_button = Button(image=self.play, bg=THEME_COLOR, command=self.app_pause, highlightthickness=0)
        self.play_state = True
        self.stop_button = Button(image=self.stop, bg=THEME_COLOR, command=self.app_stop, highlightthickness=0)
        self.stop_state = True
        self.reset_button = Button(image=self.reset, bg=THEME_COLOR, command=self.app_reset, highlightthickness=0)
        self.reset_button_response = BooleanVar()

        self.play_button.grid(column=0, row=0, sticky="w")
        self.stop_button.grid(column=0, row=0, sticky="e")
        self.reset_button.grid(column=1, row=0, sticky="e")

        self.get_next_question()

        self.window.mainloop()

    def app_reset(self):
        if self.quiz.still_has_questions():
            self.canvas.config(bg="blue")
            font_size = ("Arial", 20, "italic")
            self.canvas.itemconfig(self.question_text, text="Reset...", font=font_size, fill="white")
            self.play_button.config(image=self.pause, command=self.app_play)
            self.window.after(1000, self.complete_reset)
            self.quiz.reset_questions()
            for widget in self.window.winfo_children()[1:3]:
                widget.config(state="normal")
            self.reset_button_response.set(True)
            self.reset_response()
        else:
            self.reset_button_response.set(False)
            self.reset_response()
            if self.reset_response() == False:
                self.play_button.config(image=self.pause, command=self.app_play)
                self.answer_reset = messagebox.askyesno(title="Reset the game...",
                                                        message="Are you sure you want to reset Quizzler?")
                if self.answer_reset == self.play_state:
                    self.play_button.config(image=self.play, command=self.app_pause)
                    # self.app_reset()
                    self.canvas.config(bg="blue")
                    font_size = ("Arial", 20, "italic")
                    self.canvas.itemconfig(self.question_text, text="Reset...", font=font_size, fill="white")
                    self.window.after(1000, self.get_next_question)
                    self.quiz.reset_questions()
                    for widget in self.window.winfo_children()[1:3]:
                        widget.config(state="normal")
                    self.play_button.config(image=self.play, command=self.app_pause)
                else:
                    self.play_button.config(image=self.play, command=self.app_pause)

    def complete_reset(self):
        self.play_button.config(image=self.play, command=self.app_pause)
        self.get_next_question()

    def reset_response(self):
        reset_boolean = self.reset_button_response.get()
        return reset_boolean

    def app_pause(self):
        if self.quiz.still_has_questions():
            self.play_button.config(image=self.pause, command=self.app_play)
            for widget in self.window.winfo_children()[1:3]:
                widget.config(state="disabled")
        else:
            self.play_button.config(image=self.pause, command=self.app_play)

    def app_stop(self):
        #if self.stop_state:
        if self.quiz.still_has_questions():
            self.play_button.config(image=self.pause, command=self.app_play)
            for widget in self.window.winfo_children()[1:3]:
                widget.config(state="disabled")
            self.answer = messagebox.askyesno("Quizzler", "Do you want to go out to the Quizzler?")
            #print(self.answer)
            if self.answer == self.stop_state:
                self.window.destroy()
            elif self.answer != self.stop_state:
                self.play_button.config(image=self.play, command=self.app_pause)
                for widget in self.window.winfo_children()[1:3]:
                    widget.config(state="normal")
        elif not self.quiz.still_has_questions():
            self.play_button.config(image=self.pause, command=self.app_play)
            self.answer = messagebox.askyesno("Quizzler", "Do you want to go out to the Quizzler?")
            if self.answer != self.stop_state:
                self.play_button.config(image=self.play, command=self.app_pause)
                for widget in self.window.winfo_children()[1:3]:
                    widget.config(state="disabled")
            else:
                self.window.destroy()

    def app_play(self):
        #if self.play_state:
        if self.quiz.still_has_questions():
            self.play_button.config(image=self.play, command=self.app_pause)
            for widget in self.window.winfo_children()[1:3]:
                widget.config(state="normal")
        else:
            self.play_button.config(image=self.play, command=self.app_pause)

    def get_next_question(self):
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.score_label.config(text=f"Score: {self.quiz.score}/{self.quiz.question_number}")
            if len(q_text) <= 90:
                font_size=("Arial", 20, "italic")
                self.canvas.itemconfig(self.question_text, text=q_text, font=font_size, fill="black")
            elif len(q_text) > 90:
                font_size=("Arial", 12, "italic")
                self.canvas.itemconfig(self.question_text, text=q_text, font=font_size, fill="black")
            return len(q_text)
        else:
            self.canvas.itemconfig(self.question_text, text="You have reached the end of the quiz. ")
            self.right_button.config(state="disabled")
            self.wrong_button.config(state="disabled")

    def true_pressed(self):
        self.give_feedback(self.quiz.check_answer("True"))

    def false_pressed(self):
        is_right = self.quiz.check_answer("False")
        self.give_feedback(is_right)

    def give_feedback(self, is_right):
        if is_right:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        self.window.after(1000, self.get_next_question)