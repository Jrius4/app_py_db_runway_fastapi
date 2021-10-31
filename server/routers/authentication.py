from fastapi import APIRouter
from server import models
from fastapi import APIRouter, Depends,status,HTTPException
from server.database import get_db
from server.helpers import Hash
from sqlalchemy.orm import Session
from datetime import timedelta
from server.token import ACCESS_TOKEN_EXPIRE_MINUTES,create_access_token
from fastapi.security import OAuth2PasswordRequestForm



router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)

@router.post('')

# def login(request:schemas.LoginSchema, db:Session=Depends(get_db)):

def login(request:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username",
            headers={"WWW-Authenticate": "Bearer"},
            )
    if not Hash.verify(user.password,request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
            )
            
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    # return user
    return {"access_token": access_token, "token_type": "bearer"}