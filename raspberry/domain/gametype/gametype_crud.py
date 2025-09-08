from models import Gametype,User
from sqlalchemy.orm import Session
import datetime
from sqlalchemy.sql import func

from domain.record.record_schema import RecordCreate
import asyncio

from domain.score import score_router,score_schema


def create_type(db: Session, school_id: int,typename:int,school_name:str=""):
    
    check = len(db.query(Gametype).filter(Gametype.typename==typename).filter(Gametype.school_id==school_id).all())
    if check>0:
        return 0
    
    
    db_gametype = Gametype(
        typename = typename,
        school_id=school_id
    )
    db.add(db_gametype)
    db.commit()
    
    # score 에 전체 추가
    Users = db.query(User.school_id,User.username,User.school_number,User.id).filter(User.school_id==school_id).all()
    
    #print("school_name",school_name)
    for user in Users:
        #print("user",user)
        score_router.create_score(db=db,school_name=school_name,score_input=score_schema.ScoreCreate(user_id=user.id,gametype=typename,score=0))
    
    return 1
    
    
def type_list(db:Session,school_id : int):
    return db.query(Gametype).filter(Gametype.school_id==school_id).all()

def check_category(db:Session,category:str, school_id : int):
    category = db.query(Gametype).filter(Gametype.school_id==school_id).filter(Gametype.typename==category).all()
    if len(category)>0:
        return 1
    else:
        return 0