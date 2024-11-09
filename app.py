from flask import Flask, render_template, redirect, url_for, request, session,jsonify
import requests, googlemaps
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length

app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path='/')
app.config['SECRET_KEY'] = 'fsaufvuyagbubikni'

API_KEY='AIzaSyDT3TNy2KLvYHQWWpJ-IZDjFodhOfDAFeU'
# Dummy in-memory users (for demonstration purposes)
users_db = {}

# Forms for Login and Signup
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=6)])

class ForgotPasswordForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4)])
    new_password = PasswordField('New Password', validators=[InputRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=6)])

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # Check if the user exists and password matches
        if username in users_db and users_db[username] == password:
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials, please try again.'

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        
        # Check if passwords match
        if password != confirm_password:
            return 'Passwords do not match.'
        
        # Save the user in the database (in this case, just a dictionary)
        if username in users_db:
            return 'Username already taken.'
        
        users_db[username] = password
        return redirect(url_for('dashboard'))
    
    return render_template('register.html', form=form)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        username = form.username.data
        new_password = form.new_password.data
        confirm_password = form.confirm_password.data

        # Check if the user exists
        if username not in users_db:
            return 'Username not found.'

        # Check if passwords match
        if new_password != confirm_password:
            return 'Passwords do not match.'

        # Update password in the database
        users_db[username] = new_password
        return redirect(url_for('login'))

    return render_template('forgot_password.html', form=form)


@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    carbon_perks = 100
    PrestoBalance = 5
    results = None
    return render_template('dashboard.html',carbon_perks=carbon_perks,results=results,PrestoBalance=PrestoBalance)



if __name__ == '__main__':
    app.run(debug=True)