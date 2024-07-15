from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db

import asyncio
from domain.user import user_crud
from domain.score import score_schema,score_crud
from models import Gametype,Score

router = APIRouter(
    prefix="/api/score",
)


# 학교 체크
def exiting_school(db,school_name):
    school_id = user_crud.exist_school(db,school_name)
    
    if school_id==0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="학교가 존재하지 않습니다.")
    
    return school_id

"""class GametypeCreate(BaseModel):
    school_id : int = 0
    typename : str = ""
"""


@router.post("/create-score", status_code=status.HTTP_204_NO_CONTENT)
def create_score(school_name : str,score_input : score_schema.ScoreCreate,
                              db: Session = Depends(get_db)): # 어차피 유저에게 업데이트 하는 거면 유저의 id 값을 구할 수 있음
    
    school_id = exiting_school(db,school_name)
    score_crud.check_gametype(db,school_id=school_id,gametype=score_input.gametype)
    
    if score_crud.check_record_score(db=db,user_id=score_input.user_id,gametype=score_input.gametype,school_id=school_id,score=score_input.score):
        return
    

    score_crud.create_score(db=db,school_id=school_id,user_id = score_input.user_id, gametype = score_input.gametype, score = score_input.score)
    
@router.get("/score-list", response_model=score_schema.Scorelist)
def score_list(db: Session = Depends(get_db)): # 어차피 유저에게 업데이트 하는 거면 유저의 id 값을 구할 수 있음
    

    return {"scorelist":score_crud.score_list_all(db)}
    
@router.get("/score-update")
def score_update_all(db: Session = Depends(get_db)): # 어차피 유저에게 업데이트 하는 거면 유저의 id 값을 구할 수 있음
    
    score_crud.score_update_all(db)
    
