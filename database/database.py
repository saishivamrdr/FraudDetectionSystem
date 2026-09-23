import sqlite3
from pathlib import Path
from datetime import datetime


DATABASE_PATH = Path(__file__).resolve().parent / "transactions.db"


def create_database():
    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            amount REAL,
            risk_score INTEGER,
            decision TEXT,
            anomaly_score REAL
        )
    """)

    connection.commit()
    connection.close()


def save_transaction(amount, risk_score, decision, anomaly_score):

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO transactions
        (timestamp, amount, risk_score, decision, anomaly_score)
        VALUES (?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        amount,
        risk_score,
        decision,
        anomaly_score
    ))

    connection.commit()
    connection.close()