from database.connection import db
class Transcription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    audio_path = db.Column(db.String(120), nullable=False)
    text = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)