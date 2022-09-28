from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Create a Flask Instance
app = Flask(__name__)
# Add the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SECRET_KEY'] = 'my secret key'

# Initialize the database
db = SQLAlchemy(app)


from app import routes



# This function creates a database if it doesn't already exist
def create_database(app):
    if not path.exists('webservice/user.db'):
        db.create_all(app=app)
        print('Created Database!')


create_database(app)

# define a function to use LoginManager to manage user login
def mangage_login():
    login_manager = LoginManager()
    # This is where flask will redirect the users if they are not logged in
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    # This is telling flask what user model we are looking for and referencing the user by their ID
    @login_manager.user_loader
    def load_user(id):
        from .models import User
        return User.query.get(int(id))

mangage_login()