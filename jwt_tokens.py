import jwt
from config import SECRET_KEY



def encode_jwt(body:dict, algorithm = "HS256") -> str:

    encoded_jwt = jwt.encode(body, SECRET_KEY, algorithm)
    return encoded_jwt

def decode_jwt(encoded_jwt:str) -> dict:

    decoded_jwt = jwt.decode(encoded_jwt, SECRET_KEY, algorithms=["HS256"])
    return decoded_jwt

