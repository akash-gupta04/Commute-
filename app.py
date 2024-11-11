from flask import Flask, render_template, redirect, url_for, request, session,jsonify
import requests, googlemaps,random
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length
from map import get_distance,get_coordinates,get_time

app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path='/')
app.config['SECRET_KEY'] = '__API_Key__'

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

offers = {
    "10% off Tim Hortons Gift Card": 100,
    "Free Coffee at Starbucks": 50,
    "5% off on Amazon Gift Card": 150,
    "Discount on Transit Pass": 75,
    "Buy 1 Get 1 Free Movie Ticket": 120
}
@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    PrestoBalance = 5
    start = request.args.get('start')
    end = request.args.get('end')
    mode = request.args.get('mode')
    get_coordinates(start)
    get_coordinates(end)
    bike_perks = 0
    transit_perks = 0
    walking_perks = 0
    distance = get_distance(start,end,mode) 
    if mode == 'bicycling':
        bike_perks += distance * 15
    elif mode == 'walking':
        walking_perks += distance * 20
    elif mode == 'transit':
        transit_perks += distance * 2
    total_perks = bike_perks + walking_perks + transit_perks
    time = get_time(start,end,mode)
    session['total_perks'] = total_perks
    session['bike_perks'] = bike_perks
    session['walking_perks'] = walking_perks
    session['transit_perks'] = transit_perks
    session['distance'] = distance
    return render_template('dashboard.html',walking_perks = walking_perks, transit_perks=transit_perks,bike_perks=bike_perks, total_perks=total_perks,distance=distance,PrestoBalance=PrestoBalance,time=time)


@app.route('/redeem',methods=['GET','POST'])
def redeem_perks():
    walking_perks = session.get('walking_perks', request.args.get('dashboard'))
    transit_perks = session.get('transit_perks', request.args.get('dashboard'))
    bike_perks = session.get('bike_perks', request.args.get('dashboard'))
    total_perks = session.get('total_perks', request.args.get('dashboard'))
    message = ""

    # Select a random offer to display
    random_offer = random.choice(list(offers.items()))

    if request.method == 'POST':
        selected_offer = request.form.get('offer')
        
        # Check if the selected offer exists in the dictionary
        if selected_offer and selected_offer in offers:
            perk_cost = offers[selected_offer]
            if total_perks >= perk_cost:
                session['total_perks'] -= perk_cost
                message = f"Successfully redeemed {selected_offer} for {perk_cost} perks!"
            else:
                message = "You don't have enough perks to redeem this offer."
        else:
            message = "Please select a valid offer."

    return render_template('redeem.html', perks=session['total_perks'], offers=offers, message=message, random_offer=random_offer, walking_perks = walking_perks, transit_perks=transit_perks,bike_perks=bike_perks, total_perks=total_perks)

@app.route('/redeem-success')
def redeem_success():
    perks = session.get('total_perks', request.args.get('redeem'))
    return render_template('redeem-success.html',perks=perks)

if __name__ == '__main__':
    app.run(debug=True)
