import pandas as pd
import joblib

from pathlib import Path
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split


ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(ROOT / "data" / "creditcard.csv")

features = [
    "Time",
    "V1", "V2", "V3", "V4", "V5", "V6", "V7",
    "V8", "V9", "V10", "V11", "V12", "V13", "V14",
    "V15", "V16", "V17", "V18", "V19", "V20", "V21",
    "V22", "V23", "V24", "V25", "V26", "V27", "V28",
    "Amount"
]


legitimate = df[df["Class"] == 0]
fraud = df[df["Class"] == 1]

train_legitimate, test_legitimate = train_test_split(
    legitimate,
    test_size=0.20,
    random_state=42
)

test_data = pd.concat([
    test_legitimate,
    fraud
]).sample(
    frac=1,
    random_state=42
)


X_train = train_legitimate[features]

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

model = IsolationForest(
    n_estimators=200,
    contamination=0.002,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train_scaled)


X_test = test_data[features]
y_test = test_data["Class"]

X_test_scaled = scaler.transform(X_test)

predictions = model.predict(X_test_scaled)

predictions = (predictions == -1).astype(int)


print("========== PROPER MODEL EVALUATION ==========\n")

print("Training legitimate transactions:", len(train_legitimate))
print("Test legitimate transactions:", len(test_legitimate))
print("Test fraud transactions:", len(fraud))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions,
        target_names=["Legitimate", "Fraud"],
        zero_division=0
    )
)

print("\nTotal test transactions:", len(test_data))
print("Actual fraud transactions:", int(y_test.sum()))
print("Detected fraud transactions:", int(predictions.sum()))