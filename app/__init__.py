from flask import Flask
from .controllers.naver_crawling_controller import configure_routes
from .services.kafka_topic01_service import kafka_topic_01
from .services.kafka_topic02_service import kafka_topic_02
from .services.kafka_topic03_service import kafka_topic_03

from .services.kafka_topic04_service import kafka_topic_04
from .services.kafka_topic11_service import kafka_topic_11
from .services.kafka_topic21_service import kafka_topic_21
from .services.kafka_topic31_service import kafka_topic_31
import threading


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.config")

    configure_routes(app)

    kafka_thread = threading.Thread(target=kafka_topic_01, args=(app,))
    kafka_thread.start()

    kafka_thread = threading.Thread(target=kafka_topic_02, args=(app,))
    kafka_thread.start()

    kafka_thread = threading.Thread(target=kafka_topic_03, args=(app,))
    kafka_thread.start()

    kafka_thread = threading.Thread(target=kafka_topic_04, args=(app,))
    kafka_thread.start()

    kafka_thread = threading.Thread(target=kafka_topic_11, args=(app,))
    kafka_thread.start()

    kafka_thread = threading.Thread(target=kafka_topic_21, args=(app,))
    kafka_thread.start()

    kafka_thread = threading.Thread(target=kafka_topic_31, args=(app,))
    kafka_thread.start()

    return app
