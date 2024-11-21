from database.connection import db
from sqlalchemy.dialects.mysql import CHAR

class ApiKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(CHAR(64), unique=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))