from flask import Flask
from .controllers.naver_crawling_controller import configure_routes
from .services.kafka_consumer_service import kafka_consumer
import threading


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.config")

    configure_routes(app)

    kafka_thread = threading.Thread(target=kafka_consumer)
    kafka_thread.start()

    return app
