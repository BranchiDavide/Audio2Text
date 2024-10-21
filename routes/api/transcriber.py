from flask import Blueprint

transcriber = Blueprint("transcriber", __name__)

@transcriber.route("/")
def get_all():
    # Return all the transcriptions of an authenticated user
    raise NotImplementedError

@transcriber.route("/", methods=["POST"])
def create():
    # Create a new transcription for an authenticated user
    raise NotImplementedError
