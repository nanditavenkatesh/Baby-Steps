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
            session['role'] = account['role']
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
    session.pop('role', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        default_role = 'user'  # set default role value for new user
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
            cursor.execute('INSERT INTO accounts (username, password, email, role) VALUES (% s, % s, % s, % s)', (username, password, email, default_role,))
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
    return flask.send_file("templates/videos/atutorial.mp4")

@app.route('/videoB')
def videoB():
    session.clear()
    return flask.send_file("templates/videos/btutorial.mp4")

@app.route('/videoC')
def videoC():
    session.clear()
    return flask.send_file("templates/videos/ctutorial.mp4")

@app.route('/videoD')
def videoD():
    session.clear()
    return flask.send_file("templates/videos/dtutorial.mp4")

@app.route('/videoE')
def videoE():
    session.clear()
    return flask.send_file("templates/videos/etutorial.mp4")

@app.route('/videoF')
def videoF():
    session.clear()
    return flask.send_file("templates/videos/ftutorial.mp4")

@app.route('/videoG')
def videoG():
    session.clear()
    return flask.send_file("templates/videos/gtutorial.mp4")

@app.route('/videoH')
def videoH():
    session.clear()
    return flask.send_file("templates/videos/htutorial.mp4")

@app.route('/videoI')
def videoI():
    session.clear()
    return flask.send_file("templates/videos/itutorial.mp4")

@app.route('/videoJ')
def videoJ():
    session.clear()
    return flask.send_file("templates/videos/jtutorial.mp4")

@app.route('/videoK')
def videoK():
    session.clear()
    return flask.send_file("templates/videos/ktutorial.mp4")

@app.route('/videoL')
def videoL():
    session.clear()
    return flask.send_file("templates/videos/ltutorial.mp4")

@app.route('/videoM')
def videoM():
    session.clear()
    return flask.send_file("templates/videos/mtutorial.mp4")

@app.route('/videoN')
def videoN():
    session.clear()
    return flask.send_file("templates/videos/ntutorial.mp4")

@app.route('/videoO')
def videoO():
    session.clear()
    return flask.send_file("templates/videos/otutorial.mp4")

@app.route('/videoP')
def videoP():
    session.clear()
    return flask.send_file("templates/videos/ptutorial.mp4")

@app.route('/videoQ')
def videoQ():
    session.clear()
    return flask.send_file("templates/videos/qtutorial.mp4")

@app.route('/videoR')
def videoR():
    session.clear()
    return flask.send_file("templates/videos/rtutorial.mp4")

@app.route('/videoS')
def videoS():
    session.clear()
    return flask.send_file("templates/videos/stutorial.mp4")

@app.route('/videoT')
def videoT():
    session.clear()
    return flask.send_file("templates/videos/ttutorial.mp4")

@app.route('/videoU')
def videoU():
    session.clear()
    return flask.send_file("templates/videos/ututorial.mp4")

@app.route('/videoV')
def videoV():
    session.clear()
    return flask.send_file("templates/videos/vtutorial.mp4")

@app.route('/videoW')
def videoW():
    session.clear()
    return flask.send_file("templates/videos/wtutorial.mp4")

@app.route('/videoX')
def videoX():
    session.clear()
    return flask.send_file("templates/videos/xtutorial.mp4")

@app.route('/videoY')
def videoY():
    session.clear()
    return flask.send_file("templates/videos/ytutorial.mp4")

@app.route('/videoZ')
def videoZ():
    session.clear()
    return flask.send_file("templates/videos/ztutorial.mp4")

if __name__ == '__main__':
    app.run(debug=True)
