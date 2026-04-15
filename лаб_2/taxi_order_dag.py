from __future__ import annotations

import json
import os
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from generation import generate_message

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
MESSAGE_FILE = os.path.join(DATA_DIR, "taxi_messages.json")
VALIDATED_FILE = os.path.join(DATA_DIR, "taxi_validated.json")


def ensure_data_dir() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)


def generate_taxi_messages() -> None:
    """Генерирует тестовые сообщения заказа такси и сохраняет их в локальный JSON-файл."""
    ensure_data_dir()
    messages = [json.loads(generate_message()) for _ in range(10)]
    with open(MESSAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)


def validate_message(message: dict) -> bool:
    """Проверяет сообщение на валидность по правилам проекта."""
    required_keys = [
        "client_id",
        "client_name",
        "driver_name",
        "car",
        "trip_id",
        "tariff",
        "price",
        "rating",
    ]
    for key in required_keys:
        if key not in message:
            return False

    if not isinstance(message["price"], (int, float)) or message["price"] <= 0:
        return False

    if not isinstance(message["rating"], int) or not (1 <= message["rating"] <= 5):
        return False

    return True


def consume_and_validate() -> None:
    """Считывает сообщения из файла, выполняет валидацию и сохраняет результат."""
    ensure_data_dir()

    with open(MESSAGE_FILE, "r", encoding="utf-8") as f:
        messages = json.load(f)

    results = []
    for message in messages:
        is_valid = validate_message(message)
        results.append({
            "message": message,
            "valid": is_valid,
        })

    with open(VALIDATED_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


def archive_results() -> None:
    """Создает простую сводку по валидации для отчета DAG."""
    with open(VALIDATED_FILE, "r", encoding="utf-8") as f:
        validated_data = json.load(f)

    total = len(validated_data)
    valid_count = sum(1 for item in validated_data if item["valid"])
    invalid_count = total - valid_count

    summary = {
        "total_messages": total,
        "valid_messages": valid_count,
        "invalid_messages": invalid_count,
    }

    summary_file = os.path.join(DATA_DIR, "taxi_validation_summary.json")
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)


def print_summary() -> None:
    """Печатает краткий отчет по результатам валидации."""
    summary_file = os.path.join(DATA_DIR, "taxi_validation_summary.json")
    with open(summary_file, "r", encoding="utf-8") as f:
        summary = json.load(f)

    print("Taxi DAG summary:")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


with DAG(
    dag_id="taxi_order_pipeline",
    description="DAG для обработки заказа такси: генерация, валидация и сохранение результатов.",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["taxi", "validation"],
) as dag:

    task_generate_messages = PythonOperator(
        task_id="generate_taxi_messages",
        python_callable=generate_taxi_messages,
    )

    task_consume_and_validate = PythonOperator(
        task_id="consume_and_validate_messages",
        python_callable=consume_and_validate,
    )

    task_archive_results = PythonOperator(
        task_id="archive_validation_results",
        python_callable=archive_results,
    )

    task_print_summary = PythonOperator(
        task_id="print_validation_summary",
        python_callable=print_summary,
    )

    task_generate_messages >> task_consume_and_validate >> task_archive_results >> task_print_summary
