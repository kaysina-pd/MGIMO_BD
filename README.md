
# Лабораторная работа 1  
  
Кайсина Полина
Вариант: январь 21-31   
Тема: Заказ такси   
Сущности: Клиенты, водители, автомобили, поездки, тарифы, оплата, оценка поездки   
  
---  

# Последовательность выполнения
  
## 1. Установка Apache Kafka  
  
С официального сайта скачана бинарная версия дистрибутива Apache Kafka 4.2.0 в режиме KRaft (без ZooKeeper). Дистрибутив распакован в корневую папку для удобства запуска.   
  
Последовательность действий для запуска:  
  
1. Инициализация хранилища Kafka (только один раз):  
  

    bat  
    cd C:\path\to\kafka_2.13-4.2.0  
    bin\windows\kafka-storage.bat random-uuid  
    bin\windows\kafka-storage.bat format --standalone -t <UUID> -c config\server.properties

2.  Запуск Kafka-брокера (окно 1):
    

    bin\windows\kafka-server-start.bat config\server.properties

3.  Создание тестового топика (taxi-orders):
    

    bin\windows\kafka-topics.bat --create --topic taxi-orders --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

----------

## 2. Написание скриптов

Скрипты написаны на Python 3 с использованием библиотеки `kafka-python`. Для генерации тестовых сообщений используется отдельный модуль `generation.py`.


### 2.1 Формат сообщения

{  
 "client": "Alex",  
 "driver": "Ivan",  
 "car": "Toyota Prius",  
 "trip_id": 101,  
 "tariff": "Standard",  
 "price": 250,  
 "payment_method": "Card",  
 "rating": 4  
}

### 2.2 Правила валидации (Consumer)

Поле

Условие невалидности

price

<= 0

rating

< 1 или > 5

----------

## 3. Запуск

1.  Установить зависимости Python:
    

python -m venv venv  
venv\Scripts\activate  
pip install -r requirements.txt

2.  Запустить Consumer (окно 2):
    

venv\Scripts\activate  
python consumer.py

3.  Запустить Producer (окно 3):
    

venv\Scripts\activate  
python producer.py

----------

## 4. Пример вывода

**Producer:**

SEND: {"client": "Olga", "driver": "Sergey", "car": "Kia Rio", "trip_id": 201, "tariff": "Economy", "price": 300, "payment_method": "Cash", "rating": 5}  
SEND: {"client": "Petr", "driver": "Ivan", "car": "Hyundai Solaris", "trip_id": 202, "tariff": "Premium", "price": -150, "payment_method": "Card", "rating": 6}  
SEND: {"client": "Anna", "driver": "Dmitry", "car": "Lada Vesta", "trip_id": 203, "tariff": "Standard", "price": 200, "payment_method": "Card", "rating": 4}

**Consumer:**

RECEIVED: {"client": "Olga", "driver": "Sergey", "car": "Kia Rio", "trip_id": 201, "tariff": "Economy", "price": 300, "payment_method": "Cash", "rating": 5}  
NOT VALID: {"client": "Petr", "driver": "Ivan", "car": "Hyundai Solaris", "trip_id": 202, "tariff": "Premium", "price": -150, "payment_method": "Card", "rating": 6}  
RECEIVED: {"client": "Anna", "driver": "Dmitry", "car": "Lada Vesta", "trip_id": 203, "tariff": "Standard", "price": 200, "payment_method": "Card", "rating": 4}

----------

## 5. Результат работы

Consumer успешно принимает все сообщения из Kafka-топика, проверяет их на соответствие правилам валидации и выводит на консоль как валидные (`RECEIVED`), так и невалидные (`NOT VALID`) сообщения.  
Таким образом, демонстрируется полный цикл потоковой обработки данных для платформы заказа такси.

