from flask import Flask, make_response, render_template, request, redirect, url_for, session
from bcrypt import checkpw
from data import users
from os import urandom
FORM_USERNAME = 'username'
FORM_PASSWORD = 'password'
SESSION_USERNAME = 'username'

app = Flask(__name__)
app.secret_key = urandom(16)

@app.route('/')
def index():
    response = make_response(render_template('index.html', username=SESSION_USERNAME))
    #response.set_cookie('nazwa_uzytkownika', 'tony halik')
    return response


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form[FORM_USERNAME]
        pwd = request.form[FORM_PASSWORD]
        if user in users:
            if checkpw(pwd.encode('utf-8'), users[user]):
                #nazwa uzytkownika i haslo zgadzaja sie
                session[SESSION_USERNAME] = user
                return redirect(url_for('index'))
            else:
                return redirect(url_for('bad_login'))
        else:
            return redirect(url_for('bad_login'))
    else:
        response = make_response(render_template('login.html', username = FORM_USERNAME, password = FORM_PASSWORD))
        return response


@app.route('/bad_login/')
def bad_login():
    return render_template('bad_login.html')

@app.route('/logout/')
def logout():
    session.pop(SESSION_USERNAME)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
