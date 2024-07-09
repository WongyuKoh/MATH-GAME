from models import User, Record,Detail
from sqlalchemy.orm import Session
import datetime
from sqlalchemy.sql import func

from domain.record.record_schema import RecordCreate


def DateTimeNow():
    nowDate=datetime.datetime.now()
    return f"{str(nowDate.year)}-{str(nowDate.month)}-{str(nowDate.day)} {str(nowDate.hour)}:{str(nowDate.minute)}:{str(nowDate.second)}.{str(nowDate.microsecond)}"



def get_record(db: Session, question_id: int):
    question = db.query(Record).get(question_id)
    return question

"""create_record(db, user=user,
                              record_create=_record_create,
                              record=current_user)"""
                              
                              
def trytime_update(db : Session, record : Record,cnt : int):
    record_by_id = db.query(Record).filter(Record.id == record.id).first()
    record_by_id.trytime = cnt
    db.commit()
    
    
def record_trytime_update(db : Session):
    records = db.query(Record).all()
    for record in records:
        detail_by_record_list=db.query(Detail).filter(Detail.record_id == record.id).all()
        cnt=0
        for one_detail in detail_by_record_list:
            cnt+=one_detail.trytime
            
        record.trytime=cnt
        
    db.commit()
    

def create_record(db: Session, user : User,
                  record_create: RecordCreate,school_id : int):
    

    db_record = Record(
                         correct_pb_cnt=record_create.correct_pb_cnt,
                           wrong_pb_cnt=record_create.wrong_pb_cnt,
                           create_date=datetime.datetime.now(), score=record_create.score,
                           main_category=record_create.main_category,
                           user_id=user.school_number,user_name=user.username,
                           trytime=0,school_id=school_id)
    db.add(db_record)
    db.commit()
    
    ID=db.query(User).filter(User.school_number == user.school_number).first()
    if record_create.main_category=="지수":
        ID.exponential_score=max(record_create.score,ID.exponential_score)
    elif record_create.main_category=="로그":
        ID.log_score=max(record_create.score,ID.log_score)
    elif record_create.main_category=="수열":
        ID.sequence_score=max(record_create.score,ID.sequence_score)

    db.commit()  
    
    return db_record


# 수정중
def aidata_record(db: Session, school_number : int, category : str):
    aidata_record_by_Record = db.query(Record).filter(Record.user_id==school_number).filter(Record.main_category==category).all()
    
    #for i in range(len(aidata_record_by_Record)):
        #aidata_record_by_Record[i]["detail"]
    
    return aidata_record_by_Record


def get_record_by_category(db: Session, school_number : int, category : str,cnt : int):
    _get_record_by_category = db.query(Record).filter(Record.user_id==school_number).filter(Record.main_category==category)
    
    get_record_by_category=_get_record_by_category.limit(cnt).all()

    return get_record_by_category

def get_record_by_category_all(db: Session, school_number : int, category : str):
    _get_record_by_category = db.query(Record).filter(Record.user_id==school_number).filter(Record.main_category==category).all()
    
    #print(get_record_by_category)
    print(_get_record_by_category[0])
    return _get_record_by_category

def get_record_cnt_all(db: Session, school_number : int):
    _get_record_by_category = db.query(Record).filter(Record.user_id==school_number).all()
    
    return len(_get_record_by_category)

def get_record_class_cnt_all(db: Session, school_class: int = 1): # skip : 데이터 시작 위치, limit : 데이터 건수
    _question_list = db.query(User)\
        .order_by(User.school_number.asc()) # order_by : 정렬, desc : 내림차순 정렬, asc : 오름차순 정렬

    question_list = _question_list.filter((User.school_number//100)%10==school_class).all()
    stack=[]
    user_stack=[]
    for data in question_list:
        if not data.school_number in user_stack:
            stack.append({
                "school_number" : data.school_number,
                "username" : data.username, 
                "record_cnt" : get_record_cnt_all(db,data.school_number)
            })
            user_stack.append(data.school_number)

    return stack 

"""create_record(db, user=user,
                              record_create=_record_create,
                              record=current_user)"""
    
"""def get_record_list(db: Session, skip: int = 0, limit: int = 10): # skip : 데이터 시작 위치, limit : 데이터 건수
    _question_list = db.query(Record)\
        .order_by(Record.create_date.desc()) # order_by : 정렬

    total = _question_list.count() # question_list 에 answer 도 들어있음
    question_list = _question_list.offset(skip).limit(limit).all() # offset : 어디부터 불러온건지 정하는 db 문법, limit : limit 변수와 동일한 db문법
    
    return total, question_list  # (전체 건수, 페이징 적용된 질문 목록)"""