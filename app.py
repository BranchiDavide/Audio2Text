import os
from flask import Flask
from dotenv import load_dotenv
from flask_migrate import Migrate
from database.connection import db
load_dotenv()

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER")

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_SCHEMA")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
from models.user import User
from models.transcription import Transcription
migrate = Migrate(app, db)

from routes.api_routes import api
app.register_blueprint(api, url_prefix='/api/v1')


if __name__ == '__main__':
    app.run(debug=True)