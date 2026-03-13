# producer_taxi.py
from kafka import KafkaProducer
from generation import generate_message

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: v.encode('utf-8')
)

topic = 'taxi_platform'

if __name__ == "__main__":
    for _ in range(5):  
        msg = generate_message()
        print("Sending:", msg)
        producer.send(topic, msg)
        producer.flush()