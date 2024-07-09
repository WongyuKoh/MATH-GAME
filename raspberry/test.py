"""from sqlalchemy import create_engine , MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./myapi.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)""" 
"""
   from sqlalchemy.ext.declarative import declarative_base 
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,MetaData
import json
import os
#'mysql+pymysql://root:kohwongyu@121.191.57.210/MathGame'
URL_DATABASE = 'mysql+pymysql://root:kohwongyu@121.191.57.210/MathGame_rev2'#'mysql+pymysql://root:kohwongyu@localhost:3306/MathGame'
engine = create_engine(URL_DATABASE)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
"""naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
Base.metadata = MetaData(naming_convention=naming_convention)"""
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

def findtrytime(text):

	#text=data_parsing['user_answers']
	text=text.replace(',,',',')
	text=text.split(',')

	trytime = -1
	if len(text)==0:
		if len(text)==0:
			trytime=5
		elif text=="ac":
			trytime=1
		else:
			trytime=5
	else:
		if text[-1]=='wa' or text[-1]=='w':
			trytime=5
		elif text[-1]=='ac' or text[-1]=='c':
			trytime=len(text)
		else:
			if text[-1]=='':
				trytime=5
			else:
				trytime=len(text)
    

	if trytime>4:
		trytime=5

	return trytime

from fastapi import Depends

db = Depends(get_db)

from models import Detail


detail = db.query(Detail).all()
for i in range(len(detail)):
    detail.trytime = findtrytime(detail[i].user_answers)

detail.commit()