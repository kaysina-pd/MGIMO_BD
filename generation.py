import random
import json
from faker import Faker

fake = Faker()
drivers = ['Ivan Petrov', 'Anna Sidorova', 'Sergey Kuznetsov', 'Olga Smirnova']
cars = ['Toyota Camry', 'Hyundai Solaris', 'Kia Rio', 'Lada Vesta']
tariffs = ['Economy', 'Comfort', 'Business']
ratings = [1, 2, 3, 4, 5]

def generate_message():
    message = {
        "client_id": fake.uuid4(),
        "client_name": fake.name(),
        "driver_name": random.choice(drivers),
        "car": random.choice(cars),
        "trip_id": fake.uuid4(),
        "tariff": random.choice(tariffs),
        "price": random.randint(-3, 10),
        "rating": random.randint(-10, 5),
    }

    return json.dumps(message)