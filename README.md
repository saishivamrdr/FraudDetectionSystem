#  Real-Time Fraud Detection System

A real-time transaction fraud detection system built using
Kafka, Isolation Forest, FastAPI, SQLite and Streamlit.

The system receives transaction data through a Kafka stream,
analyzes transactions using an Isolation Forest anomaly detection
model, calculates a risk score, stores the results in SQLite and
visualizes them through a real-time Streamlit dashboard.

---------------------------------------------------------------------------

## Features

- Real-time transaction streaming using Apache Kafka
- Machine learning based anomaly detection
- Isolation Forest fraud detection model
- Risk scoring from 0 to 100
- Automatic transaction classification
- SQLite transaction storage
- FastAPI backend
- Real-time Streamlit dashboard
- Automatic dashboard refresh
- Model evaluation using precision, recall and F1-score

----------------------------------------------------------------

## System Architecture

```text
Credit Card Dataset
        │
        ▼
 Kafka Producer
        │
        ▼
 Apache Kafka
        │
        ▼
 Kafka Consumer
        │
        ▼
 Isolation Forest
        │
        ▼
 Risk Scoring
        │
        ▼
 SQLite Database
        │
        ▼
 FastAPI
        │
        ▼
 Streamlit Dashboard
 ```
--------------------------------------------------------------------


## System Architecture

![Fraud Detection System Architecture](architecture.png)

--------------------------------------------------------------

## Running the Project with Docker

Building Docker image:

```bash
docker build -t fraud-detection-system .
```
-------------------------------------------------------------