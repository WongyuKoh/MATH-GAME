from fastapi import APIRouter,HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status
from argon2.exceptions import VerificationError
from domain.rank import rank_schema,rank_crud
from database import get_db

router = APIRouter(
    prefix="/api/rank",
)



@router.get("/list/{page_data_cnt}/{now_page}", response_model=rank_schema.RankList)
def user_list(db: Session = Depends(get_db),
                  page_data_cnt : int = 10, now_page : int = 1, category : str = ""):
    rank_list = rank_crud.get_rank_list(
        db, page_data_cnt=page_data_cnt,now_page=now_page,category=category)
    
    #print(f"_question_list : {_user_list.first().school_number}")
    
    return {'rank_list':rank_list}

@router.get("/class/list/{class_number}", response_model=rank_schema.RankList)
def user_list(db: Session = Depends(get_db),
                  class_number : int = 1,category : str = ""):

    rank_list = rank_crud.get_rank_class_list(
        db, class_number=class_number,category=category)
    
    #print(f"_question_list : {_user_list.first().school_number}")
    
    return {'rank_list':rank_list}

    
@router.get("/user-profile/{school_number}/{category}", response_model=rank_schema.Rank_User)
def rank_user(db: Session = Depends(get_db),
                  school_number : int = 11111, category : str = ""):

    rank,rank_user = rank_crud.get_rank_user_profile(
        db, school_number=school_number,category=category)
    
    
    #print(f"_question_list : {_user_list.first().school_number}")
    
    return {"rank":rank,"info":rank_user}