from database.connection import db
import bcrypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    transcriptions = db.relationship('Transcription', backref='user', lazy=True)

    def set_password(self, password):
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(password.encode("UTF-8"), salt)

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("UTF-8"), self.password.encode("UTF-8"))