# from selenium.common.exceptions import NoSuchElementException
# from confluent_kafka import Consumer, Producer, KafkaError
# from confluent_kafka.avro import AvroConsumer, AvroProducer
# from confluent_kafka.avro.serializer import SerializerError
# from avro.schema import parse
# import json
# import uuid
# from .naver_view_blog_service import main


# def kafka_topic_04(app):
#     consumer_config = {
#         "bootstrap.servers": "localhost:19092",
#         "group.id": "copykle-group",
#         "auto.offset.reset": "earliest",
#         "schema.registry.url": "http://127.0.0.1:8081",
#     }

#     value_schema = parse(
#         open(
#             "/Users/gnimom/Documents/Personal/Flask_Practice/app/services/NaverCrawlingSchema.avsc",
#             "rb",
#         ).read()
#     )

#     key_schema = parse(
#         open(
#             "/Users/gnimom/Documents/Personal/Flask_Practice/app/services/UUIDKeySchema.avsc",
#             "rb",
#         ).read()
#     )

#     producer_config = {
#         "bootstrap.servers": "localhost:19092",
#         "schema.registry.url": "http://127.0.0.1:8081",
#     }

#     consumer = AvroConsumer(consumer_config)
#     producer = AvroProducer(
#         producer_config, default_key_schema=key_schema, default_value_schema=value_schema
#     )

#     consumer.subscribe(["topicA04"])

#     def delivery_report(err, msg):
#         if err is not None:
#             print(f"Message delivery failed: {err}")
#         else:
#             print(f"Message delivered to {msg.topic()}")

#     while True:
#         msg = consumer.poll(1)

#         if msg is None:
#             continue

#         if msg.error():
#             if msg.error().code() == KafkaError._PARTITION_EOF:
#                 continue
#             else:
#                 print(msg.error())
#                 break

#         msg_key = msg.key() if msg.key() else "None"
#         msg_value = msg.value()

#         parentId = msg_value.get("uniqueId")

#         query = msg_value["message"]

#         print("check point 4: " + query)

#         try:
#             query_json = json.loads(query)
#             tabs = query_json.get("tabs", [])
#         except (json.JSONDecodeError, AttributeError):
#             tabs = []  # JSON 디코딩 오류 또는 "tabs" 키가 없는 경우 빈 리스트로 처리

#         with app.app_context():
#             for tab in tabs:
#                 new_uniqueId = str(uuid.uuid4())

#                 try:
#                     result_view_blog = main(tab.strip())  # 각 탭을 공백 제거 후 호출

#                     filtered_results = []

#                     if result_view_blog:
#                         for response in result_view_blog:
#                             # '?' 문자가 들어있는 블로그 ID는 무시
#                             if "?" in response.blogId:
#                                 continue
#                             filtered_results.append(response)

#                         if filtered_results:  # 결과가 빈 리스트가 아니면 Kafka로 메시지를 전송
#                             result_view_blog_str = json.dumps(
#                                 [response.to_dict() for response in filtered_results]
#                             )

#                             new_message = {
#                                 "parentId": parentId,
#                                 "uniqueId": new_uniqueId,
#                                 "message": result_view_blog_str,
#                             }

#                             producer.produce(
#                                 topic="topicA05",
#                                 key=new_uniqueId,
#                                 value=new_message,
#                                 callback=delivery_report,
#                             )
#                 except NoSuchElementException:
#                     # 요소를 찾을 수 없는 경우 그냥 건너뛰기
#                     continue
#         producer.flush()

#     consumer.close()


# if __name__ == "__main__":
#     kafka_topic_03()
