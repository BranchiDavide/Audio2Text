from flask import Blueprint, jsonify, request
from utils.filechecker import *
import os
import uuid
import time
import whisper
whisper_model = whisper.load_model("base")

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

transcriber = Blueprint("transcriber", __name__)

@transcriber.route("/")
def get_all():
    # Return all the transcriptions of an authenticated user
    raise NotImplementedError

@transcriber.route("/", methods=["POST"])
def create():
    # Create a new transcription for an authenticated user
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
    transcription = whisper_model.transcribe(file_path)
    end_time = time.time()
    
    return jsonify({
                    "status": "success",
                    "transcription": transcription["text"],
                    "detected_lang": transcription["language"],
                    "transcription_time": round(end_time - start_time, 2)
                    }), 200