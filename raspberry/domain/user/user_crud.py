#from passlib.context import CryptContext
from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate
from models import User
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
    
    
def get_user(db: Session, school_number: str):
    return db.query(User).filter(User.school_number == school_number).first()

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