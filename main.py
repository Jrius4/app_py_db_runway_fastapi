from typing import Optional
from fastapi import FastAPI

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

@app.post("/users")
def create_user():
    return {
        "data":"User is created"
    }