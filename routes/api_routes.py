from flask import Blueprint

api = Blueprint("api", __name__)

@api.get("/")
def root():
    return "API root"

from routes.api.transcriber import transcriber
api.register_blueprint(transcriber, url_prefix='/transcriber')