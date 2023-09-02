# from confluent_kafka import Consumer, KafkaError


# def kafka_consumer():
#     config = {
#         "bootstrap.servers": "localhost:9092",
#         "group.id": "my-group",
#         "auto.offset.reset": "earliest",
#     }

#     consumer = Consumer(config)
#     consumer.subscribe(["test"])

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

#         msg_key = msg.key().decode("utf-8") if msg.key() else "None"
#         msg_value = msg.value().decode("utf-8")
#         print(f"Received: key={msg_key}, value={msg_value}")

#         try:
#             prefix, numbers_str = msg_value.split(":")
#             if prefix == "INPUT":
#                 num1_str, num2_str = numbers_str.split(",")
#                 num1 = int(num1_str)
#                 num2 = int(num2_str)
#                 total = num1 + num2
#                 print(f"Sum: {total}")
#             elif prefix == "OUTPUT":  # 이 부분을 추가
#                 print(f"Received output: {numbers_str}")
#             else:
#                 print("Invalid prefix")
#         except ValueError:
#             print("Invalid message format")

#     consumer.close()

from confluent_kafka import Consumer, KafkaError
from .naver_tab_service import main


def kafka_consumer(app):
    config = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "my-group",
        "auto.offset.reset": "earliest",
    }

    consumer = Consumer(config)
    consumer.subscribe(["test-topic"])

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
                    main(query)
            elif prefix == "OUTPUT":
                print(f"Received output: {query}")
            else:
                print("Invalid prefix")
        except ValueError:
            print("Invalid message format")

    consumer.close()


if __name__ == "__main__":
    kafka_consumer()
