from flask import Flask, Blueprint


def create_app():
    app = Flask(__name__)
    api = Blueprint("api", __name__, url_prefix="/api")

    @app.route("/")
    def home():
        return "Hello, World!"

    app.register_blueprint(api)

    return app
