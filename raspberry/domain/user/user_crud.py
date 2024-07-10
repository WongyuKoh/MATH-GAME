#from passlib.context import CryptContext
from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate
from models import User,Record,School
import asyncio
from argon2 import PasswordHasher

#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") bcrypt 코드
pwd_context = PasswordHasher()

def create_user(db: Session, user_create: UserCreate,school_id : int):
    
    
    

    db_user = User(school_number=user_create.school_number,
                    username=user_create.username,
                   password=pwd_context.hash(user_create.password1),
                   log_score=0,
                   exponential_score=0,
                   sequence_score=0,
                   school_id = school_id)
    
    db.add(db_user)
    db.commit()
    
    
def get_si2sn(db:Session,school_id:int):
    return db.query(School).filter(School.school_id==school_id).first()

    
def exist_school(db:Session,school_name:str):
    school = db.query(School).filter(School.school_name==school_name).all()
    if len(school)>0:
        return school[0].school_id
    else:
        return 0

def get_existing_user(db: Session, user_create: UserCreate,school_id : int):
    return db.query(User).filter(
        (User.school_number == user_create.school_number)
    ).filter(User.school_id == school_id).first()
    
  
def get_user(db: Session, school_number: int,school_id : int):

    return db.query(User).filter(User.school_number == school_number).filter(User.school_id==school_id).first()

def get_user_detail(db:Session,school_number : int , school_id : int):
    
    return db.query(Record).filter(Record.user_id == school_number).filter(Record.school_id==school_id).all()


def get_username(db: Session, school_number: int,school_id : int):
    return db.query(User).filter(User.school_number == school_number).filter(User.school_id==school_id).first()

def get_user_exit(db:Session,school_number:int,school_id : int):

    cnt=len(db.query(User).filter(User.school_number == school_number).filter(User.school_id==school_id).all())
    if(cnt==0):return False
    else: return True
    
def user_delete(db:Session,school_number:int,school_id : int): # get 은 filter 없을때만 작동
    ID=db.query(User).filter(User.school_number == school_number).filter(User.school_id==school_id).first()

    db.delete(ID)
    db.commit()
    
    
# 게임 랭킹 구조를 뜯어 고쳐야 됨
# 유형을 자유롭게 추가가능해야되며, 문제도 자유롭게 추가할 수 있어야 함

# ------------------------------------------------------------------------- #
    
def user_score_updatebyinput(db:Session,school_number:int,category:str,score : int): # get 은 filter 없을때만 작동
    ID=db.query(User).filter(User.school_number == school_number).first()
    if category=="지수":
        ID.exponential_score=max(score,ID.exponential_score)
    elif category=="로그":
        ID.log_score=max(score,ID.log_score)
    elif category=="수열":
        ID.sequence_score=max(score,ID.sequence_score)

    db.commit()  
    
def user_score_updatebyrecord(db:Session,school_number:int): # get 은 filter 없을때만 작동
    record_list=db.query(Record).order_by(Record.user_id.asc()).all() # order_by : 정렬, desc : 내림차순 정렬, asc : 오름차순 정렬
    ID=db.query(User).filter(User.school_number == school_number).first()
    update_on=0
    for data in record_list:
        if data.user_id==school_number:
            update_on=1
            if data.main_category=="지수":
                ID.exponential_score=max(data.score,ID.exponential_score)
            elif data.main_category=="로그":
                ID.log_score=max(data.score,ID.log_score)
            elif data.main_category=="수열":
                ID.sequence_score=max(data.score,ID.sequence_score)
        else:
            if update_on:
                break
        db.commit() 

def user_score_update_all(db:Session): # get 은 filter 없을때만 작동
    record_list=db.query(Record).order_by(Record.user_id.asc()).all() # order_by : 정렬, desc : 내림차순 정렬, asc : 오름차순 정렬
    last_school_number=-1
    ID=0
    for data in record_list:
        if last_school_number!=data.user_id:
            last_school_number=data.user_id
            ID=db.query(User).filter(User.school_number == last_school_number).first()
        if data.main_category=="지수":
            ID.exponential_score=max(data.score,ID.exponential_score)
        elif data.main_category=="로그":
            ID.log_score=max(data.score,ID.log_score)
        elif data.main_category=="수열":
            ID.sequence_score=max(data.score,ID.sequence_score)

        db.commit()  

def user_score(db:Session,school_number:int,category:str): # get 은 filter 없을때만 작동
    ID=db.query(User).filter(User.school_number == school_number).first()
    
    if category=="지수":
        return ID.exponential_score
    elif category=="로그":
        return ID.log_score
    elif category=="수열":
        return ID.sequence_score
    
 
 # ------------------------------------------------------------------------- #
    
    
# ------------------------------------------------------------------------- #    
    
    
def user_password_change(db:Session,school_number:int,new_password:str,school_id:int):

    ID=db.query(User).filter(User.school_number == school_number).filter(User.school_id==school_id).first()
    ID.password=pwd_context.hash(new_password)
    db.commit()
    
def user_username_change(db:Session,school_number:int,new_username:str,school_id:int):

    ID=db.query(User).filter(User.school_number == school_number).filter(User.school_id==school_id).first()
    ID.username=new_username
    db.commit()
    async def change_school_number(new_username,school_number):
        change_list=db.query(Record).filter(Record.user_id==school_number).all()
        for data in change_list:
            data.user_name = new_username
            
        db.commit()
        
    asyncio.run(change_school_number(school_number=school_number,new_username=new_username))
    
    
def user_school_number_change(db:Session,school_number:int,new_school_number:str,school_id:int):
    
    if get_user_exit(db,school_number):
        
        ID=db.query(User).filter(User.school_number == school_number).filter(User.school_id==school_id).first()
        ID.school_number=new_school_number
        db.commit()
        async def change_school_number(school_number,new_school_number):
            change_list=db.query(Record).filter(Record.user_id==school_number).all()
            for data in change_list:
                data.user_id = new_school_number
                
            db.commit()
            
        asyncio.run(change_school_number(school_number=school_number,new_school_number=new_school_number))
        
        return 1
    
    else:
        return 0
        


def get_user2name(db: Session, username: str,school_id : int = 0):
    return db.query(User).filter(User.username == username).filter(User.school_id==school_id).first()


def get_user_list(db: Session, school_class: int = 1,school_id : int = 0): # skip : 데이터 시작 위치, limit : 데이터 건수
    _question_list = db.query(User).filter(User.school_id==school_id)\
        .order_by(User.school_number.asc()) # order_by : 정렬, desc : 내림차순 정렬, asc : 오름차순 정렬

    total = _question_list.count() # question_list 에 answer 도 들어있음
    #print("-"*15)
    #print(f"User.school_number : {User.school_number}")
    #print(f"school_class : {school_class}")
    #print(f"question_list : {_question_list}")
    question_list = _question_list.filter((User.school_number//100)%100==school_class).all()
    
    return total, question_list  # (전체 건수, 페이징 적용된 질문 목록)"""