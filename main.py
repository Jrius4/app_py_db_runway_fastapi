from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

@app.get("/")

def index():
    return {"data":{'name':'kazibwe'}}


@app.get("/users")

def get_users(limit:int = 10,sort:Optional[str]=None):
    result = f'{limit} users from db'
    return {"data":result} 


@app.get("/users/administrator")

def get_users_admins():
    return {"data":"all administrators"}


@app.get("/users/{id}")

def get_user(id:int):
    return {"data":id} 


class User(BaseModel):
    name:str
    title:str
    admin:Optional[bool]

@app.post("/users")
def create_user(request:User):
    return {"data":f"{request.name} is created"}


if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=9000)