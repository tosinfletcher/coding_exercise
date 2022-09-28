from app import db
from flask_login import UserMixin


# Defind User calss that will be used to create our database table
# For the user object inherit UserMixin from flask_login
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    last_login = db.Column(db.String(60), nullable=True)

