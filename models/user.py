from database.connection import db
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from sqlalchemy.dialects.mysql import CHAR

from models.apikey import ApiKey

bcrypt = Bcrypt()
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(CHAR(60), nullable=False)
    is_active = db.Column(db.Boolean, default=True) 

    transcriptions = db.relationship('Transcription', backref='user', lazy=True)
    api_keys = db.relationship('ApiKey', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    def set_api_key(self, key_value):
        new_key = ApiKey(user=self, value=key_value)
        db.session.add(new_key)
        db.session.commit()

    def get_api_keys(self):
        return self.api_keys