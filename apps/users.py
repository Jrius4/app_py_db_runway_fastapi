from database.config import db_session as session
from database.models import User

def index():
    result = session.query(User).all()
    return result

def create_user(name,fullname,nickname):
    
    new_user = User(name=name,fullname= fullname,nickname=nickname )
    session.add(new_user)
    
    success = True
    try:
        session.commit()
    except:
        session.rollback()
        session.flush()
        success=False
    return success

def get_user(keyword):
   result = session.query(User).filter(User.id == keyword).first()
   return result

def update_user(keyword,name,fullname,nickname):
    session.query(User).filter(User.id == keyword).update(
        {
            User.fullname:fullname,
            User.name:name,
            User.nickname:nickname
        },synchronize_session=False
    )
    
   

    success = True
    try:
        session.commit()
    except:
        session.rollback()
        session.flush()
        success=False
    return success

def delete_user(keyword):
    session.query(User).filter(User.id == keyword).delete()


    success = True
    try:
        session.commit()
    except:
        session.rollback()
        session.flush()
        success=False
    return success

def raw_sql():
    rs = session.execute("""SELECT * FROM users;""")
    return rs