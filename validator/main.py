from fastapi import FastAPI, Request, Response

app = FastAPI()

MAIN_API_URI = ''

#TODO:redirect

@app.post("/register")
async def register(request: Request):

    try:
        body = dict(await request.json())

        if "username" in body.keys() and "password" in body.keys():
            #redirect next
            print("redirect")
            return {"status":True}
        else:
            raise Exception
        
    except:
        return {"status":False}

    

@app.post("/login")
async def login(request: Request, response:Response):

    try:
        body = dict(await request.json())

        if "username" in body.keys() and "password" in body.keys():
            #redirect next
            print("redirect")
            return {"status":True}
        else:
            raise Exception

    except:
        return {"status":False}
    

#TODO: 
@app.post("/logout")
async def logout(request: Request):
    pass




@app.post("/tasks")
async def post_tasks(request: Request):
    try:
        body = dict(await request.json())
        if not ("description" in body.keys()):
            raise Exception
        
        if (request.cookies.get("token") == None) and ("token" not in body.keys()):
            raise Exception

        print("redirect")
        return {"status":True}

    except:
        return {"status":False}
    
    

@app.get("/tasks")
async def get_tasks(request: Request):
    try:
        body = dict(await request.json())
        if (request.cookies.get("token") == None) and ("token" not in body.keys()):
            raise Exception

        print("redirect")
        return {"status":True}

    except:
        return {"status":False}
    


@app.get("/tasks/{task_id}")
async def user_tasks(task_id:int, request:Request):
    try:
        body = dict(await request.json())
        if (request.cookies.get("token") == None) and ("token" not in body.keys()):
            raise Exception

        print("redirect")
        return {"status":True}
    
    except:
        return {"status":False}
    


@app.put("/tasks/{task_id}")
async def update_task(task_id:int, request:Request):
    try:
        body = dict(await request.json())
        if not ("description" in body.keys()):
            raise Exception
        
        if (request.cookies.get("token") == None) and ("token" not in body.keys()):
            raise Exception

        print("redirect")
        return {"status":True}

    except:
        return {"status":False}
    


@app.put("/tasks/{task_id}")
async def put_task(task_id:int, request:Request):
    try:
        body = dict(await request.json())
        if not ("description" in body.keys()):
            raise Exception
        
        if (request.cookies.get("token") == None) and ("token" not in body.keys()):
            raise Exception

        print("redirect")
        return {"status":True}

    except:
        return {"status":False}
    

@app.delete("/tasks/{task_id}")
async def delete_task(task_id:int, request:Request):
    try:
        body = dict(await request.json())

        if (request.cookies.get("token") == None) and ("token" not in body.keys()):
            raise Exception

        print("redirect")
        return {"status":True}

    except:
        return {"status":False}