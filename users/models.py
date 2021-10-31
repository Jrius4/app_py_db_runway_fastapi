from sqlalchemy import Column, Integer,String,DateTime,Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"],deprecated="auto")
hashedPassword = pwd_cxt.hash("password")
class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    email = Column(String,unique=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String,unique=True)
    password = Column(String,default="hashedPassword")
    uuid = Column(String,unique=True)

    blogs = relationship("Blog",back_populates="creator")

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s', password='%s', email='%s',uuid='%s',blogs='%s')>" % (
        self.name, self.fullname, self.nickname,self.password, self.email, self.uuid, self.blogs)




class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,unique=True)
    body = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    published = Column(Boolean,default="hashedPassword")
    uuid = Column(String,unique=True)
    user_id = Column(Integer,ForeignKey('users.id'))

    creator = relationship("User",back_populates="blogs")

    def __repr__(self):
        return "<Blog (title='%s', body='%s', created_at='%s', updated_at='%s', published='%s',uuid='%s',user_id='%s',creator='%s')>" % (
        self.title, self.body, self.created_at,self.updated_at, 
        self.published, self.uuid,self.user_id,self.creator)