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
@validate_api_key
def get_all():
    # Return all the transcriptions of an authenticated user
    user = g.get("user")
    transcriptions = Transcription.query.filter_by(user_id=user.id).order_by(Transcription.created_at.desc()).all()
    response = {"status": "success"}
    transcriptions_resp = []
    for transcription in transcriptions:
        transcriptions_resp.append({
            "id": transcription.id,
            "title": transcription.title,
            "created_at": transcription.created_at.strftime("%d/%m/%Y %H:%M:%S"),
            "transcription_time": transcription.transcription_time,
            "text": transcription.text,
            "audio_path": transcription.audio_path,
            "detected_lang": transcription.detected_lang,
            "model": transcription.model
        })
    response["transcriptions"] = transcriptions_resp
    return jsonify(response)

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
        title_value = request.form["title"].strip()
        if len(title_value) > 0:
            title = title_value


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
    if os.path.isfile(os.path.join(os.getenv("UPLOAD_FOLDER"), filename)):
        user = g.get("user")
        audio_path_query = url_for("api.transcriber.get_audio", filename=filename)
        transcription = Transcription.query.filter_by(audio_path=audio_path_query).first()
        if not transcription:
            return jsonify({"status": "error", "message": "Audio file not found"}), 404
        if transcription.user_id != user.id:
            return jsonify({"status": "error", "message": "You don't have access to this resource"}), 403
        return send_from_directory(os.getenv("UPLOAD_FOLDER"), filename)
    else:
        return jsonify({"status": "error", "message": "Audio file not found"}), 404
    
@transcriber.route("/", methods=["DELETE"])
@validate_api_key
def delete():
    # Delete a transcription for an authenticated user
    transcription_id = request.json.get("id")
    if not transcription_id:
        return jsonify({"status": "error", "message": "Transcription ID is required."}), 400
    user = g.get("user")
    transcription = Transcription.query.filter_by(id=transcription_id, user_id=user.id).first()
    if not transcription:
        return jsonify({"status": "error", "message": "Transcription not found or not owned by the user."}), 404
    
    filename = os.path.join(UPLOAD_FOLDER, transcription.audio_path.split('/')[-1])
    os.remove(filename)

    db.session.delete(transcription)
    db.session.commit()

    return jsonify({"status": "success", "message": "Transcription deleted successfully."}), 200