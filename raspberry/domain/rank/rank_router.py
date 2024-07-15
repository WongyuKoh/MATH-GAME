from fastapi import APIRouter,HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status
from argon2.exceptions import VerificationError
from domain.rank import rank_schema,rank_crud
from database import get_db
from domain.user import user_crud

router = APIRouter(
    prefix="/api/rank",
)
# 학교 체크
def exiting_school(db,school_name):
    school_id = user_crud.exist_school(db,school_name)
    
    if school_id==0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="학교가 존재하지 않습니다.")
    
    return school_id


@router.get("/list/{page_data_cnt}/{now_page}", response_model=rank_schema.RankList)
def user_list(db: Session = Depends(get_db),school_name : str = "",
                  page_data_cnt : int = 10, now_page : int = 1, category : str = ""):
    
    school_id = exiting_school(db,school_name)
    
    rank_list = rank_crud.get_rank_list(
        db, page_data_cnt=page_data_cnt,
        now_page=now_page,category=category,
        school_id=school_id)
    
    #print(f"_question_list : {_user_list.first().school_number}")
    
    return {'rank_list':rank_list}

@router.get("/class/list/{class_number}", response_model=rank_schema.RankList)
def user_list(db: Session = Depends(get_db),school_name : str = "",
                  class_number : int = 1,category : str = ""):

    school_id = exiting_school(db,school_name)

    rank_list = rank_crud.get_rank_class_list(
        db, class_number=class_number,category=category,school_id=school_id)
    
    #print(f"_question_list : {_user_list.first().school_number}")
    
    return {'rank_list':rank_list}

    
@router.get("/user-profile/{school_number}/{category}", response_model=rank_schema.Rank_User)
def rank_user(db: Session = Depends(get_db),school_name : str = "",
                  school_number : int = 11111, category : str = ""):
    
    
    school_id = exiting_school(db,school_name)

    rank,rank_user = rank_crud.get_rank_user_profile(
        db, school_number=school_number,category=category,school_id=school_id)
    
    
    #print(f"_question_list : {_user_list.first().school_number}")
    
    return {"rank":rank,"info":rank_user}