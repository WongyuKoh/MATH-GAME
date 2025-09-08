from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.school import school_schema,school_crud
from domain.user import user_crud
from domain.gametype import gametype_crud

router = APIRouter(
    prefix="/api/school",
)
# ----- problem ------ 

def exiting_school(db,school_name):
    school_id = user_crud.exist_school(db,school_name)
    
    if school_id==0:
        return 0
    
    return 1


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def school_create(_school_create: school_schema.SchoolCreate,
                  db: Session = Depends(get_db)):
    
    if exiting_school(db,_school_create.school_name):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="학교가 이미 존재합니다.")
    
    
    db_school = school_crud.create_school(db,_school_create.school_name,address=_school_create.address)
    
    gametype_crud.create_type(db=db,school_id = db_school.school_id,typename="수열",school_name=_school_create.school_name)
    gametype_crud.create_type(db=db,school_id = db_school.school_id,typename="로그",school_name=_school_create.school_name)
    gametype_crud.create_type(db=db,school_id = db_school.school_id,typename="지수",school_name=_school_create.school_name)
    

@router.get("/list",response_model=school_schema.SchoolList)
def school_list(db:Session = Depends(get_db)):
    
    return {"school_list":school_crud.school_list(db)}

@router.get("/search-list",response_model=school_schema.SchoolSearchList)
def school_list(search_text : str = "",
                db:Session = Depends(get_db)):
    
    search_result = school_crud.school_search_list(db=db,search_text=search_text)
    
    return {"serach_data_cnt":len(search_result),"school_search_list":search_result}

@router.get("/limited-search-list",response_model=school_schema.SchoolSearchList)
def school_list(search_text : str = "",
                search_data_cnt : int = 10, now_page : int = 1,
                db:Session = Depends(get_db)):
    
    search_result_cnt,search_result = school_crud.school_limited_search_list(db=db,search_text=search_text,
                                                           now_page=now_page,
                                                           search_data_cnt=search_data_cnt)
    
    return {"serach_data_cnt":search_result_cnt, "school_search_list":search_result}