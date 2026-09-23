import pandas as pd
import requests
import time


API_URL = "http://127.0.0.1:8000/predict"

features = [
    "Time",
    "V1", "V2", "V3", "V4", "V5", "V6", "V7",
    "V8", "V9", "V10", "V11", "V12", "V13", "V14",
    "V15", "V16", "V17", "V18", "V19", "V20", "V21",
    "V22", "V23", "V24", "V25", "V26", "V27", "V28",
    "Amount"
]


df = pd.read_csv("../data/creditcard.csv")


for index, transaction in df.head(20).iterrows():

    data = {
        feature: float(transaction[feature])
        for feature in features
    }

    response = requests.post(API_URL, json=data)

    result = response.json()

    print("--------------------------------")
    print("Transaction:", index)
    print("Amount:", transaction["Amount"])
    print("Actual class:", transaction["Class"])
    print("Risk score:", result["risk_score"])
    print("Decision:", result["decision"])

    time.sleep(1)