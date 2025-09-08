from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db

import asyncio
from domain.record import record_schema, record_crud
from domain.user import user_crud
from domain.detail import detail_crud
from domain.problem_data.pbd_schema import ProblemCreate,ProblemTitleCreate
from domain.problem_data import pbd_crud

from domain.aimodel import aimodel_router


# record school_id 추가 하는 작업 해야됨

router = APIRouter(
    prefix="/api/record",
)


# 학교 체크
def exiting_school(db,school_name):
    school_id = user_crud.exist_school(db,school_name)
    
    if school_id==0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="학교가 존재하지 않습니다.")
    
    return school_id


def findtrytime(text):

	#text=data_parsing['user_answers']
	text=text.replace(',,',',')
	text=text.split(',')

	trytime = -1
	if len(text)==0:
		if len(text)==0:
			trytime=5
		elif text=="ac":
			trytime=1
		else:
			trytime=5
	else:
		if text[-1]=='wa' or text[-1]=='w':
			trytime=5
		elif text[-1]=='ac' or text[-1]=='c':
			trytime=len(text)
		else:
			if text[-1]=='':
				trytime=5
			else:
				trytime=len(text)
    

	if trytime>4:
		trytime=5

	return trytime


@router.get("/category_try/{school_class}",response_model=record_schema.Categorylist)
def category_try(school_class:int,school_name:str,db:Session = Depends(get_db)):
    school_id = exiting_school(db,school_name)
    
    categorylist=record_crud.category_try(db=db,school_class=school_class,school_id=school_id)
    
    return {"classcategorylist" : categorylist}
    
    

@router.post("/create/{school_number}", status_code=status.HTTP_204_NO_CONTENT)
def record_create(school_number: int,school_name : str,
                  _record_create: record_schema.RecordCreate,
                  db: Session = Depends(get_db)):
    
    school_id = exiting_school(db,school_name)

    # create record
    user = user_crud.get_user(db, school_number=school_number,school_id=school_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    
    
    #print("#$%#$%#$%")
    
    # ------ evaluate 위치 ------
    """def user_evaluate(_record_create: record_schema.RecordCreate,
                  db: Session = Depends(get_db), 
                  school_number : int = 0, school_name : str = ""):"""
                  
    aimodel_router.user_evaluate(db=db,_record_create = _record_create, school_number=school_number,school_name=school_name)
    
    # ------------------------
    
    #print("HDFG")
    #print(_record_create.score)
    
    new_record = record_crud.create_record(db, user=user,
                              record_create=_record_create,school_id=school_id
                              )

    #print("!!@#")
        
    all_cnt=0

    for game_problem in _record_create.detail:
        all_cnt+=detail_crud.create_detail(db,record=new_record,detail_create=game_problem)
        
            
        #print("#@$@",_record_create.main_category)
            
        pbd_crud.create_problem(db,
                                problem_create=ProblemCreate(problem=game_problem.problem,
                                                             category=game_problem.category,
                                                             bundles_idx_list="",
                                                             answer=game_problem.problem_answer,main_category=_record_create.main_category),
                                
                                trytime=findtrytime(game_problem.user_answers),
                                main_category=_record_create.main_category) # 랜덤 문제라고 하더라도 결국 틀이 있고 ,사전에 랜덤 문제의 형태를 넣어줘야되기 때문에 db 에 다 있음
    """bundles_idx_list : str = "" # 음수 값 들어가는 건 그 값을 idx 가 아닌 실제로 이용하겠다는 의미, - 를 붙여서 사용
problem_digit_idx_list : str = "" 
    """
            
        
    record_crud.trytime_update(db,record=new_record,cnt=all_cnt)
        
        


@router.post("/record-trytime-update")
def detail_trytime_update(db: Session = Depends(get_db)):
    record_crud.record_trytime_update(db)
    
        
        
@router.get("/aidata-record/{school_number}/{category}", response_model=record_schema.RecordList)
def aidata_record(db: Session = Depends(get_db),school_name : str = "",
                  school_number : int = 11111, category : str = ""):
    
    school_id = exiting_school(db,school_name)

    rank_user_list = record_crud.aidata_record(
        db, school_number=school_number,category=category,school_id=school_id)
    
    
    return {"record_list":rank_user_list}

        
@router.get("/record-by-category/{school_number}/{category}/{cnt}", response_model=record_schema.RecordList)
def user_record_category(db: Session = Depends(get_db),
                  school_number : int = 11111, category : str = "",cnt : int = 3,school_name : str = ""):
    
    
    school_id = exiting_school(db,school_name)

    rank_user_list = record_crud.get_record_by_category(
        db, school_number=school_number,category=category,cnt = cnt,school_id=school_id)
    
    
    return {"record_list":rank_user_list}

@router.get("/record-by-category-all/{school_number}/{category}", response_model=record_schema.RecordList)
def user_record_category_all(db: Session = Depends(get_db),
                  school_number : int = 11111, category : str = "",school_name : str = ""):
    
    
    school_id = exiting_school(db,school_name)

    rank_user_list = record_crud.get_record_by_category_all(
        db, school_number=school_number,category=category,school_id=school_id)
    
    
    return {"record_list":rank_user_list}

@router.get("/record-cnt-all/{school_number}", response_model=record_schema.RecordCnt)
def user_record_cnt_all(db: Session = Depends(get_db),
                  school_number : int = 11111,school_name : str = ""):
    
    school_id = exiting_school(db,school_name)

    rank_cnt = record_crud.get_record_cnt_all(
        db, school_number=school_number,school_id=school_id)
    
    
    return {"record_cnt":rank_cnt}

@router.get("/record-class-cnt-all", response_model=record_schema.RecordClassCnt)
def user_record_class_cnt_all(db: Session = Depends(get_db),
                  school_class : int = 1,school_name : str = ""):
    
    school_id = exiting_school(db,school_name)

    rank_list = record_crud.get_record_class_cnt_all(
        db, school_class=school_class,school_id=school_id)
    
    
    return {"record_class":rank_list}