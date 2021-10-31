from fastapi import APIRouter, Depends,status,Response,HTTPException
from server.database import get_db
from typing import List
from server import schemas,models
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime

from .Oauth2 import get_current_user


router = APIRouter(
    prefix="/blogs"
,tags=["blogs"]
)




@router.get("",response_model=List[schemas.ShowBlogSchema])

def get_blogs(db:Session=Depends(get_db),get_current_user:schemas.UserSchema=Depends(get_current_user)):
    blogs = db.query(models.Blog).all()
    return blogs



@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.ShowBlogSchema)


def show(id:int,response:Response,db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Blog with the id of {id} is not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail":f"Blog with the id of {id} is not found"}

    return blog



@router.post("",status_code=status.HTTP_201_CREATED)

def create_blog(blog:schemas.BlogSchema,db:Session=Depends(get_db)):

    
    new_blog= models.Blog(title=blog.title,body=blog.body,
    published=blog.published,created_at=datetime.now(),
    updated_at=datetime.now(),uuid=str(uuid4()),user_id= 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog




@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED)

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



@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)

def destroy_blog(id, db:Session=Depends(get_db)):
    

    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Blog with the id of {id} is not found")
    
    else:
        db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
        db.commit()
        return {"message":"delete"}

