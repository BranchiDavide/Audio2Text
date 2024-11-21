from models.apikey import ApiKey
from functools import wraps
from flask import request, jsonify
import secrets
def generate_api_key():
    return secrets.token_hex(32)

def validate_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return jsonify({"status": "error", "message": "API Key is missing"}), 401
        
        api_key_db = ApiKey.query.filter_by(value=api_key).first()
        if not api_key_db:
            return jsonify({"status": "error", "message": "Invalid API Key"}), 403
        
        return f(*args, **kwargs)
    return decorated_function