from confluent_kafka import Consumer, Producer, KafkaError
from confluent_kafka.avro import AvroConsumer, AvroProducer
from confluent_kafka.avro.serializer import SerializerError
from avro.schema import parse
import json
import uuid
from .naver_visitor_service import main


def kafka_topic_31(app):
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

        msg_key = msg.key() if msg.key() else "None"
        msg_value = msg.value()
        print(f"Received: key={msg_key}, value={msg_value}")

        message_content = json.loads(msg_value.get("message", "{}"))  # message 필드를 파싱
        blogId = message_content.get("blogId")  # message 내의 blogId를 가져옴
        publishDate = message_content.get("publishDate")
        print(blogId, publishDate)

        parentId = msg_value.get("uniqueId")
        new_uniqueId = str(uuid.uuid4())

        if blogId:
            with app.app_context():
                # main 함수를 실행하고 결과를 받음
                result_tabs = main(blogId)

                # 결과가 빈 배열이라면 무시하고 계속
                if len(result_tabs) == 0:
                    continue

                # 결과를 JSON 문자열로 변환
                result_tabs_json = json.dumps(result_tabs, ensure_ascii=False)

                # 새로운 메시지 생성
                new_message = {
                    "parentId": parentId,
                    "uniqueId": new_uniqueId,
                    "message": result_tabs_json,
                }

                # 새로운 토픽에 메시지를 produce 함
                producer.produce(
                    topic="topicA32", key=new_uniqueId, value=new_message, callback=delivery_report
                )
                producer.flush()

    consumer.close()


if __name__ == "__main__":
    kafka_consumer()
