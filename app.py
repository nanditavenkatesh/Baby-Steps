import flask
import numpy as np
from bidict import bidict
from flask import (
    Flask, render_template, request,
    redirect, url_for, session
)
from random import choice
from tensorflow import keras
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

import password

global quiz


ENCODER = bidict({
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6,
    'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12,
    'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18,
    'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24,
    'Y': 25, 'Z': 26
})

app = Flask(__name__)
app.secret_key = 'alphabet_quiz'
app.logger = 0
app.aborter = 0

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = password.c
app.config['MYSQL_DB'] = 'babystepslogin'
mysql = MySQL(app)


@app.route('/')
def index():
    session.clear()
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


@app.route('/add-data', methods=['GET'])
def add_data_get():
    message = session.get('message', '')
    labels = np.load('data/labels.npy')
    count = {k: 0 for k in ENCODER.keys()}
    for label in labels:
        count[label] += 1
    count = sorted(count.items(), key=lambda x: x[1])
    letter = count[0][0]
    # letter = choice(list(ENCODER.keys()))
    return render_template("addData.html", letter=letter, message=message)


@app.route('/add-data', methods=['POST'])
def add_data_post():
    label = request.form['letter']
    labels = np.load('data/labels.npy')
    labels = np.append(labels, label)
    np.save("data/labels.npy", labels)

    pixels = request.form['pixels']
    pixels = pixels.split(',')
    img = np.array(pixels).astype(float).reshape(1, 50, 50)
    images = np.load('data/images.npy')
    images = np.vstack([images, img])
    np.save("data/images.npy", images)

    session['message'] = f'"{label}" Added to the Training Dataset'

    return redirect(url_for('add_data_get'))


@app.route('/practice', methods=['GET'])
def practice_get():
    letter = choice(list(ENCODER.keys()))
    return render_template("practice.html", letter=letter, correct='')


@app.route('/practice', methods=['POST'])
def practice_post():
    letter = request.form['letter']
    pixels = request.form['pixels']
    pixels = pixels.split(',')
    img = np.array(pixels).astype(float).reshape(1, 50, 50, 1)

    model = keras.models.load_model('letter.model')

    pred_letter = np.argmax(model.predict(img), axis=-1)
    pred_letter = ENCODER.inverse[pred_letter[0]]

    correct = 'yes' if pred_letter == letter else 'no'
    letter = choice(list(ENCODER.keys()))

    return render_template("practice.html", letter=letter, correct=correct)


@app.route('/attempt-quiz', methods=['GET'])
def quiz_get():
    letter = choice(list(ENCODER.keys()))
    return render_template("attemptQuiz.html", letter=letter, correct='')


@app.route('/attempt-quiz', methods=['POST'])
def quiz_post():
    if app.logger < 4:
        letter = request.form['letter']
        pixels = request.form['pixels']
        pixels = pixels.split(',')
        img = np.array(pixels).astype(float).reshape(1, 50, 50, 1)

        model = keras.models.load_model('letter.model')

        pred_letter = np.argmax(model.predict(img), axis=-1)
        pred_letter = ENCODER.inverse[pred_letter[0]]

        correct = 'yes' if pred_letter == letter else 'no'
        if correct == "yes":
            app.aborter += 1
        letter = choice(list(ENCODER.keys()))
        app.logger += 1
        return render_template("attemptQuiz.html", letter=letter, correct=correct)
    else:
        msg = "Score is " + str(app.aborter)
        app.logger = 0
        app.aborter = 0
        return render_template('score.html', msg=msg)

# @app.route('/score', methods=['GET'])
# def login(msg):
#     msg = 'Incorrect username / password !'
#     return render_template('login.html', msg=msg)

@app.route('/watch-tutorial')
def watchTutorial():
    session.clear()
    return render_template("watchtutorial.html")

@app.route('/videoA')
def videoA():
    session.clear()
    return flask.send_file("templates/atutorial.mp4")


if __name__ == '__main__':
    app.run(debug=True)
