from database.connection import db
class Transcription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    audio_path = db.Column(db.String(120), nullable=False)
    text = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    detected_lang = db.Column(db.String(255), nullable=True)
    model = db.Column(db.String(255), nullable=False)
    transcription_time = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def set_title(self, title):
        self.title = title[:255]