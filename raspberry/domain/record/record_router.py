from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db

import asyncio
from domain.user.user_router import get_current_user
from domain.record import record_schema, record_crud
from domain.user import user_crud
from domain.detail import detail_crud
from domain.problem_data import pbd_crud

router = APIRouter(
    prefix="/api/record",
)

# class ProblemCreate(BaseModel):
#     problem : str = ""
#     category : str = ""

# 학교 체크
def exiting_school(db,school_name):
    school_id = user_crud.exist_school(db,school_name)
    
    if school_id==0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="학교가 존재하지 않습니다.")
    
    return school_id



@router.post("/create/{school_number}", status_code=status.HTTP_204_NO_CONTENT)
def record_create(school_number: int,school_name : int,
                  _record_create: record_schema.RecordCreate,
                  db: Session = Depends(get_db)):
    
    school_id = exiting_school(school_name)

    # create record
    user = user_crud.get_user(db, school_number=school_number,school_id=school_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    
    
    new_record = record_crud.create_record(db, user=user,
                              record_create=_record_create,school_id=school_id
                              )

    
    async def detail_create_problem(_record_create):
        
        all_cnt=0
    
        for game_problem in _record_create.detail:
            all_cnt+=detail_crud.create_detail(db,record=new_record,detail_create=game_problem)
            if pbd_crud.check_problem_in_db(db,game_problem.problem):
                pbd_crud.create_problem(db,autoproblemdata={"problem":game_problem.problem,"categroy":game_problem.category})
            
            
        record_crud.trytime_update(db,record=new_record,cnt=all_cnt)
        
    asyncio(detail_create_problem(_record_create=_record_create))
        


@router.post("/record-trytime-update")
def detail_trytime_update(db: Session = Depends(get_db)):
    record_crud.record_trytime_update(db)
    
        
        
@router.get("/aidata-record/{school_number}/{category}", response_model=record_schema.RecordList)
def aidata_record(db: Session = Depends(get_db),
                  school_number : int = 11111, category : str = ""):

    rank_user_list = record_crud.aidata_record(
        db, school_number=school_number,category=category)
    
    
    return {"record_list":rank_user_list}

        
@router.get("/record-by-category/{school_number}/{category}/{cnt}", response_model=record_schema.RecordList)
def user_record_category(db: Session = Depends(get_db),
                  school_number : int = 11111, category : str = "",cnt : int = 3):

    rank_user_list = record_crud.get_record_by_category(
        db, school_number=school_number,category=category,cnt = cnt)
    
    
    return {"record_list":rank_user_list}

@router.get("/record-by-category-all/{school_number}/{category}", response_model=record_schema.RecordList)
def user_record_category_all(db: Session = Depends(get_db),
                  school_number : int = 11111, category : str = ""):

    rank_user_list = record_crud.get_record_by_category_all(
        db, school_number=school_number,category=category)
    
    
    return {"record_list":rank_user_list}

@router.get("/record-cnt-all/{school_number}", response_model=record_schema.RecordCnt)
def user_record_cnt_all(db: Session = Depends(get_db),
                  school_number : int = 11111):

    rank_cnt = record_crud.get_record_cnt_all(
        db, school_number=school_number)
    
    
    return {"record_cnt":rank_cnt}

@router.get("/record-class-cnt-all", response_model=record_schema.RecordClassCnt)
def user_record_class_cnt_all(db: Session = Depends(get_db),
                  school_class : int = 1):

    rank_list = record_crud.get_record_class_cnt_all(
        db, school_class=school_class)
    
    
    return {"record_class":rank_list}