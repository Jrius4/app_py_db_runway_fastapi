from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


project_dir = os.path.dirname(os.path.abspath(__file__))

SQLALCHEMY_DATABASE_URL = "sqlite:///{}".format(os.path.join(project_dir,"sys.db"))
engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False})

SessionLocal = sessionmaker(bind=engine,autocommit=False,autoflush=False)

Base = declarative_base()
