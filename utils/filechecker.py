import magic
ALLOWED_EXTENSIONS = ["wav", "mp3", "m4a"]
ALLOWED_MIME_TYPES = ["audio/wav", "audio/x-wav", "audio/mpeg3", "audio/mp4", "audio/x-mpeg-3", "audio/m4a", "audio/x-m4a", "audio/mpeg"]
def allowed_file_ext(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_ext(filename):
    return filename.rsplit(".", 1)[1].lower()

def allowed_mime_type(file):
    mime = magic.from_buffer(file.stream.read(2048), mime=True)
    file.stream.seek(0)
    return mime in ALLOWED_MIME_TYPES
