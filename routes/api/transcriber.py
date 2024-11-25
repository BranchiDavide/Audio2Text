from flask import Blueprint, jsonify, request, send_from_directory, url_for, g
from utils.filechecker import *
from utils.apikeyvalidator import validate_api_key
from database.connection import db
from models.transcription import Transcription
import gc
import os
import uuid
import time
from datetime import datetime

import whisper
ALLOWED_MODELS = ["base", "tiny", "small", "medium", "turbo"]
base_model = whisper.load_model("base")

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

transcriber = Blueprint("transcriber", __name__)

@transcriber.route("/")
def get_all():
    # Return all the transcriptions of an authenticated user
    raise NotImplementedError

@transcriber.route("/", methods=["POST"])
@validate_api_key
def create():
    # Create a new transcription for an authenticated user
    user = g.get("user")
    if "file" not in request.files:
        return jsonify({"status": "error", "message": "File not found in the request"}), 400

    file = request.files["file"]
    
    if not allowed_file_ext(file.filename):
        return jsonify({"status": "error", "message": "Invalid file extension. Supported extensions: " + str(ALLOWED_EXTENSIONS)}), 400
    
    if not allowed_mime_type(file):
        return jsonify({"status": "error", "message": "Invalid mime type. Supported mime types: " + str(ALLOWED_MIME_TYPES)}), 400

    file.filename = f"{uuid.uuid4().hex}.{get_file_ext(file.filename)}"
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    start_time = time.time()
    transcription = ""
    model_name = "base" # Set default model to base
    if "model" in request.form:
        model_name = request.form["model"]
        if model_name not in ALLOWED_MODELS:
            return jsonify({"status": "error", "message": "Invalid model name. Supported models: " + str(ALLOWED_MODELS)}), 400
        model = whisper.load_model(model_name)
        transcription = model.transcribe(file_path)
        del model
        gc.collect()
    else:
        transcription = base_model.transcribe(file_path)
    end_time = time.time()
    
    current_time = datetime.now()
    formatted_date = current_time.strftime("%d/%m/%Y %H:%M:%S")
    formatted_date_db = current_time.strftime("%Y/%m/%d-%H:%M:%S")
    title = f"New transcription, {formatted_date}"
    if "title" in request.form:
        title = request.form["title"].strip()

    transcription_db = Transcription(audio_path=url_for("api.transcriber.get_audio", filename=file.filename), text=transcription["text"], user_id=user.id,
                                     created_at=formatted_date_db, detected_lang=transcription["language"], model=model_name, transcription_time=round(end_time - start_time, 2))
    transcription_db.set_title(title)
    db.session.add(transcription_db)
    db.session.commit()

    return jsonify({
                    "status": "success",
                    "transcription": transcription["text"],
                    "detected_lang": transcription["language"],
                    "transcription_time": round(end_time - start_time, 2),
                    "model": model_name
                    }), 200

@transcriber.route("/audio/<filename>")
@validate_api_key
def get_audio(filename):
    #TODO: Check if user is authorized to get audio file, and if file exists
    return send_from_directory(os.getenv("UPLOAD_FOLDER"), filename)