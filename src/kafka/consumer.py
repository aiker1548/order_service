import json

from aiokafka import AIOKafkaConsumer

from config import config as kafka_config

async def consume_kafka_messages_for_users(correlation_id: str, user_ids: list):
    """Консьюмер для получения пользователей по их ID"""
    consumer = AIOKafkaConsumer(
        kafka_config.response_topic,  # Тема для ответа
        bootstrap_servers=kafka_config.bootstrap_servers,
        group_id=kafka_config.group_id,
        auto_offset_reset=kafka_config.auto_offset_reset
    )
    await consumer.start()

    users_data = {}

    try:
        async for msg in consumer:
            response = json.loads(msg.value.decode("utf-8"))
            if response.get("correlation_id") == correlation_id:
                for user_id, user_info in response.get("users", {}).items():
                    user_id = int(user_id)
                    if user_id in user_ids:
                        users_data[user_id] = user_info
                # Выход после получения всех данных
                if len(users_data) == len(user_ids):
                    break
    finally:
        await consumer.stop()

    return users_data