from models import Problem,Detail,User
from sqlalchemy.orm import Session
import datetime
import asyncio
import re
import json
from domain.problem_data.pbd_schema import ProblemCreate,ProblemTitleCreate
import domain.problem_parsing.exponents.problem_e_1 as pe1
import domain.problem_parsing.exponents.problem_e_2 as pe2
import domain.problem_parsing.exponents.problem_e_3 as pe3

from domain.user import user_crud
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from random import *

from domain.problem_data import pbd_schema
from domain.gametype import gametype_crud

# class Problem(Base): # user 에 종속, record 복수, record id 를 id로 가짐
#     __tablename__ = "problem"

#     id = Column(Integer, primary_key=True)
#     problem = Column(String, nullable=False) # 문제 
#     problem_list = Column(String, nullable=False) # 문제 숫자만 뽑은거

def check_problem_in_db(db:Session,text : str):
    cnt = db.query(Problem).filter(Problem.problem==text).count()
    if cnt > 0:
        return 1
    else:
        return 0

def try_update(db : Session, problem : str = "", trytime : int = 0):
    pb=db.query(Problem).filter(Problem.problem==problem).first()
    pb.trytime +=trytime
    pb.trystudent += 1
    
    db.commit()
    
    pb.problem_level = problem_level(pb.trytime,pb.trystudent)
    
    db.commit()
    
def problem_level_return(trytime,trystudent):
    V=trytime/trystudent
    
    if 3.5<=V:
        return 1 # 난이도 상
    elif 1.5<=V<3.5:
        return 2 # 난이도 중
    else:
        return 3 # 난이도 하

def plbil(bundles_idx_list,category,problem_text): # 여기서 데이터 추출 위치 설정
    if category == '지수 함수 값 계산하기':
        problem_list = str(pe1.data_extract(problem_text))

        if bundles_idx_list == "":
            bundles_idx_list = "[[0,1]]"
            
    elif category == '식을 만족하는 x 값 찾기':
        problem_list = str(pe2.data_extract(problem_text))
        if bundles_idx_list == "":
            bundles_idx_list = "[[0,1],[2,4]]"
    
    elif category == "제곱근 계산":
        problem_list = str(pe3.data_extract(problem_text))
        if bundles_idx_list == "":
            lt = []
            str2list = json.loads(problem_list)
            for i in range(len(str2list)-2): # 값이 음수면 인덱스 값이 아닌 실제 값을 의미, -를 붙여서 사용
                lt.append([-(i+1),str2list[i]])
                
            lt.append([len(str2list)-2,len(str2list)-1])  
            
            bundles_idx_list = str(lt)
            
              
    else:    
        # 저장된 데이터에 기반으로 bundles_idx_list 작성
        # problem_list 작성
        return ["#","#"]
    
    return bundles_idx_list,problem_list


def create_problem(db: Session,
                  problem_create: ProblemCreate = None,
                  trytime = 0,main_category :str = ""):
    
    if check_problem_in_db(db,problem_create.problem):
        try_update(db,problem_create.problem,trytime=trytime)
        return
    
    #print("XCVXCVX",main_category)
    
    trystudent=1
    problem_level = problem_level_return(trytime=trytime,trystudent=trystudent)
    
    # db 에 같은 유형인 거와 bundles_idx_list 가 일치 할거임
    
    
    
    category = problem_create.category
    problem_text = problem_create.problem
    
    problem_list = []
    
    #print(category,problem_text)
    
    #problem_list = list(map(int,re.findall(r'\d+',problem_text))) 문자에서 숫자만 추출하는 코드
    
    bundles_idx_list = problem_create.bundles_idx_list
    
    bundles_idx_list,problem_list=plbil(bundles_idx_list=bundles_idx_list,
                                        category=category,
                                        problem_text=problem_text)
    
    #print("!@#@!#!@#")
    db_problem = Problem(
        problem=problem_text,
        problem_list=problem_list,
        category=category,
        trytime = trytime,
        trystudent = trystudent,
        problem_level = problem_level,
        bundles_idx_list = bundles_idx_list,
        answer = problem_create.answer,
        main_category = main_category
        
                         )
    db.add(db_problem)
    db.commit()
    
    return db_problem


def problem_level(trytime,trystudent):
    V=trytime/trystudent
    
    if 3.5<=V:
        return 1 # 난이도 상
    elif 1.5<=V<3.5:
        return 2 # 난이도 중
    else:
        return 3 # 난이도 하
    

"""
async def change_school_number(school_number,new_school_number):
        change_list=db.query(Record).filter(Record.user_id==school_number).all()
        for data in change_list:
            data.user_id = new_school_number
            
        db.commit()
        
    asyncio.run(change_school_number(school_number=school_number,new_school_number=new_school_number))
    
"""

def problem_update(db:Session):
    details = db.query(Detail).all()
    
    for detail in details: 

        create_problem(db,
                        problem_create=ProblemCreate(problem=detail.problem,
                                                     category=detail.category,
                                                     bundles_idx_list="",
                                                     answer=detail.problem_answer),
                        trytime=detail.trytime)
            
            
    db.commit()
    
    

def exiting_school(db: Session,school_name: str):
    school_id = user_crud.exist_school(db,school_name)
    
    if school_id==0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="학교가 존재하지 않습니다.")
    
    return school_id   

def check_category(db :Session, category : str, school_id : int):
    Category =  gametype_crud.check_category(db=db,category=category,school_id=school_id)
    
    if not Category:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="카테고리가 존재하지 않습니다.")
        


    
#pbd_crud.problem_emit(db=db,username=username,school_name=school_name,problem_level=problem_level)
def problem_emit(db:Session,school_number : int, school_name : str,cnt : int,category : str):
    
    school_id = exiting_school(db,school_name)
    check_category(db,category=category,school_id=school_id)
    user_state = db.query(User).filter(User.school_id==school_id).filter(User.school_number==school_number).first()
    percent=[0,0,0,0] # 상 중 하 랜덤 퍼센트
    
    #print(f"user_level : {user_state.user_level}")
    
    if user_state.user_level==0:
        percent=[25,25,25,25]
    elif user_state.user_level==3: # 하
        percent=[16,22,37,25]
    elif user_state.user_level==2: # 중
        percent=[22,37,16,25] # 22, 59, 75, 100
    else: # 상, = 1
        percent=[37,22,16,25]
        
    problem_list = []
    
    for i in range(cnt):
        #print("================")
        
        rand = choices(range(1,5),weights= [percent[lev]/100 for lev in range(4)])[0]
        
        #print(f"idx : {i}, rand : {rand}")
        problem_level=rand
            
        #print("------------")
        #print(f"problem_level : {problem_level}")
        
        if problem_level != 4:
        
            one_problem = db.query(Problem.problem,Problem.category,Problem.answer,Problem.problem_level,Problem.main_category).filter(Problem.main_category==category).filter(Problem.problem_level==problem_level).all()
            
            if len(one_problem)==0:
                problem_list.append(pbd_schema.Problem_Emit(problem_level=4))
                
            else:
                
                problem_list.append(one_problem[randint(0,len(one_problem)-1)])
            
        else:
            problem_list.append(pbd_schema.Problem_Emit(problem_level=4))
        
    return {"cnt":cnt,"problem_list":problem_list}
        
    
     
    
    
def answer_update(db:Session):
    detail_all=db.query(Detail).all()
    for idx,detail in enumerate(detail_all):
        if detail.category!="식을 만족하는 x 값 찾기" and \
            detail.category!="지수 함수 값 계산하기" and \
                detail.category!="제곱근 계산":
            #print("!!SDDSDDDS")
            # 지금까지 있던 문제 분류에 대해 problem 추가 하면 없애도 됨
            
            continue
        
        
        #print("----------------------")
        #print("#",detail)
        #print(detail.problem)
        pb = db.query(Problem).filter(Problem.problem == detail.problem).first()
        
        if pb.answer!=0:
            continue
        #print(idx)
        #print(pb.problem)
        #print(detail.problem_answer)
        pb.answer = detail.problem_answer
        
        db.commit()
    
    
def bundles_update(db:Session):
    problem_set= db.query(Problem).all()
    
    
    #print(f"probelm_set size : {len(problem_set)}")
    
    for i,pb in enumerate(problem_set):
        if pb.category == "지수 함수 값 계산하기":
            pb.bundles_idx_list = "[[0,1]]"
            
        elif pb.category == "제곱근 계산":
            lt = []
            str2list = json.loads(pb.problem_list)
            for i in range(len(str2list)-2): # 값이 음수면 인덱스 값이 아닌 실제 값을 의미, -를 붙여서 사용
                lt.append([-(i+1),str2list[i]])
                
            lt.append([len(str2list)-2,len(str2list)-1])    
                
            pb.bundles_idx_list = str(lt)
            
        elif pb.category == "식을 만족하는 x 값 찾기":
            pb.bundles_idx_list = "[[0,1],[2,4]]"
        
        
        #print(f"finish i : {i}")
        
        
    db.commit()
        
            
def problem_trytime_update(db:Session):
    problem_set= db.query(Problem).all()
    
    def problem_reset(problem_set):
    
        #print(f"probelm_set size : {len(problem_set)}")
        """27434 {4}^{2} = ?
        27435 {(-3)}^{2} = ?"""
        
        
        for i,pb in enumerate(problem_set):
            pb.trystudent = 0
            pb.trytime = 0
            pb.problem_level = 0
            #print(f"finish i : {i}")
            
        db.commit()
        
    #problem_reset(problem_set=problem_set
    
    details = db.query(Detail).all()
    
    
    for i,detail in enumerate(details): 
        if check_problem_in_db(db,detail.problem):
            #print(detail.id,detail.problem)
            try_update(db,detail.problem,detail.trytime)
            
            
        #print(f"finish i : {i}")
            
            
    db.commit()
        
            

# def get_problem(db: Session, category_number : int = 0):
#     _get_problem = db.query(PROBLEM).filter(PROBLEM.category_number==category_number).all()

#     return _get_problem

# def Title_name2number(db: Session, title_name : str = ""):
#     get_title_number = db.query(PROBLEM_TITLE).filter(PROBLEM_TITLE.title==title_name).first().title_number

#     return get_title_number



# def create_title(db: Session,
#                   problem_create: ProblemTitleCreate):
    

#     number=int(db.query(PROBLEM_TITLE).count()+1)

#     db_problem_title = PROBLEM_TITLE(
#         title=problem_create.title,
#         title_number=number)
    
    
#     db.add(db_problem_title)
#     db.commit()
    
#     return db_problem_title


# def get_title(db: Session):
#     _get_title = db.query(PROBLEM_TITLE).all()
#     return _get_title