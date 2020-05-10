from flask import Flask, render_template, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from forms import SignUpForm, PassResetForm
from forms import check_password, check_user
import os

import csv


app = Flask(__name__)
app.secret_key = 'a3'
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'
app.config['USE_SESSION_FOR_NEXT'] = True

class User(UserMixin):
    def __init__(self, username):
        self.id = username



@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def base():
    return render_template("home.html")

@app.route('/personal')
@login_required
def personal():
    return render_template('personal.html')
@app.route('/daily')
@login_required
def daily():
    return render_template('daily.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/tips')
@login_required
def tips():
    return render_template('tips.html')

@app.route('/survival')
@login_required
def survival():
    return render_template('survival.html')
@app.route('/clocks')
def clocks():
    return render_template('clocks.html.')

@app.route('/signupres')
def signupres():
    return render_template('signupres.html')

@app.route('/signup', methods= ['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = check_user(form.username.data)
        if not user:
            with open('data/sign.csv', 'a') as f:
             writer = csv.writer(f,lineterminator = '\n')
             writer.writerow([form.username.data, form.password.data])
            return redirect(url_for('signupres', username=form.username.data))
        else:
            flash('Username already taken')
            return render_template('signup.html.', form=form)


    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = SignUpForm()
    if form.validate_on_submit():
        if check_password(form.username.data, form.password.data) or (form.username.data == 'admin'and form.password.data):
            login_user(User(form.username.data))
            session['username'] = form.username.data
            return redirect('home')
        else:
            flash('Incorrrect Username or Password, try again..')
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)

@app.route('/passreset',methods=['GET', 'POST'])
def pass_reset():
    form = PassResetForm()
    if form.validate_on_submit():
        user = check_user(form.username.data)
        if not user:
            flash("Incorrect username")
        if user and form.password.data == form.passcheck.data:
            with open('data/sign.csv', 'r') as readFile:
                reader = csv.reader(readFile)
                with open('data/reset.csv', 'w', newline='') as f:
                    writer = csv.writer(f)
                    for user in reader:
                        if form.username.data == user[0]:
                            writer.writerow([form.username.data, form.passcheck.data])
                        else:
                            writer.writerow([user[0], user[1]])
            with open('data/reset.csv', 'r') as q:
                reader = csv.reader(q)
                with open ('data/sign.csv', 'w', newline = '') as f:
                    writer = csv.writer(f)
                    for user in reader:
                        writer.writerow([user[0], user[1]])

            os.remove('data/reset.csv')
            return redirect(url_for('signupres', username=form.username.data))
        return redirect('passreset')
    else:
        return render_template('passreset.html', form=form)

@app.route('/table')
def table():
    users = []
    with open('data/sign.csv', 'r') as f:
        reader = csv.reader(f)
        for user in reader:
            name = user[0]
            users.append(name)
    return render_template('users.html', users = users)

@app.route('/admin',methods=['GET', 'POST'])
def admin():
    form = SignUpForm()
    if form.validate_on_submit():
        if (form.username.data == 'admin' and form.password.data == '1q2w3e4r'):
            users = []
            passwords = []
            with open('data/sign.csv', 'r') as f:
                reader = csv.reader(f)
                for user in reader:
                    name = user[0]
                    users.append(name)
                    pasw = user[1]
                    passwords.append(pasw)
            return render_template('admin.html.', users=users, passwords = passwords)
        else:
            return render_template('adminlog.html', form=form)
    else:
        return render_template('adminlog.html' ,form = form)




@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

if __name__ == '__main__':
    app.run()

