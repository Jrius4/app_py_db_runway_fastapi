from typing import List
from fastapi import FastAPI, Depends,status,Response,HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from uuid import uuid4
from .helpers import Hash
from datetime import datetime


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users",response_model=List[schemas.ShowUserSchema],tags=["users"])

def get_users(db:Session=Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.get("/users/{id}",status_code=status.HTTP_200_OK,response_model=schemas.ShowUserSchema,tags=["users"])

def show(id:int,response:Response,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with the id of {id} is not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail":f"User with the id of {id} is not found"}

    return user


@app.post("/users",status_code=status.HTTP_201_CREATED,tags=["users"])

def create_user(user:schemas.UserSchema,db:Session=Depends(get_db)):

    hashedPassword = Hash.bcrypt(user.password)
    new_user= models.User(name=user.name,email=user.email,
    nickname=user.nickname,fullname=user.fullname,
    password=hashedPassword,uuid=str(uuid4()))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.put("/users/{id}",status_code=status.HTTP_202_ACCEPTED,tags=["users"])

def update_user(id,request: schemas.UserSchema, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with the id of {id} is not found")
    else:
        user.update(request.dict(), synchronize_session=False)

        db.commit()

        user = db.query(models.User).filter(models.User.id == id).first()
        return {
            "user":user,
            "message":"successful update"
        }



@app.delete("/users/{id}",status_code=status.HTTP_204_NO_CONTENT,tags=["users"])

def destroy_user(id, db:Session=Depends(get_db)):
    

    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with the id of {id} is not found")
    
    else:
        db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)
        db.commit()
        return {"message":"delete"}



# blogs


@app.get("/blogs",response_model=List[schemas.ShowBlogSchema],tags=["blogs"])

def get_blogs(db:Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blogs/{id}",status_code=status.HTTP_200_OK,response_model=schemas.ShowBlogSchema,tags=["blogs"])
# @app.get("/blogs/{id}",status_code=status.HTTP_200_OK)

def show(id:int,response:Response,db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Blog with the id of {id} is not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail":f"Blog with the id of {id} is not found"}

    return blog


@app.post("/blogs",status_code=status.HTTP_201_CREATED,tags=["blogs"])

def create_blog(blog:schemas.BlogSchema,db:Session=Depends(get_db)):

    
    new_blog= models.Blog(title=blog.title,body=blog.body,
    published=blog.published,created_at=datetime.now(),
    updated_at=datetime.now(),uuid=str(uuid4()),user_id= 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.put("/blogs/{id}",status_code=status.HTTP_202_ACCEPTED,tags=["blogs"])

def update_blog(id,request: schemas.ShowBlogSchema, db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Blog with the id of {id} is not found")
    else:
        blog.update(request.dict(), synchronize_session=False)

        db.commit()

        blog = db.query(models.Blog).filter(models.Blog.id == id).first()
        return {
            "Blog":blog,
            "message":"successful update"
        }



@app.delete("/blogs/{id}",status_code=status.HTTP_204_NO_CONTENT,tags=["blogs"])

def destroy_blog(id, db:Session=Depends(get_db)):
    

    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Blog with the id of {id} is not found")
    
    else:
        db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
        db.commit()
        return {"message":"delete"}


