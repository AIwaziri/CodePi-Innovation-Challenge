import tkinter as tk
import random
import numpy as np
from sklearn.tree import DecisionTreeClassifier


# AI Model: Simple decision tree for question type generation
class QuestionGenerator:
    def __init__(self):
        self.model = DecisionTreeClassifier()
        self.train_model()

    def train_model(self):
        # Sample training data (level, problem type)
        # Levels: 0 = Fractions, 1 = Geometry, 2 = Algebra, 3 = Calculus
        # Problem types: 0 = Addition, 1 = Subtraction, 2 = Multiplication, 3 = Division
        # This is a simple representation, you can expand this further
        X_train = np.array([[0, 0], [0, 1], [0, 2], [0, 3],
                            [1, 0], [1, 1], [1, 2], [1, 3],
                            [2, 0], [2, 1], [2, 2], [2, 3],
                            [3, 0], [3, 1], [3, 2], [3, 3]])
        y_train = np.array([0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3])  # Question type

        self.model.fit(X_train, y_train)

    def generate_question(self, level):
        # Level here is from 0 to 3 (Fractions, Geometry, Algebra, Calculus)
        problem_type = self.model.predict([[level, random.randint(0, 3)]])[0]
        return self.create_question(level, problem_type)

    def create_question(self, level, problem_type):
        # Define the questions based on level and problem type
        if level == 0:  # Fractions
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            question = f"Solve: {num1}/{num2}"
            answer = round(num1 / num2, 2)
        elif level == 1:  # Geometry
            if problem_type == 0:  # Addition
                length = random.randint(1, 10)
                width = random.randint(1, 10)
                question = f"Find the area of a rectangle with length {length} and width {width}"
                answer = length * width
            elif problem_type == 1:  # Subtraction
                # Additional question types...
                pass
        elif level == 2:  # Algebra
            x = random.randint(1, 10)
            question = f"Solve for x: x + 5 = {x + 5}"
            answer = x
        elif level == 3:  # Calculus
            coefficient = random.randint(1, 5)
            question = f"Differentiate y = {coefficient}x^2"
            answer = f"{2 * coefficient}x"

        return {"text": question, "answer": str(answer)}


# Game class with AI enhancements
class MathQuest:
    def __init__(self, root):
        self.root = root
        self.root.title("MathQuest: An Interactive Adventure in Math")

        self.current_level = 0
        self.score = 0
        self.question_count = 0
        self.questions_per_level = 5
        self.current_question = {}

        self.start_game_button = tk.Button(root, text="Start Game", command=self.start_game)
        self.start_game_button.pack(pady=10)

        self.question_label = tk.Label(root, text="", font=("Arial", 16))
        self.question_label.pack(pady=20)

        self.answer_entry = tk.Entry(root, font=("Arial", 14))
        self.answer_entry.pack(pady=10)

        self.submit_button = tk.Button(root, text="Submit Answer", command=self.submit_answer)
        self.submit_button.pack(pady=10)

        self.hint_button = tk.Button(root, text="Show Hint", command=self.show_hint)
        self.hint_button.pack(pady=10)

        self.hint_label = tk.Label(root, text="", font=("Arial", 12), fg="blue")
        self.hint_label.pack(pady=10)

        self.progress_label = tk.Label(root, text="", font=("Arial", 12))
        self.progress_label.pack(pady=10)

        self.feedback_label = tk.Label(root, text="", font=("Arial", 12))
        self.feedback_label.pack(pady=10)

        # Initialize Question Generator (AI model)
        self.qg = QuestionGenerator()

    def start_game(self):
        self.current_level = 0
        self.score = 0
        self.question_count = 0
        self.update_progress()
        self.generate_question()
        self.start_game_button.pack_forget()
        self.show_ui()

    def show_ui(self):
        self.answer_entry.config(state="normal")
        self.submit_button.config(state="normal")
        self.hint_button.config(state="normal")

    def hide_ui(self):
        self.answer_entry.config(state="disabled")
        self.submit_button.config(state="disabled")
        self.hint_button.config(state="disabled")

    def generate_question(self):
        if self.question_count < self.questions_per_level:
            self.current_question = self.qg.generate_question(self.current_level)
            self.question_label.config(text=self.current_question['text'])
            self.hint_label.config(text="")
        else:
            self.current_level += 1
            self.question_count = 0
            if self.current_level < 4:
                self.generate_question()
            else:
                self.end_game()

    def submit_answer(self):
        user_answer = self.answer_entry.get().strip()
        if user_answer == self.current_question["answer"]:
            self.score += 10
            self.question_count += 1
            self.update_progress()
            self.generate_question()
            self.feedback_label.config(text="Correct! Great job!", fg="green")
        else:
            self.feedback_label.config(text="Incorrect. Try again!", fg="red")

    def show_hint(self):
        self.hint_label.config(text="AI Hint: Approach the problem step by step.")

    def update_progress(self):
        self.progress_label.config(
            text=f"Level: {self.current_level + 1} | Question: {self.question_count}/{self.questions_per_level} | Score: {self.score}")

    def end_game(self):
        self.question_label.config(text="Congratulations! You've completed the game.")
        self.hide_ui()
        restart_button = tk.Button(self.root, text="Start Over", command=self.start_game)
        restart_button.pack(pady=10)
        quit_button = tk.Button(self.root, text="Quit", command=self.root.quit)
        quit_button.pack(pady=10)


# Running the game
if __name__ == "__main__":
    root = tk.Tk()
    game = MathQuest(root)
    root.mainloop()