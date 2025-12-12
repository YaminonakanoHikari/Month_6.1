import random
from .redis_client import redis_client

def generate_confirmation_code():
    return str(random.randint(100000, 999999))  # 6-значный код

def save_confirmation_code(user_id, code):
    # Сохраняем код в Redis с TTL 5 минут (300 секунд)
    redis_client.setex(f"confirmation:{user_id}", 300, code)

def verify_confirmation_code(user_id, code):
    key = f"confirmation:{user_id}"
    stored_code = redis_client.get(key)
    if stored_code == code:
        redis_client.delete(key)  # удаляем код сразу после использования
        return True
    return False
