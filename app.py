import os
from flask import Flask
from dotenv import load_dotenv
from flask_migrate import Migrate
from database.connection import db
from flask_login import LoginManager

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

# Routes configuration
from routes.api_routes import api
from routes.auth import auth
from routes.homepage import homepage
app.register_blueprint(api, url_prefix='/api/v1')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(homepage, url_prefix='/')

# Auth configuration
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

@login_manager.user_loader
def load_user(user_id):
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.execute(stmt).scalar_one_or_none()
    return user

if __name__ == '__main__':
    app.run(debug=True)