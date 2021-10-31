from fastapi import APIRouter, Depends,status,Response,HTTPException
from ..database import get_db
from typing import List
from .. import schemas,models
from sqlalchemy.orm import Session
from uuid import uuid4
from ..helpers import Hash



router = APIRouter(
    prefix="/users"
,tags=["users"]
)

@router.get("",response_model=List[schemas.ShowUserSchema])

def get_users(db:Session=Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.ShowUserSchema)

def show(id:int,response:Response,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with the id of {id} is not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail":f"User with the id of {id} is not found"}

    return user


@router.post("",status_code=status.HTTP_201_CREATED)

def create_user(user:schemas.UserSchema,db:Session=Depends(get_db)):

    hashedPassword = Hash.bcrypt(user.password)
    new_user= models.User(name=user.name,email=user.email,
    nickname=user.nickname,fullname=user.fullname,
    password=hashedPassword,uuid=str(uuid4()))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED)

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



@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)

def destroy_user(id, db:Session=Depends(get_db)):
    

    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with the id of {id} is not found")
    
    else:
        db.query(models.User).filter(models.User.id == id).delete(synchronize_session=False)
        db.commit()
        return {"message":"delete"}

