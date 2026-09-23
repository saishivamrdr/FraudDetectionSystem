from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import sqlite3
from pathlib import Path
from database.database import create_database, save_transaction



app = FastAPI(title="Real-Time Fraud Detection API")

create_database()

# Load trained model
bundle = joblib.load("model/fraud_model.pkl")

model = bundle["model"]
scaler = bundle["scaler"]
features = bundle["features"]


class Transaction(BaseModel):
    Time: float
    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float
    Amount: float


@app.get("/")
def root():
    return {
        "message": "Fraud Detection API is running"
    }


@app.post("/predict")
def predict(transaction: Transaction):

    data = transaction.model_dump()

    X = pd.DataFrame([data])[features]

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
        amount=transaction.Amount,
        risk_score=risk_score,
        decision=decision,
        anomaly_score=float(anomaly_score)
    )

    return {
        "risk_score": risk_score,
        "decision": decision,
        "anomaly_score": float(anomaly_score)
    }
DATABASE_PATH = Path(__file__).resolve().parents[1] / "database" / "transactions.db"


@app.get("/transactions")
def get_transactions():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            timestamp,
            amount,
            risk_score,
            decision,
            anomaly_score
        FROM transactions
        ORDER BY id DESC
    """)

    transactions = [dict(row) for row in cursor.fetchall()]

    connection.close()

    return {
        "transactions": transactions
    }


@app.get("/stats")
def get_stats():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM transactions")
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM transactions
        WHERE decision = 'SUSPICIOUS'
    """)
    suspicious = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM transactions
        WHERE decision = 'REVIEW'
    """)
    review = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM transactions
        WHERE decision = 'NORMAL'
    """)
    normal = cursor.fetchone()[0]

    connection.close()

    return {
        "total": total,
        "suspicious": suspicious,
        "review": review,
        "normal": normal
    }