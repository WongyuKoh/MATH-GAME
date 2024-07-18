from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db

import asyncio
from domain.user import user_crud
from domain.gametype import gametype_schema,gametype_crud

router = APIRouter(
    prefix="/api/gametype",
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

@router.post("/create-type", status_code=status.HTTP_204_NO_CONTENT)
def user_record_class_cnt_all(gametype_input : gametype_schema.GametypeCreate,
                              db: Session = Depends(get_db)):
    
    school_id = exiting_school(db,gametype_input.school_name)

    v = gametype_crud.create_type(db=db,school_id = school_id, typename=gametype_input.typename)
    
    if v==0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="존재하는 게임 유형입니다.")
    
    
@router.get("/type-list", response_model=gametype_schema.GametypeList)
def user_record_class_cnt_all(school_name : str = "",
                              db: Session = Depends(get_db)):
    
    school_id = exiting_school(db,school_name)

    return {"gametype_list":gametype_crud.type_list(db=db,school_id = school_id)}
