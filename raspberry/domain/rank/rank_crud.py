from sqlalchemy.orm import Session
from models import Record



def get_rank_list(db: Session, page_data_cnt : int = 10 ,now_page : int = 1): # skip : 데이터 시작 위치, limit : 데이터 건수
    _rank_list = db.query(Record)\
        .order_by(Record.score.desc()) # order_by : 정렬, desc : 내림차순 정렬, asc : 오름차순 정렬
        
    
    rank_list = _rank_list.offset(page_data_cnt*(now_page-1)).limit(page_data_cnt).all()
    
    return rank_list  # (전체 건수, 페이징 적용된 질문 목록)


def get_rank_class_list(db: Session, class_number : int = 1): # skip : 데이터 시작 위치, limit : 데이터 건수
    _rank_list = db.query(Record)\
        .order_by(Record.score.desc()) # order_by : 정렬, desc : 내림차순 정렬, asc : 오름차순 정렬
        
        
    rank_list = _rank_list.filter((Record.user_id//100)%10==class_number).all()
    
    return rank_list  # (전체 건수, 페이징 적용된 질문 목록)

def get_rank_user(db: Session, school_number : int = 1,score : int = 0): # skip : 데이터 시작 위치, limit : 데이터 건수
    _rank_user = db.query(Record).order_by(Record.score.desc())
    
    rank_user = _rank_user.filter(Record.user_id==school_number).filter(Record.score==score).first()

    rank = _rank_user.filter(Record.score>score).count()+1

        
    
    return rank,rank_user  # (전체 건수, 페이징 적용된 질문 목록)    

def get_rank_user_profile(db: Session, school_number : int = 1): # skip : 데이터 시작 위치, limit : 데이터 건수
    _rank_user = db.query(Record).order_by(Record.score.desc())
    
    rank_user = _rank_user.filter(Record.user_id==school_number).first()

    rank = _rank_user.filter(Record.score>rank_user.score).count()+1

        
    
    return rank,rank_user  # (전체 건수, 페이징 적용된 질문 목록)    