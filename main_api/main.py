from fastapi import FastAPI, Request, Response
from db import User, session, Task
from jwt_tokens import *
from utils import *
import uvicorn
import os
from dotenv import load_dotenv
from logger import to_brocker

#SlowAPI
from slowapi import Limiter
from slowapi.util import get_remote_address
#

limiter = Limiter(get_remote_address)
load_dotenv()
app = FastAPI()



if __name__=="__main__":
    uvicorn.run(app)


#
#TODO: Exception handling, Clean the code
#




@app.get("/hello")
@limiter.limit(f"{os.getenv("REQUESTS_PER_MINUTE_LIMIT")}/minute")
def root(request:Request):
    return {"message": "Hello World"}



@app.post("/register")
@limiter.limit(f"{os.getenv("REQUESTS_PER_MINUTE_LIMIT")}/minute")
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
    except:
        return {"status":False}

    

@app.post("/login")
@limiter.limit(f"{os.getenv("REQUESTS_PER_MINUTE_LIMIT")}/minute")
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
    except:
        return {"status":False}
    


@app.post("/logout")
async def logout(request: Request):
    pass




@app.post("/tasks")
@limiter.limit(f"{os.getenv("REQUESTS_PER_MINUTE_LIMIT")}/minute")
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
    except:
        return {"status":False}
    
    

@app.get("/tasks")
@limiter.limit(f"{os.getenv("REQUESTS_PER_MINUTE_LIMIT")}/minute")
async def get_tasks(request: Request):
    try:
        body = dict(await request.json())
        id = tokenAuth(body, request)
        tasks = session.query(Task).filter_by(user_id = id).all()

        return tasks
    
    except AuthError as e:
        return {"status":False, "Error":e.msg}
    except:
        return {"status":False}
    


@app.get("/tasks/{task_id}")
@limiter.limit(f"{os.getenv("REQUESTS_PER_MINUTE_LIMIT")}/minute")
async def user_tasks(task_id:int, request:Request):
    try:
        body = dict(await request.json())
        id = tokenAuth(body, request)
        task = session.query(Task).filter_by(user_id = id).filter_by(id = task_id).first()
        return task
    
    except AuthError as e:
        return {"status":False, "Error":e.msg}
    except:
        return {"status":False}
    


@app.put("/tasks/{task_id}")
@limiter.limit(f"{os.getenv("REQUESTS_PER_MINUTE_LIMIT")}/minute")
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
    except:
        return {"status":False}
    


@app.put("/tasks/{task_id}")
@limiter.limit(f"{os.getenv("REQUESTS_PER_MINUTE_LIMIT")}/minute")
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
    except:
        return {"status":False}
    

@app.delete("/tasks/{task_id}")
@limiter.limit(f"{os.getenv("REQUESTS_PER_MINUTE_LIMIT")}/minute")
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
    except:
        return {"status":False}
    

