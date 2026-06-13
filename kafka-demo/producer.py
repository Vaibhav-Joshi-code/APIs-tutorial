from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

events = [
    {"event": "ride_booked",   "user": "Rahul",  "from": "Connaught Place", "to": "Airport"},
    {"event": "ride_booked",   "user": "Priya",  "from": "Lajpat Nagar",   "to": "Select City Walk"},
    {"event": "ride_cancelled","user": "Amit",   "from": "Dwarka",          "to": "Gurgaon"},
    {"event": "ride_completed","user": "Rahul",  "from": "Connaught Place", "to": "Airport"},
    {"event": "payment_done",  "user": "Rahul",  "amount": 450, "method": "UPI"},
]

print("Producer started — sending messages to Kafka...\n")

for event in events:
    producer.send('ride-events', value=event)
    print(f"Sent → {event}")
    time.sleep(1)

producer.flush()
print("\nAll messages sent!")