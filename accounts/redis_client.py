# accounts/redis_client.py
import redis
from django.conf import settings

redis_client = redis.Redis(
    host='localhost',  # или settings.REDIS_HOST
    port=6379,         # или settings.REDIS_PORT
    db=0,
    decode_responses=True
)
