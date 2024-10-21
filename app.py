from flask import Flask

app = Flask(__name__)

from routes.api_routes import api
app.register_blueprint(api, url_prefix='/api/v1')


if __name__ == '__main__':
    app.run(debug=True)