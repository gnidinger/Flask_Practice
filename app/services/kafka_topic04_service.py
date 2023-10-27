from selenium.common.exceptions import NoSuchElementException
from confluent_kafka import Consumer, Producer, KafkaError
from confluent_kafka.avro import AvroConsumer, AvroProducer
from confluent_kafka.avro.serializer import SerializerError
from avro.schema import parse
import json
import uuid
from .naver_view_blog_service import main


def kafka_topic_04(app):
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

    consumer.subscribe(["topicA04"])

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
        query = msg_value["message"]

        with app.app_context():
            try:
                result_view_blog = main(query)  # 단일 쿼리 문자열로 처리

                filtered_results = []

                if result_view_blog:
                    for response in result_view_blog:
                        # '?' 문자가 들어있는 블로그 ID는 무시
                        if "?" in response.blogId:
                            continue
                        filtered_results.append(response)

                    for response in filtered_results:  # 각각의 결과를 별도의 메시지로 처리
                        new_uniqueId = str(uuid.uuid4())  # 각 response마다 새로운 UUID 생성

                        result_view_blog_dict = response.to_dict()
                        new_message = {
                            "parentId": parentId,
                            "uniqueId": new_uniqueId,
                            "message": json.dumps(result_view_blog_dict, ensure_ascii=False),
                        }

                        producer.produce(
                            topic="topicA05",
                            key=new_uniqueId,
                            value=new_message,
                            callback=delivery_report,
                        )
            except NoSuchElementException:
                print("View-Blog 검색 실패")
                # 요소를 찾을 수 없는 경우 그냥 건너뛰기
                continue
        producer.flush()

    consumer.close()


if __name__ == "__main__":
    kafka_topic_04()
