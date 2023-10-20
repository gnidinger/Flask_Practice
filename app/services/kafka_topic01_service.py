from confluent_kafka import Consumer, Producer, KafkaError
from confluent_kafka.avro import AvroConsumer, AvroProducer
from confluent_kafka.avro.serializer import SerializerError
from avro.schema import parse
import json
import uuid
from .keyword_service import main as keyword_main
from .keyword_shopping_service import main as keyword_shopping_main
from .keyword_google_service import main as keyword_google_main
from .naver_tab_service import main


def kafka_topic_01(app):
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

    consumer.subscribe(["topicA01"])

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

        print("check point 1: " + query)
        print(f"Type of 'query': {type(query)}")

        # 문자열이 None이거나 빈 문자열인 경우 넘어감
        if query is None or query.strip() == "":
            continue

        # 문자열을 쉼표로 분리하고 각 요소에 대해 공백을 제거한 후 처리
        query_elements = [elem.strip() for elem in query.split(",")]

        result_list = []

        for query_elem in query_elements:
            with app.app_context():
                keyword_list = keyword_main(query_elem)
                keyword_shopping_list = keyword_shopping_main(query_elem)
                keyword_google = keyword_google_main(query_elem)

                # 결과가 비어있지 않은 경우에만 추가
                if keyword_list:
                    result_list.append(f"{query_elem}, {', '.join(keyword_list)}")
                if keyword_shopping_list:
                    result_list.append(f"{query_elem}, {', '.join(keyword_shopping_list)}")
                if keyword_google:
                    result_list.append(f"{query_elem}, {', '.join(keyword_google)}")

        # 리스트가 비어있지 않은 경우에만 결합
        if result_list:
            result = ", ".join(result_list)
        else:
            result = ""

        print("check point 2: " + result)

        result_list_json = json.dumps(result, ensure_ascii=False)

        new_message = {
            "parentId": parentId,
            "uniqueId": new_uniqueId,
            "message": result_list_json,
        }

        producer.produce(
            topic="topicA02", key=new_uniqueId, value=new_message, callback=delivery_report
        )
        producer.flush()

    consumer.close()


if __name__ == "__main__":
    kafka_topic_01()
