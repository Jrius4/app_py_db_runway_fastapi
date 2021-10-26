from config import Model
from sqlalchemy import Column,String,Integer,ForeignKey

class User(Model):
    __tablename__ = "users"
    id = Column("user_id",Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
        self.name, self.fullname, self.nickname)
