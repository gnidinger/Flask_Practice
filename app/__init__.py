from flask import Flask
from .controllers.naver_crawling_controller import configure_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.config")

    configure_routes(app)

    return app
