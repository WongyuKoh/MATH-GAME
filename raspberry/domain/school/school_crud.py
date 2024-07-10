from models import School
from sqlalchemy.orm import Session
import datetime
import asyncio

def create_school(db:Session,school_name : str):
    
    
    db_school = School(school_name=school_name)
    
    db.add(db_school)
    db.commit()
    
    
def school_list(db:Session):
    
    schools=db.query(School).all()
    
    return schools