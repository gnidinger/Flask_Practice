from confluent_kafka import Consumer, Producer, KafkaError
from confluent_kafka.avro import AvroConsumer, AvroProducer
from confluent_kafka.avro.serializer import SerializerError
from avro.schema import parse
import json
import uuid
from .naver_view_blog_service import main


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
        new_uniqueId = str(uuid.uuid4())

        query = msg_value["message"]

        try:
            tabs = json.loads(query)["tabs"]
        except (json.JSONDecodeError, KeyError):
            tabs = []  # "tabs" 키가 없거나 JSON 디코딩 오류 시 빈 리스트로 처리

        with app.app_context():
            for tab in tabs:
                result_view_blog = main(tab.strip())  # 각 탭을 공백 제거 후 호출

                filtered_results = []

                if result_view_blog:
                    for response in result_view_blog:
                        # '?' 문자가 들어있는 블로그 ID는 무시
                        if "?" in response.blogId:
                            continue
                        filtered_results.append(response)

                result_view_blog_str = json.dumps(
                    [response.to_dict() for response in filtered_results]
                )

                if filtered_results:  # 결과가 빈 리스트가 아니면 Kafka로 메시지를 전송
                    new_message = {
                        "parentId": parentId,
                        "uniqueId": new_uniqueId,
                        "message": result_view_blog_str,
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
    kafka_consumer()
