from fastapi import Body, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from fastapi_cache.backends.redis import RedisBackend
import json
from hashing import sha256
import redis
from config import REDIS_HOST, REDIS_PORT
import jsonpickle

try:
    redis = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
    redis.ping()
    print("Connected to Redis successfully")
    redis.set('test', 'test')
    value = redis.get('test')
    print(f"Data from Redis: {value}")
except Exception as e:
    print(f"Failed to connect to Redis: {e}")



FastAPICache.init(RedisBackend(redis), prefix="main_api-cache")



# Custom cache key function
async def request_key_builder(func, *args, **kwargs) -> str:

    request = kwargs["request"]
    method = request.method

    try:
        body = await request.json()
    except Exception:
        body = None

    return make_unique_key(request, body)


def make_unique_key(request, body:dict):
    """
    Builds a unique key of request (based on its parametrs)
    
    """

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
    """
    Returns data from the cache (based on request parameters)
    
    """
    unique_key = make_unique_key(request, body)
    data = redis.get(unique_key)

    if data == None: return None

    data = jsonpickle.decode(data)

    return data

class redis_coder:
    """
    Coder for @cache decocator
    
    """
    @classmethod
    def encode(cls, value):
        return jsonpickle.encode(value)

    @classmethod
    def decode(cls, value):
        return jsonpickle.decode(value)
    


