#from passlib.context import CryptContext
from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate
from models import User,Record
import asyncio
from argon2 import PasswordHasher

#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") bcrypt 코드
pwd_context = PasswordHasher()

def create_user(db: Session, user_create: UserCreate):
    db_user = User(school_number=user_create.school_number,
                    username=user_create.username,
                   password=pwd_context.hash(user_create.password1))
    db.add(db_user)
    db.commit()

def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter(
        (User.school_number == user_create.school_number)
    ).first()
    
    
def get_user(db: Session, school_number: int):

    return db.query(User).filter(User.school_number == school_number).first()

def get_username(db: Session, school_number: int):
    return db.query(User).filter(User.school_number == school_number).first()

def get_user_exit(db:Session,school_number:int):

    cnt=len(db.query(User).filter(User.school_number == school_number).all())
    if(cnt==0):return False
    else: return True
    
def user_delete(db:Session,school_number:int): # get 은 filter 없을때만 작동
    ID=db.query(User).filter(User.school_number == school_number).first()

    db.delete(ID)
    db.commit()
    
def user_password_change(db:Session,school_number:int,new_password:str):

    ID=db.query(User).filter(User.school_number == school_number).first()
    ID.password=pwd_context.hash(new_password)
    db.commit()
    
def user_username_change(db:Session,school_number:int,new_username:str):

    ID=db.query(User).filter(User.school_number == school_number).first()
    ID.username=new_username
    db.commit()
    
def user_school_number_change(db:Session,school_number:int,new_school_number:str):
    
    if get_user_exit(db,school_number):
        
        ID=db.query(User).filter(User.school_number == school_number).first()
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
        


def get_user2name(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_list(db: Session, school_class: int = 1): # skip : 데이터 시작 위치, limit : 데이터 건수
    _question_list = db.query(User)\
        .order_by(User.school_number.asc()) # order_by : 정렬, desc : 내림차순 정렬, asc : 오름차순 정렬

    total = _question_list.count() # question_list 에 answer 도 들어있음
    #print("-"*15)
    #print(f"User.school_number : {User.school_number}")
    #print(f"school_class : {school_class}")
    #print(f"question_list : {_question_list}")
    question_list = _question_list.filter((User.school_number//100)%10==school_class).all()
    
    return total, question_list  # (전체 건수, 페이징 적용된 질문 목록)