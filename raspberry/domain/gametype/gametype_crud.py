from models import Gametype
from sqlalchemy.orm import Session
import datetime
from sqlalchemy.sql import func

from domain.record.record_schema import RecordCreate
import asyncio


def DateTimeNow():
    nowDate=datetime.datetime.now()
    return f"{str(nowDate.year)}-{str(nowDate.month)}-{str(nowDate.day)} {str(nowDate.hour)}:{str(nowDate.minute)}:{str(nowDate.second)}.{str(nowDate.microsecond)}"


def create_type(db: Session, school_id: int,typename:int):
    
    check = len(db.query(Gametype).filter(Gametype.typename==typename).filter(Gametype.school_id==school_id).all())
    if check>0:
        return 0
    
    
    db_gametype = Gametype(
        typename = typename,
        school_id=school_id
    )
    db.add(db_gametype)
    db.commit()
    
    return 1
    
    
def type_list(db:Session,school_id : int):
    return db.query(Gametype).filter(Gametype.school_id==school_id).all()
