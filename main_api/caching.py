from fastapi import FastAPI, Request, Body, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from fastapi_cache.backends.redis import RedisBackend
import redis.asyncio as aioredis
import json
from hashing import sha256
import redis
import pickle
from config import REDIS_HOST, REDIS_PORT







try:
    redis = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
    # Test connection (optional)
    redis.ping()  # Sends a simple ping command to verify the connection
    print("Connected to Redis successfully")

    # Example: Set and Get values in Redis
    redis.set('test-key', 'test-value')
    value = redis.get('test-key')
    print(f"Value from Redis: {value}")

except Exception as e:
    print(f"Failed to connect to Redis: {e}")





# redis = aioredis.from_url(f"redis://{REDIS_HOST}", encoding="utf8", decode_responses=True)
FastAPICache.init(RedisBackend(redis), prefix="myapp-cache")






# Custom cache key function
async def request_key_builder(func, *args, **kwargs) -> str:
    request = kwargs["request"]
    method = request.method
    
    try:
        body = await request.json()  # Try to get the JSON body
    except Exception:
        body = None  # No body for GET or simple requests

    return make_unique_key(request, body)


def make_unique_key(request, body:dict):

    method = request.method
    
    path = request.url.path
    query_params = str(sorted(request.query_params.items()))  
    

    
    body_str = json.dumps(body, sort_keys=True) if body else ""
    cookies = str(request.cookies)
    headers = str(request.headers.get("Authorization", ""))

    raw_key = f"{method}|{path}|{query_params}|{body_str}|{cookies}|{headers}"
    

    cache_key = sha256(raw_key)
    
    return cache_key



def getCache(request, body:dict):
    unique_key = make_unique_key(request, body)
    data = r.get(unique_key)
    return data

class redis_coder:
    def encode(value):
        return pickle.dumps(value)

    def decode(value):
        return pickle.loads(value)
    
