from models import Score,User
from sqlalchemy.orm import Session
import datetime
from sqlalchemy.sql import func
from fastapi import APIRouter, Depends, HTTPException
from models import Gametype,Score,Record
from starlette import status

import asyncio



def check_gametype(db : Session,school_id : int,gametype : str):
    check = db.query(Gametype).filter(Gametype.school_id==school_id).filter(Gametype.typename==gametype).all()
    if len(check)==0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="게임 유형이 존재하지 않습니다.")

def check_record_score(db : Session,user_id : int, gametype : str, school_id : int,score : int):
    check = db.query(Score).filter(Score.user_id==user_id).filter(Score.gametype==gametype).filter(Score.school_id==school_id).all()
    if len(check)>0:
        check[0].score = max(score,check[0].score)
        db.commit()
        return True
    
    return False


def score_update_all(db:Session):
    
    records = db.query(Record).all()
    
        
    for idx, record in enumerate(records):
        
        #print(f"idx : {idx}")
        
        find_user_score = db.query(Score).\
            filter(Score.school_id==record.school_id).\
            filter(Score.school_number==record.user_id).\
            filter(Score.gametype==record.main_category).all()
            
        if len(find_user_score)==0:
            
            user_status = db.query(User).filter(User.school_id==record.school_id).\
                filter(User.school_number==record.user_id).first()
            
            db_score = Score(
                school_id = record.school_id,
                gametype = record.main_category,
                score = record.score,
                user_id = user_status.id,
                username = record.user_name,
                school_number = record.user_id
                
            )
            db.add(db_score)

            
        else:
            find_user_score[0].score = max(record.score,find_user_score[0].score)
        
        db.commit()
    
    
    

def score_list_all(db:Session):
    return db.query(Score).all()

def create_score(db: Session, school_id : int, user_id: int,gametype:str,score : int):
    
    user_status = db.query(User).filter(User.id==user_id).first()

    db_score = Score(
        school_id = school_id,
        gametype = gametype,
        score = score,
        user_id = user_id,
        username = user_status.username,
        school_number = user_status.school_number
        
    )
    db.add(db_score)
    db.commit()
    
    