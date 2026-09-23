import pandas as pd
import joblib

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


# Load dataset
df = pd.read_csv("../data/creditcard.csv")

# Features used by the model
features = [
    "Time",
    "V1", "V2", "V3", "V4", "V5", "V6", "V7",
    "V8", "V9", "V10", "V11", "V12", "V13", "V14",
    "V15", "V16", "V17", "V18", "V19", "V20", "V21",
    "V22", "V23", "V24", "V25", "V26", "V27", "V28",
    "Amount"
]

# Use legitimate transactions for learning normal behaviour
legitimate = df[df["Class"] == 0]

X = legitimate[features]

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Create Isolation Forest model
model = IsolationForest(
    n_estimators=200,
    contamination=0.002,
    random_state=42,
    n_jobs=-1
)

# Train the model
model.fit(X_scaled)

# Save model + scaler + feature names
joblib.dump(
    {
        "model": model,
        "scaler": scaler,
        "features": features
    },
    "fraud_model.pkl"
)

print("Model trained successfully!")
print("Training transactions:", len(X))
print("Model saved as fraud_model.pkl")