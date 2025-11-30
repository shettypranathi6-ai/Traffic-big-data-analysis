import time
import json
import requests
import os
from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv()

print("Waiting for Kafka to start...")
time.sleep(30) 

def get_producer():
    try:
        return KafkaProducer(
            bootstrap_servers=['kafka:29092'],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
    except Exception as e:
        print(f"Error connecting to Kafka: {e}")
        return None

producer = get_producer()

API_KEY = os.getenv("TOMTOM_API_KEY")
if not API_KEY:
    print("ERROR: TOMTOM_API_KEY not found in .env file")
    exit(1)

# Silk Board Junction, Bangalore (Change if you want!)
LAT = "12.9175"
LON = "77.6236"
URL = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key={API_KEY}&point={LAT},{LON}"

print("Starting Traffic Data Stream...")

while True:
    if producer:
        try:
            response = requests.get(URL)
            if response.status_code == 200:
                data = response.json()
                if 'flowSegmentData' in data:
                    traffic_info = {
                        "road_name": "Silk Board Junction",
                        "current_speed": data['flowSegmentData']['currentSpeed'],
                        "free_flow_speed": data['flowSegmentData']['freeFlowSpeed'],
                        "confidence": data['flowSegmentData']['confidence'],
                        "timestamp": time.time()
                    }
                    producer.send('traffic_data', value=traffic_info)
                    print(f"Sent: {traffic_info}")
            else:
                print(f"API Error: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        producer = get_producer()
    
    time.sleep(60)