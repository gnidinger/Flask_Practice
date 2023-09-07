from confluent_kafka import Consumer, Producer, KafkaError
from .naver_visitor_service import main
import json


def kafka_topic_31(app):
    consumer_config = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "my-group",
        "auto.offset.reset": "earliest",
    }
    producer_config = {
        "bootstrap.servers": "localhost:9092",
    }

    consumer = Consumer(consumer_config)
    producer = Producer(producer_config)

    consumer.subscribe(["topicA31"])

    def delivery_report(err, msg):
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()}")

    while True:
        msg = consumer.poll(1)

        if msg is None:
            continue

        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break

        msg_key = msg.key().decode("utf-8") if msg.key() else "None"
        msg_value = msg.value().decode("utf-8")
        print(f"Received: key={msg_key}, value={msg_value}")

        try:
            prefix, query = msg_value.split(":", 1)
            if prefix == "INPUT":
                # Selenium 로직 실행
                with app.app_context():
                    result = main(query)
                    # result_dict_list = [r.to_dict() for r in result]
                    # result_str = json.dumps(result_dict_list)
                    result_str = json.dumps(result)
                    producer.produce(
                        "topicA32", key=msg_key, value=result_str, callback=delivery_report
                    )
                    producer.flush()
            else:
                print("Invalid prefix")
        except ValueError:
            print("Invalid message format")

    consumer.close()


if __name__ == "__main__":
    kafka_consumer()
