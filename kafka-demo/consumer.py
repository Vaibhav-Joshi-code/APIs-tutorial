from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'ride-events',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='notification-service',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

print("Consumer started — waiting for messages...\n")

for message in consumer:
    event = message.value
    print(f"Received from Partition {message.partition} | Offset {message.offset}")
    print(f"Event: {event}\n")