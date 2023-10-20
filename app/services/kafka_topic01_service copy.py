# from confluent_kafka import Consumer, Producer, KafkaError
# from confluent_kafka.avro import AvroConsumer, AvroProducer
# from confluent_kafka.avro.serializer import SerializerError
# from avro.schema import parse
# import json
# import uuid
# from .keyword_service import main as keyword_main
# from .keyword_shopping_service import main as keyword_shopping_main
# from .keyword_google_service import main as keyword_google_main
# from .naver_tab_service import main


# def kafka_topic_01(app):
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

#     consumer.subscribe(["topicA01"])

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
#         new_uniqueId = str(uuid.uuid4())

#         query = msg_value["message"]

#         print("check point 1: " + query)

#         with app.app_context():
#             keyword_list = keyword_main(query)
#             keyword_shopping_list = keyword_shopping_main(query)
#             keyword_google = keyword_google_main(query)
#             result = (
#                 (query or "")
#                 + (keyword_list or "")
#                 + (keyword_shopping_list or "")
#                 + (keyword_google or "")
#             )

#             print("check point 2: " + result)

#             result_list_json = json.dumps(result, ensure_ascii=False)

#             new_message = {
#                 "parentId": parentId,
#                 "uniqueId": new_uniqueId,
#                 "message": result_list_json,
#             }

#             producer.produce(
#                 topic="topicA02", key=new_uniqueId, value=new_message, callback=delivery_report
#             )
#             producer.flush()

#     consumer.close()


# if __name__ == "__main__":
#     kafka_consumer()
