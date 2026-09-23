import joblib
import pandas as pd

# Load trained model
bundle = joblib.load("fraud_model.pkl")

model = bundle["model"]
scaler = bundle["scaler"]
features = bundle["features"]

# Load dataset
df = pd.read_csv("../data/creditcard.csv")

# Find one legitimate transaction
normal_transaction = df[df["Class"] == 0].iloc[0]

# Find one fraud transaction
fraud_transaction = df[df["Class"] == 1].iloc[0]


def predict_transaction(transaction):

    X = pd.DataFrame(
        [[transaction[feature] for feature in features]],
        columns=features
    )

    X_scaled = scaler.transform(X)

    prediction = model.predict(X_scaled)[0]
    anomaly_score = model.decision_function(X_scaled)[0]

    print("\n----------------------------")
    print("Actual class:", transaction["Class"])
    print("Prediction:", prediction)
    print("Anomaly score:", anomaly_score)

    if prediction == -1:
        print("🚨 SUSPICIOUS")
    else:
        print("✅ NORMAL")


predict_transaction(normal_transaction)
predict_transaction(fraud_transaction)