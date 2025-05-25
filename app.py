from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
import random
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to something secure
app.permanent_session_lifetime = timedelta(minutes=30)
CORS(app)

# Hardcoded users
users = {
    "user1": "password1",
    "user2": "password2"
}

# Questions organized by subject
questions_db = {
    "html": [
        {"id": 1, "question": "What does HTML stand for?", "options": ["Hyper Text Markup Language", "Hot Mail", "How to Make Lasagna", "Hyperlinks and Text Markup Language"], "answer": "Hyper Text Markup Language"},
        {"id": 2, "question": "Which tag is used for inserting a line break?", "options": ["<break>", "<br>", "<lb>", "<newline>"], "answer": "<br>"},
        {"id": 3, "question": "What tag is used to define an unordered list?", "options": ["<ul>", "<ol>", "<li>", "<list>"], "answer": "<ul>"},
        {"id": 4, "question": "Which attribute is used to provide an alternative text for an image?", "options": ["alt", "src", "title", "href"], "answer": "alt"},
        {"id": 5, "question": "The <head> section of HTML contains?", "options": ["Page content", "Meta information", "Images", "Links"], "answer": "Meta information"},
    ],
    "css": [
        {"id": 6, "question": "Which CSS property controls text color?", "options": ["color", "font-color", "text-color", "fgcolor"], "answer": "color"},
        {"id": 7, "question": "How do you select an element with id 'header'?", "options": ["#header", ".header", "*header", "header"], "answer": "#header"},
        {"id": 8, "question": "Which property is used to change the background color?", "options": ["background-color", "bgcolor", "color-background", "bg-color"], "answer": "background-color"},
        {"id": 9, "question": "How do you make the text bold in CSS?", "options": ["font-weight: bold", "text-style: bold", "font-style: bold", "text-weight: bold"], "answer": "font-weight: bold"},
        {"id": 10, "question": "Which CSS property is used for spacing between letters?", "options": ["letter-spacing", "word-spacing", "text-spacing", "character-spacing"], "answer": "letter-spacing"},
    ],
    "js": [
        {"id": 11, "question": "Which symbol is used for comments in JavaScript?", "options": ["//", "/* */", "#", "<!-- -->"], "answer": "//"},
        {"id": 12, "question": "How do you declare a variable in JavaScript?", "options": ["var", "let", "const", "All of these"], "answer": "All of these"},
        {"id": 13, "question": "Which method converts JSON to an object?", "options": ["JSON.parse()", "JSON.stringify()", "JSON.convert()", "JSON.toObject()"], "answer": "JSON.parse()"},
        {"id": 14, "question": "What keyword is used to create a function?", "options": ["function", "def", "fun", "func"], "answer": "function"},
        {"id": 15, "question": "How do you write 'Hello World' in an alert box?", "options": ["alert('Hello World')", "msg('Hello World')", "msgBox('Hello World')", "alertBox('Hello World')"], "answer": "alert('Hello World')"},
    ],
    "python": [
        {"id": 16, "question": "Which keyword is used to define a function in Python?", "options": ["def", "function", "func", "define"], "answer": "def"},
        {"id": 17, "question": "What is the output of print(2**3)?", "options": ["6", "8", "9", "5"], "answer": "8"},
        {"id": 18, "question": "How do you create a list in Python?", "options": ["[1, 2, 3]", "{1, 2, 3}", "(1, 2, 3)", "<1, 2, 3>"], "answer": "[1, 2, 3]"},
        {"id": 19, "question": "What symbol is used to start a comment?", "options": ["#", "//", "/*", "<!--"], "answer": "#"},
        {"id": 20, "question": "Which data type is immutable?", "options": ["List", "Dictionary", "Tuple", "Set"], "answer": "Tuple"},
    ],
    "java": [
        {"id": 21, "question": "Which method is the entry point of a Java program?", "options": ["main()", "start()", "run()", "init()"], "answer": "main()"},
        {"id": 22, "question": "Which of these is a valid Java identifier?", "options": ["123abc", "abc123", "java-123", "None of the above"], "answer": "abc123"},
        {"id": 23, "question": "Which keyword is used to inherit a class?", "options": ["extends", "implements", "inherits", "super"], "answer": "extends"},
        {"id": 24, "question": "What is the size of int in Java?", "options": ["4 bytes", "2 bytes", "8 bytes", "Depends on system"], "answer": "4 bytes"},
        {"id": 25, "question": "Which package contains the Scanner class?", "options": ["java.util", "java.io", "java.lang", "java.net"], "answer": "java.util"},
    ],
    "c": [
        {"id": 26, "question": "Which header file is necessary for printf()?", "options": ["stdio.h", "conio.h", "string.h", "math.h"], "answer": "stdio.h"},
        {"id": 27, "question": "Which operator is used to access value at the address stored in a pointer?", "options": ["&", "*", "%", "#"], "answer": "*"},
        {"id": 28, "question": "Which of these is the correct way to declare an integer?", "options": ["int num;", "num int;", "integer num;", "int: num;"], "answer": "int num;"},
        {"id": 29, "question": "Which function is used to read a single character from the console?", "options": ["getchar()", "scanf()", "gets()", "putchar()"], "answer": "getchar()"},
        {"id": 30, "question": "Which loop is guaranteed to execute at least once?", "options": ["for", "while", "do-while", "foreach"], "answer": "do-while"},
    ],
}

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('select_subject'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('select_subject'))

    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username] == password:
            session.permanent = True
            session['user'] = username
            return redirect(url_for('select_subject'))
        else:
            error = 'Invalid username or password'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/select-subject')
def select_subject():
    if 'user' not in session:
        return redirect(url_for('login'))
    subjects = list(questions_db.keys())
    return render_template('select_subject.html', subjects=subjects, user=session['user'])

@app.route('/quiz/<subject>')
def quiz(subject):
    if 'user' not in session:
        return redirect(url_for('login'))
    if subject not in questions_db:
        return "Subject not found", 404
    return render_template('quiz.html', subject=subject, user=session['user'])

@app.route('/api/questions/<subject>')
def get_questions(subject):
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    if subject not in questions_db:
        return jsonify({"error": "Subject not found"}), 404

    # Pick 5 random questions for the quiz
    questions = random.sample(questions_db[subject], 5)
    questions_to_send = []
    for q in questions:
        q_copy = q.copy()
        q_copy.pop('answer')  # Don't send answers to frontend
        questions_to_send.append(q_copy)
    return jsonify(questions_to_send)

@app.route('/api/submit/<subject>', methods=['POST'])
def submit(subject):
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    if subject not in questions_db:
        return jsonify({"error": "Subject not found"}), 404

    user_answers = request.json.get('answers')  # dict {question_id: selected_option}
    if not user_answers:
        return jsonify({"error": "No answers submitted"}), 400

    correct_count = 0
    for q in questions_db[subject]:
        qid = str(q['id'])
        if qid in user_answers:
            if user_answers[qid] == q['answer']:
                correct_count += 1

    return jsonify({"score": correct_count, "total": 5})

if __name__ == '__main__':
    app.run(debug=True)
