# consumer_taxi.py
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'taxi_platform',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='taxi-consumers',
    value_deserializer=lambda v: v.decode('utf-8')
)

def validate_message(msg):
    try:
        data = json.loads(msg)
        required_keys = ["client_id", "client_name", "driver_name", "car", "trip_id", "tariff", "price", "rating"]

        for key in required_keys:
            if key not in data:
                return False
        if not (isinstance(data["price"], (int, float)) and data["price"] > 0):
            return False
        if not (1 <= data["rating"] <= 5):
            return False

        return True
    except:
        return False

if __name__ == "__main__":
    for message in consumer:
        msg = message.value
        if validate_message(msg):
            print("VALID:", msg)
        else:
            print("NOT VALID:", msg)