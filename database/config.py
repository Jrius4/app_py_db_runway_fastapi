import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from sqlalchemy.ext.declarative import declarative_base




project_dir = os.path.dirname(os.path.abspath(__file__))

database_file = "sqlite:///{}".format(os.path.join(project_dir,"app.db"))

engine = create_engine(database_file,echo=True)

db_session = scoped_session(sessionmaker(
    autocommit=False,autoflush=False,
    bind=engine
))

Model= declarative_base(name="Model")
Model.query = db_session.query_property

def init_db():
    Model.metadata.create_all(bind=engine)