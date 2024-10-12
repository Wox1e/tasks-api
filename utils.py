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




#NOTES ABOUT TOKEN SYSTEM
#exists two tokens: authorization_key, user_token
# user_token sends to user
# both keys stored in key - value redis:
# user_token -> authorization_key (user_token is the key to authorization_key)




def check_authorization_key(key) -> int:

    if not key:
        raise AuthError

    id = User.check_token(key)
    if id == -1:
        raise AuthError
    
    return id
    
def getUserToken(body:dict, request:Request):

    if "token" in body.keys():
        token = body["token"]
    else:
        token = request.cookies.get("token")
    return token


def get_authorization_key(userToken:str) -> str:


    if userToken != None:
        authToken = redis.get(userToken)
    else:
        return None
    
    return authToken


def Authorization(body:dict, request:Request) -> int:
    user_token = getUserToken(body, request)
    authorization_key = get_authorization_key(user_token)
    id = check_authorization_key(authorization_key)
    return id


def generateToken():
    random_string = random.getrandbits(28)
    hash = sha256(str(random_string))
    while(hash in redis.keys()):
        random_string = random.getrandbits(28)
        hash = sha256(str(random_string))

    return hash
