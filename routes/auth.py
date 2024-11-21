from flask import Blueprint, render_template, request, flash, redirect
from flask_login import login_user, logout_user, login_required, current_user
from database.connection import db
from models.user import User
from utils.apikeyvalidator import generate_api_key

auth = Blueprint("auth", __name__)

@auth.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect("/")
    return render_template("auth/login.html")

@auth.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username:
        flash("Username is required")
        return render_template("auth/login.html")
    
    if not password:
        flash("Password is required")
        return render_template("auth/login.html")

    user = User.query.filter_by(username=username).first()
    if not user:
        flash("Username or password incorrect. Try agin")
        return render_template("auth/login.html")

    if not user.check_password(password):
        flash("Username or password incorrect. Try agin")
        return render_template("auth/login.html")
    
    login_user(user)
    return redirect("/")

@auth.route("/signup")
def signup():
    if current_user.is_authenticated:
        return redirect("/")
    return render_template("auth/signup.html")

@auth.route("/signup", methods=["POST"])
def signup_post():
    firstname = request.form.get("fname")
    lastname = request.form.get("lname")
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    r_password = request.form.get("rpassword")
    
    if not firstname:
        flash("First name is required")
        return render_template("auth/signup.html", firstname=firstname, lastname=lastname, email=email, username=username)
    
    if not lastname:
        flash("Last name is required")
        return render_template("auth/signup.html", firstname=firstname, lastname=lastname, email=email, username=username)
    
    if not email:
        flash("Email is required")
        return render_template("auth/signup.html", firstname=firstname, lastname=lastname, email=email, username=username)

    if not username:
        flash("Username is required")
        return render_template("auth/signup.html", firstname=firstname, lastname=lastname, email=email, username=username)
    
    if not password:
        flash("Password is required")
        return render_template("auth/signup.html", firstname=firstname, lastname=lastname, email=email, username=username)

    if not r_password:
        flash("Confirm password is required")
        return render_template("auth/signup.html", firstname=firstname, lastname=lastname, email=email, username=username)
    
    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        flash("User with this email already exists")
        return render_template("auth/signup.html", firstname=firstname, lastname=lastname, email=email, username=username)

    existing_username = User.query.filter_by(username=username).first()
    if existing_username:
        flash("User with this username already exists")
        return render_template("auth/signup.html", firstname=firstname, lastname=lastname, email=email, username=username)
    
    if password != r_password:
        flash("Passwords do not match")
        return render_template("auth/signup.html", firstname=firstname, lastname=lastname, email=email, username=username)
    
    user = User(firstname=firstname, lastname=lastname, email=email, username=username)
    user.set_password(password)
    user.set_api_key(generate_api_key())
    db.session.add(user)
    db.session.commit()

    return render_template("auth/signupsuccess.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/auth/login")