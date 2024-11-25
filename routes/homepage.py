from flask import Blueprint, render_template, redirect
from flask_login import current_user

homepage = Blueprint("homepage", __name__)

@homepage.route("/")
def home():
    if current_user.is_authenticated:
        user_api_key = current_user.get_api_keys().first().value
        return render_template("home.html", firstname=current_user.firstname, lastname=current_user.lastname, user_api_key=user_api_key)
    else:
        return redirect("/auth/login")

@homepage.route("my-transcriptions")
def my_transcriptions():
    return NotImplementedError

@homepage.route("transcribe")
def transcribe():
    return render_template("transcribe.html")