from models import Problem,Detail
from sqlalchemy.orm import Session
import datetime
import asyncio
import re
import json
from domain.problem_data.pbd_schema import ProblemCreate,ProblemTitleCreate
import domain.problem_parsing.exponents.problem_e_1 as pe1
import domain.problem_parsing.exponents.problem_e_2 as pe2
import domain.problem_parsing.exponents.problem_e_3 as pe3

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


def create_problem(db: Session,
                  problem_create: ProblemCreate = None,
                  trytime = 0):
    
    if check_problem_in_db(db,problem_create.problem):
        try_update(db,problem_create.problem,trytime=trytime)
        return
    
    
    trystudent=1
    problem_level = problem_level_return(trytime=trytime,trystudent=trystudent)
    
    # db 에 같은 유형인 거와 bundles_idx_list 가 일치 할거임
    
    
    
    category = problem_create.category
    problem_text = problem_create.problem
    
    problem_list = []
    
    #print(category,problem_text)
    
    #problem_list = list(map(int,re.findall(r'\d+',problem_text))) 문자에서 숫자만 추출하는 코드
    
    bundles_idx_list = problem_create.bundles_idx_list
    
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
        return
    
    
    db_problem = Problem(
        problem=problem_text,
        problem_list=problem_list,
        category=category,
        trytime = trytime,
        trystudent = trystudent,
        problem_level = problem_level,
        bundles_idx_list = bundles_idx_list,
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
    
    async def create_problem_all(details):
    
        for detail in details: 
            # 수정중
            create_problem(db,
                           problem_create=ProblemCreate(problem=detail.problem,category=detail.category,bundles_idx_list=""),
                           trytime=detail.trytime)
                
                
        db.commit()
        
    asyncio.run(create_problem_all(details=details))
    
def bundles_update(db:Session):
    problem_set= db.query(Problem).all()
    
    async def bundle_idx_update(problem_set):
    
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
        
    asyncio.run(bundle_idx_update(problem_set=problem_set))
        
            
def problem_trytime_update(db:Session):
    problem_set= db.query(Problem).all()
    
    async def problem_reset(problem_set):
    
        #print(f"probelm_set size : {len(problem_set)}")
        """27434 {4}^{2} = ?
        27435 {(-3)}^{2} = ?"""
        
        
        for i,pb in enumerate(problem_set):
            pb.trystudent = 0
            pb.trytime = 0
            pb.problem_level = 0
            #print(f"finish i : {i}")
            
        db.commit()
        
    #asyncio.run(problem_reset(problem_set=problem_set))
    
    details = db.query(Detail).all()
    
    async def try_update_all(details):
    
        for i,detail in enumerate(details): 
            if detail.id<=29216:continue
            if check_problem_in_db(db,detail.problem):
                print(detail.id,detail.problem)
                try_update(db,detail.problem,detail.trytime)
                
                
            #print(f"finish i : {i}")
                
                
        db.commit()
        
    asyncio.run(try_update_all(details=details))
            

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