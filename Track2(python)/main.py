from flask import Flask, request, jsonify, render_template
import random
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

# Initialize Flask app
app = Flask(__name__)

# Load pre-trained LSTM model
model = load_model('math_question_generator.h5')

# Math operations for Level 1 (basic arithmetic)
OPERATIONS = ['+', '-', '*', '/']


# Function to generate random questions for each level
def generate_question(level):
    if level == 1:
        # Level 1: Basic arithmetic (fractions, decimals, etc.)
        num1, num2 = random.randint(1, 10), random.randint(1, 10)
        operation = random.choice(OPERATIONS)
        question = f"{num1} {operation} {num2}"
        answer = eval(question)
    elif level == 2:
        # Level 2: Geometry (area and perimeter of simple shapes)
        question = "What is the area of a rectangle with length 5 and width 3?"
        answer = 5 * 3
    elif level == 3:
        # Level 3: Basic algebra
        question = "Solve for x: 2x + 3 = 11"
        answer = (11 - 3) / 2
    elif level == 4:
        # Level 4: Basic calculus
        question = "What is the derivative of 2x^2?"
        answer = "4x"
    else:
        question = "Invalid level"
        answer = None
    return question, answer


# Route to fetch a new question based on the level
@app.route('/get_question', methods=['GET'])
def get_question():
    level = int(request.args.get('level', 1))
    question, answer = generate_question(level)
    return jsonify({'question': question, 'answer': answer})


# Route to check the answer
@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.json
    user_answer = float(data['user_answer'])
    correct_answer = float(data['correct_answer'])

    feedback = "Correct!" if np.isclose(user_answer, correct_answer, atol=0.1) else "Incorrect. Try again!"
    return jsonify({'feedback': feedback})


# Route to display progress report
@app.route('/report', methods=['GET'])
def report():
    report_data = {
        "total_questions": 20,
        "correct_answers": 15,
        "accuracy": "75%"
    }
    return jsonify(report_data)


# Run the app
if __name__ == '__main__':
    app.run(debug=True)