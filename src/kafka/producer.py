import json
import uuid

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from config import config as kafka_config

async def send_user_ids_to_kafka(user_ids: list):
    """Отправляем запрос с уникальным идентификатором и ID пользователей"""
    correlation_id = str(uuid.uuid4())  # Генерируем уникальный идентификатор для запроса
    request_data = {
        "correlation_id": correlation_id,
        "user_ids": user_ids
    }

    producer = AIOKafkaProducer(bootstrap_servers=kafka_config.bootstrap_servers)
    await producer.start()
    try:
        await producer.send_and_wait(
            kafka_config.request_topic,
            json.dumps(request_data).encode("utf-8")
        )
    finally:
        await producer.stop()

    return correlation_id
