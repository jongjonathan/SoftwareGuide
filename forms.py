from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, none_of
import csv

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired("A username is required."), Length(min = 5, max = 10, message = "Must be between 5 and 10 characters long.")])
    password = PasswordField('Password', validators=[InputRequired("A password is required")])
    submit = SubmitField('Submit')

def check_password(username, password):
     with open('data/sign.csv') as f:
            for user in csv.reader(f):
             if username == user[0] and password == user[1]:
                    return True
     return False
def check_user(username):
    with open('data/sign.csv') as f:
        for user in csv.reader(f):
            if username == user[0]:
                return True
    return False

class PassResetForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired("A username is required."), Length(min=5, max=10, message="Must be between 5 and 10 characters long.")])
    password = PasswordField('Password', validators=[InputRequired("A password is required"),none_of(values=['password'], message="Password cannot be password")])
    passcheck = PasswordField('Confirm Password', validators=[InputRequired("Must be the same password")])
    submit = SubmitField('Submit')





