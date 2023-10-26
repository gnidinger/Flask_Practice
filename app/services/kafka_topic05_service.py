from confluent_kafka import Consumer, Producer, KafkaError
from confluent_kafka.avro import AvroConsumer, AvroProducer
from confluent_kafka.avro.serializer import SerializerError
from avro.schema import parse
import json
import uuid
from .naver_visitor_service import main


def kafka_topic_05(app):
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

    consumer.subscribe(["topicA05"])

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

        # message 필드를 파싱
        message_content = msg_value.get("message", {})

        # message_content가 문자열인지 확인하고 파싱
        if isinstance(message_content, str):
            message_content = json.loads(message_content)

        blogId = message_content.get("blogId")  # blogId를 바로 가져옴
        publishDate = message_content.get("publishDate")
        print(blogId, publishDate)

        parentId = msg_value.get("uniqueId")
        new_uniqueId = str(uuid.uuid4())

        if blogId:
            with app.app_context():
                # main 함수를 실행하고 결과를 받음
                result_tabs = main(blogId)

                # 결과에서 visitorCount 값을 숫자로 파싱
                visitor_counts = [int(visitor_info["visitorCount"]) for visitor_info in result_tabs]

                # visitor_counts가 비어있지 않을 경우 평균 계산, 비어있으면 0
                avg_visitor_count = (
                    sum(visitor_counts) / len(visitor_counts) if visitor_counts else 0
                )

                # Avro Schema를 위해 float -> str로 파싱
                avg_visitor_count_str = str(avg_visitor_count)

                # 새로운 메시지 생성
                new_message = {
                    "parentId": parentId,
                    "uniqueId": new_uniqueId,
                    "message": json.dumps({"avgVisitorCount": avg_visitor_count_str}),
                }

                # 새로운 토픽에 메시지를 produce 함
                producer.produce(
                    topic="topicA06",
                    key=new_uniqueId,
                    value=new_message,
                    callback=delivery_report,
                )
                producer.flush()

                producer.flush()

    consumer.close()


if __name__ == "__main__":
    kafka_topic_05()
