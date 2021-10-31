from typing import List, Optional
from datetime import timedelta,datetime
from pydantic import BaseModel

class UserSchema(BaseModel):
    name:str
    email:str
    fullname:str
    nickname:str
    password:str

class UserBlogsSchema(BaseModel):
    title:str
    body:str
    uuid:str
    created_at:Optional[datetime]
    updated_at:Optional[datetime]
    published:bool

    class Config():
        orm_mode = True

class ShowUserSchema(BaseModel):
    name:str
    email:str
    fullname:str
    nickname:str
    uuid:str
    blogs : List[UserBlogsSchema]

    class Config():
        orm_mode = True


class BlogSchema(BaseModel):
    title:str
    body:str
    uuid:str
    created_at:str
    updated_at:str
    published:bool



class ShowBlogSchema(BlogSchema):
    title:str
    body:str
    created_at:Optional[datetime]
    updated_at:Optional[datetime]
    published:bool
    creator:ShowUserSchema


    class Config():
        orm_mode = True