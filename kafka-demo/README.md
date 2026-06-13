# 🚀 Kafka Architecture Demo — Beginner to Advanced

![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-231F20?logo=apachekafka&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Required-2496ED?logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)
![Confluent](https://img.shields.io/badge/Confluent-Kafka%207.5-CC0000?logo=confluent&logoColor=white)

A hands-on Kafka demo that teaches **Producer → Broker → Consumer** flow with real-world analogies — the same architecture used by **Uber, Netflix, and Amazon** to process millions of events per second.

---

## 🧠 What You Will Learn

| Concept | What This Demo Shows |
|---|---|
| **Producer** | Python script sending ride events to Kafka |
| **Broker** | Confluent Kafka running inside Docker |
| **Topic** | `ride-events` — named channel for messages |
| **Partition** | Which partition each message lands on |
| **Offset** | Exact position of each message — `Offset 0, 1, 2...` |
| **Consumer** | Python script reading messages in real time |
| **Consumer Group** | Two independent groups reading the same topic |
| **Replication** | Fault tolerance config in `docker-compose.yml` |

---

## 🗂️ Project Structure

```
kafka-demo/
├── docker-compose.yml    ← ZooKeeper + Kafka broker setup
├── producer.py           ← Sends 5 ride events to Kafka
├── consumer.py           ← notification-service group reader
├── consumer2.py          ← analytics-service group reader
└── README.md
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        KAFKA CLUSTER                             │
│                                                                  │
│   ┌──────────────────────────────────────────────────────────┐  │
│   │               ZooKeeper (Port 2181)                       │  │
│   │          Cluster Coordinator — Leader Election            │  │
│   └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│   ┌──────────────────────────────────────────────────────────┐  │
│   │               Kafka Broker (Port 9092)                    │  │
│   │                                                           │  │
│   │   Topic: "ride-events"                                    │  │
│   │   ┌─────────────┐                                         │  │
│   │   │ Partition 0 │  [Offset 0] [Offset 1] [Offset 2] ...  │  │
│   │   └─────────────┘                                         │  │
│   └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
         ↑                                        ↓
   producer.py                         consumer.py  (notification-service)
   (sends events)                      consumer2.py (analytics-service)
```

**Key insight:** Both consumer groups read the **same messages independently** — Producer sends once, multiple groups consume at their own pace.

---

## ⚙️ Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and **running**
- Python 3.8+
- `kafka-python` library

**Verify Docker:**
```powershell
docker --version
docker-compose --version
```

**Install Python library:**
```powershell
pip install kafka-python
```

---

## 🚀 Running the Demo

### Step 1 — Start Kafka + ZooKeeper

```powershell
docker-compose up -d
```

Expected output:
```
Container zookeeper   Started ✅
Container kafka       Started ✅
```

Verify both containers are running:
```powershell
docker ps
```

```
CONTAINER ID   IMAGE                        STATUS
xxxx           confluentinc/cp-kafka:7.5.0  Up 30 seconds
xxxx           confluentinc/cp-zookeeper    Up 32 seconds
```

> ⚠️ **Wait 15-20 seconds** after containers start before running Python scripts. Kafka needs a moment to fully initialize.

---

### Step 2 — Start the Consumer (Terminal 1)

Open a terminal and run:

```powershell
python consumer.py
```

You will see:
```
Consumer started — waiting for messages...
```

Consumer is now **listening** on topic `ride-events` as `notification-service` group. Keep this terminal open.

---

### Step 3 — Run the Producer (Terminal 2)

Open a **second terminal** and run:

```powershell
python producer.py
```

Producer output:
```
Producer started — sending messages to Kafka...

Sent → {'event': 'ride_booked', 'user': 'Rahul', 'from': 'Connaught Place', 'to': 'Airport'}
Sent → {'event': 'ride_booked', 'user': 'Priya', 'from': 'Lajpat Nagar', 'to': 'Select City Walk'}
Sent → {'event': 'ride_cancelled', 'user': 'Amit', 'from': 'Dwarka', 'to': 'Gurgaon'}
Sent → {'event': 'ride_completed', 'user': 'Rahul', 'from': 'Connaught Place', 'to': 'Airport'}
Sent → {'event': 'payment_done', 'user': 'Rahul', 'amount': 450, 'method': 'UPI'}

All messages sent!
```

---

### Step 4 — Watch Consumer Terminal (Terminal 1)

Switch back to Terminal 1 — messages arrive in **real time**:

```
Received from Partition 0 | Offset 0
Event: {'event': 'ride_booked', 'user': 'Rahul', 'from': 'Connaught Place', 'to': 'Airport'}

Received from Partition 0 | Offset 1
Event: {'event': 'ride_booked', 'user': 'Priya', 'from': 'Lajpat Nagar', 'to': 'Select City Walk'}

Received from Partition 0 | Offset 2
Event: {'event': 'ride_cancelled', 'user': 'Amit', 'from': 'Dwarka', 'to': 'Gurgaon'}

Received from Partition 0 | Offset 3
Event: {'event': 'ride_completed', 'user': 'Rahul', 'from': 'Connaught Place', 'to': 'Airport'}

Received from Partition 0 | Offset 4
Event: {'event': 'payment_done', 'user': 'Rahul', 'amount': 450, 'method': 'UPI'}
```

> **Notice:** `Offset 0, 1, 2, 3, 4` — Kafka automatically assigned sequential numbers. This is how consumers track their position.

---

## 🧪 Consumer Group Demo

This demonstrates that **multiple independent services** can consume the same messages from the same topic.

### Step 1 — Open a third terminal and run:

```powershell
python consumer2.py
```

Output:
```
Analytics Service Consumer started — reading from beginning...

Received from Partition 0 | Offset 0
Event: {'event': 'ride_booked', 'user': 'Rahul', ...}

Received from Partition 0 | Offset 1
Event: {'event': 'ride_booked', 'user': 'Priya', ...}
...
```

> **Key observation:** `consumer2.py` reads **all 5 messages from the beginning** — even though `consumer.py` already consumed them. This is because they belong to **different Consumer Groups** (`notification-service` vs `analytics-service`).

### Why This Matters

```
Topic: "ride-events"
    │
    ├── Consumer Group: "notification-service"   → Sends SMS/email to rider
    ├── Consumer Group: "analytics-service"      → Stores data for dashboard
    └── Consumer Group: "fraud-detection"        → Checks for suspicious patterns
                                                   (add consumer3.py yourself!)
```

Producer sent **once** — three services consumed **independently**. This is the exact pattern Uber uses for every ride booking.

---

## 📄 File Breakdown

### `docker-compose.yml`

```yaml
version: "3.9"

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    container_name: zookeeper
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    container_name: kafka
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: "true"
```

| Config | Purpose |
|---|---|
| `KAFKA_BROKER_ID: 1` | Unique ID for this broker in the cluster |
| `KAFKA_ZOOKEEPER_CONNECT` | Kafka registers itself with ZooKeeper on startup |
| `KAFKA_ADVERTISED_LISTENERS` | Address Python clients use to connect |
| `KAFKA_AUTO_CREATE_TOPICS_ENABLE` | Topic `ride-events` is auto-created on first use |
| `KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1` | Single broker demo — no replication needed |

---

### `producer.py`

```python
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
```

| Line | What it does |
|---|---|
| `bootstrap_servers` | Address of Kafka broker to connect to |
| `value_serializer` | Converts Python dict → JSON bytes (Kafka stores bytes) |
| `producer.send('ride-events', value=event)` | Sends to topic named `ride-events` |
| `time.sleep(1)` | 1 second gap — so consumer receives messages one by one visibly |
| `producer.flush()` | Ensures all buffered messages are actually sent before script exits |

---

### `consumer.py`

```python
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
```

| Config | Purpose |
|---|---|
| `auto_offset_reset='earliest'` | If no prior offset exists, read from beginning of topic |
| `group_id='notification-service'` | Consumer group name — Kafka tracks offset per group |
| `value_deserializer` | Converts JSON bytes back to Python dict |
| `message.partition` | Which partition this message came from |
| `message.offset` | Sequential position of this message in the partition |

---

### `consumer2.py`

Identical to `consumer.py` with two differences:

```python
group_id='analytics-service',    # Different group — independent offset tracking
# print label changed to identify which consumer is running
```

This single change means Kafka treats it as a completely separate consumer — it gets its own offset pointer and reads all messages from the start independently.

---

## 🔍 Verify Inside Kafka Container

List all topics:
```powershell
docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --list
```

Output:
```
ride-events
__consumer_offsets
```

Describe topic — see partition and replication details:
```powershell
docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --describe --topic ride-events
```

Output:
```
Topic: ride-events   Partitions: 1   ReplicationFactor: 1
  Partition: 0   Leader: 1   Replicas: 1   Isr: 1
```

List consumer groups:
```powershell
docker exec -it kafka kafka-consumer-groups --bootstrap-server localhost:9092 --list
```

Output:
```
notification-service
analytics-service
```

Check offset progress for a group:
```powershell
docker exec -it kafka kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group notification-service
```

Output:
```
GROUP                TOPIC        PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG
notification-service ride-events  0          5               5               0
```

> `LAG: 0` means the consumer has read all available messages — no backlog.

---

## 🐛 Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `NoBrokersAvailable` error | Kafka not ready yet | Wait 20 seconds after `docker-compose up`, then retry |
| Consumer shows no messages | `auto_offset_reset` issue | Ensure `auto_offset_reset='earliest'` in consumer |
| `kafka-python` not found | Library not installed | Run `pip install kafka-python` |
| Port 9092 already in use | Another Kafka instance running | Run `docker ps` — stop conflicting container |
| Messages received but garbled | Serializer mismatch | Ensure both producer and consumer use same JSON serializer/deserializer |
| `docker-compose: command not found` | Older Docker version | Use `docker compose up -d` (no hyphen) |

---

## 🛑 Stop and Cleanup

Stop containers (keeps data):
```powershell
docker-compose down
```

Stop and remove all data (full reset):
```powershell
docker-compose down -v
```

> Use `down -v` if you want a completely fresh Kafka state for the next demo run.

---

## 💡 Real World Connection

| This Demo | Uber / Netflix / Amazon |
|---|---|
| `producer.py` sending 5 events | Millions of events per second |
| Single Kafka broker in Docker | Hundreds of brokers in clusters globally |
| `ride-events` topic | Thousands of topics per service |
| 1 partition | Hundreds of partitions per topic for parallelism |
| 2 consumer groups | Dozens of microservices consuming same topics |
| `replication-factor=1` | `replication-factor=3` — survives 2 broker failures |
| Manual `docker-compose up` | Kubernetes-managed, auto-scaling clusters |

---

## 📚 Concepts Covered

- **Producer** — Publishes messages to a topic; fire-and-forget pattern
- **Broker** — Stores messages on disk; default retention 7 days
- **Topic** — Named channel; logical grouping of related events
- **Partition** — Ordered, immutable log within a topic; enables parallelism
- **Offset** — Sequential message number within a partition; consumer's bookmark
- **Consumer** — Reads messages from a topic; stateless processing
- **Consumer Group** — Multiple consumers sharing work; each partition assigned to one consumer
- **ZooKeeper** — Coordinates broker metadata and leader election (being replaced by KRaft in Kafka 3.x+)

