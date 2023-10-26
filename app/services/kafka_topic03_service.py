from confluent_kafka import Consumer, Producer, KafkaError
from confluent_kafka.avro import AvroConsumer, AvroProducer
from confluent_kafka.avro.serializer import SerializerError
from avro.schema import parse
import json
import uuid
from .naver_tab_service import main
import re


def kafka_topic_03(app):
    consumer_config = {
        "bootstrap.servers": "localhost:19092",
        "group.id": "copykle-group",
        "auto.offset.reset": "earliest",
        "schema.registry.url": "http://127.0.0.1:8081",
    }

    value_schema = parse(
        open(
            "/Users/gnimom/Documents/Personal/Flask_Practice/app/services/NaverCrawlingSchema.avsc",
            "rb",
        ).read()
    )

    key_schema = parse(
        open(
            "/Users/gnimom/Documents/Personal/Flask_Practice/app/services/UUIDKeySchema.avsc",
            "rb",
        ).read()
    )

    producer_config = {
        "bootstrap.servers": "localhost:19092",
        "schema.registry.url": "http://127.0.0.1:8081",
    }

    consumer = AvroConsumer(consumer_config)
    producer = AvroProducer(
        producer_config, default_key_schema=key_schema, default_value_schema=value_schema
    )

    consumer.subscribe(["topicA03"])

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

        msg_key = msg.key() if msg.key() else "None"
        msg_value = msg.value()

        parentId = msg_value.get("uniqueId")
        # query = msg_value["message"]  # 메시지를 query 변수에 할당

        match = re.search(r"relKeyword=([^\,]+)", str(msg_value))
        if match:
            query = match.group(1)  # 첫 번째 그룹에 해당하는 값을 쿼리로 사용
        else:
            print("Query not found in the message!")
            continue

        print("check point 1: " + query)

        new_uniqueId = str(uuid.uuid4())

        with app.app_context():
            result_tabs = main(query)

            if result_tabs is not None:
                result_tabs_json = json.dumps(result_tabs, ensure_ascii=False)

                new_message = {
                    "parentId": parentId,
                    "uniqueId": new_uniqueId,
                    "message": result_tabs_json,
                }

                producer.produce(
                    topic="topicA04",
                    key=new_uniqueId,
                    value=new_message,
                    callback=delivery_report,
                )
                producer.flush()

    consumer.close()


if __name__ == "__main__":
    kafka_topic_03()
