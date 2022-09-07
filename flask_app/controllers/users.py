from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
@app.route("/")
def index():
    # call the get all classmethod to get all friends
    return render_template("index.html")
@app.route("/dashboard")
def show():
    return render_template("dashboard.html")

@app.route("/create_user", methods=['POST'])
def create_user():
    data = {
        "fname": request.form["fname"],
        "lname": request.form["lname"],
        "email": request.form["email"],
        "password": request.form["password"],
        "confirm_password": request.form["confirm_password"]
    }
    if not User.validate_register(data):
        return redirect('/')
    data['password'] = bcrypt.generate_password_hash(request.form['password'])
    current_user = User.save(data)
    session['user'] = current_user
    return redirect('/dashboard')
@app.route("/update_user", methods=['POST'])
def update_user():
    data = {
        "fname": request.form["fname"],
        "lname": request.form["lname"],
        "email": request.form["email"],
        "id": request.form["id"]
    }    
    User.update(data)
    return redirect(f'/users/{data["id"]}')