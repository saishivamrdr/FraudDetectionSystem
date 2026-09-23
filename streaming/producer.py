from kafka import KafkaProducer
import pandas as pd
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

features = [
    "Time",
    "V1", "V2", "V3", "V4", "V5", "V6", "V7",
    "V8", "V9", "V10", "V11", "V12", "V13", "V14",
    "V15", "V16", "V17", "V18", "V19", "V20", "V21",
    "V22", "V23", "V24", "V25", "V26", "V27", "V28",
    "Amount"
]

df = pd.read_csv(ROOT / "data" / "creditcard.csv")

normal = df[df["Class"] == 0].sample(n=45, random_state=42)
fraud = df[df["Class"] == 1].sample(n=5, random_state=42)

demo_data = pd.concat([normal, fraud]).sample(
    frac=1,
    random_state=42
)

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)

print("Kafka Producer started...")
print("Sending transactions...\n")

for index, transaction in demo_data.iterrows():

    data = {
        feature: float(transaction[feature])
        for feature in features
    }

    producer.send(
        "fraud-transactions",
        value=data
    )

    producer.flush()

    print("--------------------------------")
    print("Transaction:", index)
    print("Actual class:", int(transaction["Class"]))
    print("Amount:", transaction["Amount"])
    print("Sent to Kafka")

    time.sleep(1)

producer.close()

print("\nAll transactions sent successfully!")