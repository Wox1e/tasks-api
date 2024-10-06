from db import User
from fastapi import Request

def isCookieAllowed(body:dict) -> bool:
    try:
        cookieAllow = body["cookie"]
        if type(cookieAllow) != bool: return False
        return cookieAllow
    except:
        return False
    


class AuthError(Exception):
    msg:str = "Bad token or missing token"

def tokenAuth(body:dict, request:Request) -> int:

    if "token" in body.keys():
        token = body["token"]
    else:
        token = request.cookies.get("token")

    if not token:
        raise AuthError

    id = User.check_token(token)
    if id == -1:
        raise AuthError
    

    return id
    