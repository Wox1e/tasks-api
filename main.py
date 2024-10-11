from fastapi import FastAPI, Request, Response
from db import User, session, Task
from jwt_tokens import decode_jwt, encode_jwt
from utils import *
from config import REQUESTS_PER_MINUTE_LIMIT
from logger import to_brocker, BROKER_URI, logging_startup
from caching import *


#SlowAPI
from slowapi import Limiter
from slowapi.util import get_remote_address
#
limiter = Limiter(get_remote_address)


app = FastAPI()
logging_startup()



@app.post("/register")
@limiter.limit(f"120/minute")
async def register(request: Request):

    try:
        body = dict(await request.json())
        username = body["username"]
        password = body["password"]
        user = User(username, password)
        user.addToDB()

        return {"status":True}
    
    except KeyError as e:
        return {"status":False, "Missed Arguments":e.args}
    except Exception as e:
        to_brocker(BROKER_URI, "logs", f"error: {e}")
        return {"status":False}

    

@app.post("/login")
@limiter.limit(f"120/minute")
async def login(request: Request, response:Response):

    try:
        body = dict(await request.json())

        username = body["username"]
        password = body["password"]
        isCorrectCredentials = User.check_credentials(username, password)

        if not isCorrectCredentials:
            return{"status":True, "auth":False}
        
        
        jwt_payload = {
            "username":username,
            "password":password
        }
        token = encode_jwt(jwt_payload)

        if isCookieAllowed(body):
            response.set_cookie(key="token", value=token)

        return {"status":True, "auth":True, "token": token}
    except Exception as e:
        to_brocker(BROKER_URI, "logs", f"error: {e}")
        return {"status":False}
    


@app.post("/logout")
async def logout(request: Request):
    request.cookies.clear()
    return True




@app.post("/tasks")
@limiter.limit(f"120/minute")
async def post_tasks(request: Request):
    try:
        body = dict(await request.json())
        id = tokenAuth(body, request)
        description = body["description"]
        task = Task(id, description)
        task.addToDB()
        return {"status": True, "auth":True, "added":True}
    
    except AuthError as e:
        return {"status":False, "Error":e.msg}
    except Exception as e:
        to_brocker(BROKER_URI, "logs", f"error: {e}")
        return {"status":False}
    
    

@app.get("/tasks")
@limiter.limit(f"120/minute")
# @cache(expire=15, key_builder=request_key_builder)
async def get_tasks(request: Request):
    try:
        body = dict(await request.json())
        id = tokenAuth(body, request)
        
        tasks = session.query(Task).filter_by(user_id = id).all()
        return tasks
    
    except AuthError as e:
        return {"status":False, "Error":e.msg}
    except Exception as e:
        to_brocker(BROKER_URI, "logs", f"error: {e}")
        return {"status":False}
    


@app.get("/tasks/{task_id}")
@limiter.limit(f"120/minute")
@cache(expire=15, key_builder=request_key_builder)
async def user_tasks(task_id:int, request:Request):
    try:
        body = dict(await request.json())
        id = tokenAuth(body, request)

        cache = getCache(request, body)
        if cache != None: 
            print("from cache:", cache)
            return cache

        task = session.query(Task).filter_by(user_id = id).filter_by(id = task_id).first()
        return task
    
    except AuthError as e:
        return {"status":False, "Error":e.msg}
    except Exception as e:
        to_brocker(BROKER_URI, "logs", f"error: {e}")
        return {"status":False}
    


@app.put("/tasks/{task_id}")
@limiter.limit(f"120/minute")
async def update_task(task_id:int, request:Request):
    try:
        body = dict(await request.json())
        id = tokenAuth(body, request)
        
        description = body["description"]

        task = session.query(Task).filter_by(user_id = id).filter_by(id = task_id).first()
        task.description = description
        session.commit()

        return {"status":True, "auth":True, "updated":True}
    
    except AuthError as e:
        return {"status":False, "Error":e.msg}
    except Exception as e:
        to_brocker(BROKER_URI, "logs", f"error: {e}")
        return {"status":False}
    


@app.put("/tasks/{task_id}")
@limiter.limit(f"120/minute")
async def put_task(task_id:int, request:Request):
    try:
        body = dict(await request.json())
        id = tokenAuth(body, request)
       
        description = body["description"]
        
        task = session.query(Task).filter_by(user_id = id).filter_by(id = task_id).first()
        task.description = description
        session.commit()
        return {"status":True, "auth":True, "updated":True}
    
    except AuthError as e:
        return {"status":False, "Error":e.msg}
    except Exception as e:
        to_brocker(BROKER_URI, "logs", f"error: {e}")
        return {"status":False}
    

@app.delete("/tasks/{task_id}")
@limiter.limit(f"120/minute")
async def delete_task(task_id:int, request:Request):
    try:
        body = dict(await request.json())
        id = tokenAuth(body, request)

        task = session.query(Task).filter_by(user_id = id).filter_by(id = task_id).first()
        session.delete(task)
        session.commit()
        return {"status": True, "auth":True, "deleted":True}
    
    except AuthError as e:
        return {"status":False, "Error":e.msg}
    except Exception as e:
        to_brocker(BROKER_URI, "logs", f"error: {e}")
        return {"status":False}
    

