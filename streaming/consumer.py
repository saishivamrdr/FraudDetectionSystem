from kafka import KafkaConsumer
import pandas as pd
import joblib
import json
from pathlib import Path

from database.database import save_transaction

ROOT = Path(__file__).resolve().parents[1]

bundle = joblib.load(ROOT / "model" / "fraud_model.pkl")

model = bundle["model"]
scaler = bundle["scaler"]
features = bundle["features"]

consumer = KafkaConsumer(
    "fraud-transactions",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="fraud-detector",
    value_deserializer=lambda value: json.loads(value.decode("utf-8"))
)

print("Kafka Consumer started...")
print("Waiting for transactions...\n")

for transaction in consumer:

    data = transaction.value

    X = pd.DataFrame(
        [[data[feature] for feature in features]],
        columns=features
    )

    X_scaled = scaler.transform(X)

    prediction = model.predict(X_scaled)[0]
    anomaly_score = model.decision_function(X_scaled)[0]

    if prediction == -1:
        risk_score = int(70 + (-anomaly_score * 100))
    else:
        risk_score = int(30 - (anomaly_score * 50))

    risk_score = max(0, min(100, risk_score))

    if risk_score >= 70:
        decision = "SUSPICIOUS"
    elif risk_score >= 30:
        decision = "REVIEW"
    else:
        decision = "NORMAL"

    save_transaction(
        amount=data["Amount"],
        risk_score=risk_score,
        decision=decision,
        anomaly_score=float(anomaly_score)
    )

    print("--------------------------------")
    print("Transaction received")
    print("Amount:", data["Amount"])
    print("Risk score:", risk_score)
    print("Decision:", decision)
    print("Anomaly score:", anomaly_score)