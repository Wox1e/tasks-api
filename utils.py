from db import User
from fastapi import Request
from caching import redis
import random
from hashing import sha256

def isCookieAllowed(body:dict) -> bool:
    try:
        cookieAllow = body["cookie"]
        if type(cookieAllow) != bool: return False
        return cookieAllow
    except:
        return False
    


class AuthError(Exception):
    msg:str = "Bad token or missing token"

def tokenAuth(token) -> int:


    if not token:
        raise AuthError

    id = User.check_token(token)
    if id == -1:
        raise AuthError
    

    return id
    
def getToken(body:dict, request:Request):

    if "token" in body.keys():
        token = body["token"]
    else:
        token = request.cookies.get("token")

    if token != None:
        authToken = redis.get(token)
    else:
        return None
    
    return authToken

def generateToken():
    random_string = random.getrandbits(28)
    hash = sha256(str(random_string))
    while(hash in redis.keys()):
        random_string = random.getrandbits(28)
        hash = sha256(str(random_string))

    return hash
