from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.user.user_router import get_current_user
from models import Record
from domain.record import record_schema, record_crud
from domain.user import user_crud
from domain.detail import detail_crud

router = APIRouter(
    prefix="/api/record",
)


@router.post("/create/{school_number}", status_code=status.HTTP_204_NO_CONTENT)
def record_create(school_number: int,
                  _record_create: record_schema.RecordCreate,
                  db: Session = Depends(get_db)):

    # create record
    user = user_crud.get_user(db, school_number=school_number)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    
    
    new_record = record_crud.create_record(db, user=user,
                              record_create=_record_create,
                              )
    
    for game_problem in _record_create.detail:
        detail_crud.create_detail(db,record=new_record,detail_create=game_problem)
        
# 추가 코드 부분 
        
@router.get("/record-by-category/{school_number}/{category}/{cnt}", response_model=record_schema.RecordList)
def user_record_category(db: Session = Depends(get_db),
                  school_number : int = 11111, category : str = "",cnt : int = 3):

    rank_user_list = record_crud.get_record_by_category(
        db, school_number=school_number,category=category,cnt = cnt)
    
    
    return {"record_list":rank_user_list}

@router.get("/record-by-category-all/{school_number}/{category}", response_model=record_schema.RecordList)
def user_record_category(db: Session = Depends(get_db),
                  school_number : int = 11111, category : str = ""):

    rank_user_list = record_crud.get_record_by_category_all(
        db, school_number=school_number,category=category)
    
    
    return {"record_list":rank_user_list}