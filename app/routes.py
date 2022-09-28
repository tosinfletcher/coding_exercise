from app import app
from flask import render_template, request, flash, redirect, url_for
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime, date
import time


# create a route for the home page
@app.route('/')
@app.route('/home')
# Users cannot get to the home page unless they are logged in
@login_required
def index():
    return render_template('home.html', user=current_user)

# Create a route for the sign-up page with the GET and POST
@app.route('/sign-up', methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # assign the email address of the user to the variable user
        user = User.query.filter_by(email=email).first()

        # Create and if, elif and else statement to evaluate and ensure the user meet the sign-up credential requirement
        if user:
            flash('Email already exist.', category='error')
            return redirect(url_for('login'))
        elif len(name) < 2:
            flash('Name must be greater than 1 character.', category='error')
        elif len(email) < 5:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(password1) < 7:
            flash('Password is too short must be atleast 7 characters.', category='error')
        elif password1 != password2:
            flash('The password you entered don\'t match', category='error')

        # If all sign-up credential requirement are meet proceed to creating the new user's account
        else:
            new_user = User(name=name, email=email, password=generate_password_hash(password1, method='sha256'), )
            db.session.add(new_user)
            db.session.commit()
            # Once the user's account has been successfully created use the flash function to display a notification on the screen
            flash('Your Account has been created!', category='success')
            # Redirect the user to the login screen to login into their newly created account
            return redirect(url_for('login'))
    # serve the signup html page to the user when they access the signup endpoint
    return render_template('signup.html', user=current_user)

# Create a route for the login page with a GET and POST methods
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        # retrieve the email address provided by the user and store it in a variable called email
        email = request.form.get('email')
        # retrieve the password provided by the user and store it in a variable called password
        password = request.form.get('password')
        # query the database by the user's email address and store it in a variable called user
        user = User.query.filter_by(email=email).first()
        if user:
            # Use the check_password_hash function to validate the provided user's password and the password in the database
            if check_password_hash(user.password, password):
                # create the current date and assign it to the variable current_date
                current_date = str(date.today().strftime('%B %d, %Y'))
                # Update the last_login column in the database with the current date
                user.last_login = current_date
                # Commit the update to the database
                db.session.commit()
                # keep the user login session until the flask server is restarted - Allows user's to interact with their own personal home page
                login_user(user, remember=True)
                # Once the user has successfully logged into their account, use the flash function to display a notification on the screen
                flash('Logged in successfully!', category='success')
                # Redirect the user to their home page
                return redirect(url_for('index'))
            else:
                # Display the error on the screen if an incorrect password is provided during login
                flash('Incorrect password, try again.', category='error')
        else:
            # Notifies the user that the provided email address does not exist in the database
            flash('Email does not exist.', category='error')
    # Render the login html page to the current user.
    return render_template("login.html", user=current_user)

# Creates a route for user's to update their email address using the 'GET' and 'POST' method
@app.route('/update', methods = ['GET', 'POST'])
def update():
    # if the request method is retrieve both the old email address and new email address provided by the user and store them in a variable
    if request.method == 'POST':
        email = request.form.get('email')
        email_u1 = request.form.get('email_u1')

        # Use the old email address to query the database for the record by email
        user = User.query.filter_by(email=email).first()

        # If the email exist, update the database with the newly provided email address and commit the session
        if user:
            user.email = email_u1
            db.session.commit()
            # keep the user login session until the flask server is restarted
            login_user(user, remember=True)
            # Notify the user of the successful email update
            flash('Email address updated successfully!', category='success')
            # Redirect the user to the home page
            return redirect(url_for('index'))
        else:
            # If and incorrect email address is provided, notify the user
            flash('Incorrect email address, try again.', category='error')

    # Render the update html page to the current user.
    return render_template("update.html", user=current_user)


# Creates a logout route for the user
@app.route('/logout')
# Makes sure user's cannot access the logout route unless they are signed in
@login_required
def logout():
    # logout user
    logout_user()
    # Redirect user the login page after login out of their account
    return redirect(url_for('login'))

# Create a route for user's to be aple to delete their account with a combination of their email address.
@app.route('/delete-account', methods = ['GET','POST'])
def delete():
    # it the request method is a POST retrieve the user's email address and assign it to the variable email
    if request.method == 'POST':
        email = request.form.get('email')
        # Query the database for the user's email address
        user = User.query.filter_by(email=email).first()
        # If it exist delete the user's entire record
        if user:
            user.email = email
            time.sleep(2)
            db.session.delete(user)
            db.session.commit()
            # End the user's web session
            login_user(user, remember=False)
            # Notifiy the user of a successful deleteion
            flash('Account deleted successfully!', category='success')
            # Redirect the user to the sign-up page
            return redirect(url_for('sign_up'))
        else:
            # Notify the user if unable to delete their user account and instruct them to try again.
            flash('Unable to delete user account or User account does not exist, try again.', category='error')


    return render_template("delete.html", user=current_user)








