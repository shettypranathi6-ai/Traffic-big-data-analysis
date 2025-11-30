# 🚦 Real-Time Traffic Analysis with Apache Kafka & Streamlit

A real-time Big Data pipeline that monitors traffic conditions at specific junctions (currently configured for **Silk Board Junction, Bangalore**). The system fetches live traffic flow data from the TomTom API, streams it through **Apache Kafka**, and visualizes real-time metrics and trends using a **Streamlit** dashboard.

## 🏗 Architecture



The project follows a Producer-Consumer architecture:
1.  **Data Source:** **TomTom Traffic API** provides real-time speed and congestion data.
2.  **Producer:** A Python script (`producer.py`) polls the API every 60 seconds and pushes JSON data to a **Kafka Topic** (`traffic_data`).
3.  **Message Broker:** **Apache Kafka** (managed via Zookeeper) acts as the high-throughput buffer for the data stream.
4.  **Consumer/Dashboard:** **Streamlit** (`dashboard.py`) consumes messages from Kafka, processes the data, and updates a live interactive dashboard.

## 🛠 Tech Stack

* **Language:** Python 3.9
* **Message Broker:** Apache Kafka & Zookeeper
* **Visualization:** Streamlit, Plotly Express
* **Containerization:** Docker & Docker Compose
* **Data Processing:** Pandas
* **External API:** TomTom Maps API

## 📂 Project Structure

```text
TrafficBigData/
├── dashboard.py         # Streamlit frontend (Kafka Consumer)
├── producer.py          # Data ingestion script (Kafka Producer)
├── docker-compose.yml   # Orchestration for Kafka, Zookeeper, and App
├── Dockerfile           # Environment definition for the Python app
├── requirements.txt     # Python dependencies
├── .env                 # API Keys (Not included in repo)
└── README.md            # Project documentation
