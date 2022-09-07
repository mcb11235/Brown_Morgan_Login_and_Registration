from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
USERNAME_REGEX = re.compile(r'[^a-zA-Z]gm')
class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( first_name , last_name , email , password ) VALUES ( %(fname)s , %(lname)s , %(email)s , %(password)s );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('user_schema').query_db( query, data )
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id=%(id)s"
        results = connectToMySQL('user_schema').query_db(query, data)
        return cls(results[0])
    @staticmethod
    def validate_register( user ):
        is_valid = True
        query = "SELECT * FROM users WHERE email=%(email)s"
        results = connectToMySQL('user_schema').query_db(query, user)
        if len(results) >= 1:
            flash("Email Address Already In Use")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email Address!")
            is_valid = False
        if len(user['fname']) < 2 or USERNAME_REGEX.match(user['fname']):
            flash("Invalid First Name!")
            is_valid = False
        if len(user['lname']) < 2 or USERNAME_REGEX.match(user['lname']):
            flash("Invalid Last Name!")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords Must Match!")
            is_valid = False
        return is_valid

