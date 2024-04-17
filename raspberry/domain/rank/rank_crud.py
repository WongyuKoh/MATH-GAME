from sqlalchemy.orm import Session
from sqlalchemy import desc,distinct ,select
from models import Record,User


"""def user_high_rank_list(db : Session,category : str = ""):
    _sub_user_high_rank_list = select(Record.score,Record.user_id,Record.user_name).select_from(Record)#db.query(_sub_user_high_rank_list).filter(Record.main_category==category).order_by(Record.score.desc())
         # order_by : 정렬, desc : 내림차순 정렬, asc : 오름차순 정렬
    _user_high_rank_list=db.scalars(_sub_user_high_rank_list.where(Record.#db.query(Record.user_id).distinct().subquery()
    print(_sub_user_high_rank_list)
    rank_list=list(_user_high_rank_list)
    print(rank_list)
    for i in range(len(rank_list)):
        print(rank_list[i].user_name,rank_list[i].score)
    """



def get_rank_list(db: Session, page_data_cnt : int = 10 ,now_page : int = 1,category : str = ""): # skip : 데이터 시작 위치, limit : 데이터 건수
    
    if category=="지수":  
        _rank_list = db.query(User.username,User.school_number,User.exponential_score)
        _rank_list = _rank_list.order_by(User.exponential_score.desc()) # order_by : 정렬, desc : 내림차순 정렬, asc : 오름차순 정렬
    elif category=="로그":  
        _rank_list = db.query(User.username,User.school_number,User.log_score)
        _rank_list = _rank_list.order_by(User.log_score.desc()) # order_by : 정렬, desc : 내림차순 정렬, asc : 오름차순 정렬  
    elif category=="수열":  
        _rank_list = db.query(User.username,User.school_number,User.sequence_score)
        _rank_list = _rank_list.order_by(User.sequence_score.desc()) # order_by : 정렬, desc : 내림차순 정렬, asc : 오름차순 정렬
    
    rank_list = _rank_list.offset(page_data_cnt*(now_page-1)).limit(page_data_cnt).all()
    
    
    return rank_list  # (전체 건수, 페이징 적용된 질문 목록)


def get_rank_class_list(db: Session, class_number : int = 1,category : str = ""): # skip : 데이터 시작 위치, limit : 데이터 건수
    
    if category=="지수":  
        _rank_list = db.query(User.username,User.school_number,User.exponential_score)
        _rank_list = _rank_list.order_by(User.exponential_score.desc()) # order_by : 정렬, desc : 내림차순 정렬, asc : 오름차순 정렬
    elif category=="로그":  
        _rank_list = db.query(User.username,User.school_number,User.log_score)
        _rank_list = _rank_list.order_by(User.log_score.desc()) # order_by : 정렬, desc : 내림차순 정렬, asc : 오름차순 정렬  
    elif category=="수열":  
        _rank_list = db.query(User.username,User.school_number,User.sequence_score)
        _rank_list = _rank_list.order_by(User.sequence_score.desc()) # order_by : 정렬, desc : 내림차순 정렬, asc : 오름차순 정렬
        
    rank_list = _rank_list.filter((User.school_number//100)%10==class_number).all()
    
    return rank_list  # (전체 건수, 페이징 적용된 질문 목록)
 

def get_rank_user_profile(db: Session, school_number : int = 1,category : str = ""): # skip : 데이터 시작 위치, limit : 데이터 건수
    
    if category=="지수": 
        _rank_user = db.query(User.username,User.school_number,User.exponential_score)
        _rank_user = _rank_user.order_by(User.exponential_score.desc()) # order_by : 정렬, desc : 내림차순 정렬, asc : 오름차순 정렬
    elif category=="로그":  
        _rank_user = db.query(User.username,User.school_number,User.log_score)
        _rank_user = _rank_user.order_by(User.log_score.desc()) # order_by : 정렬, desc : 내림차순 정렬, asc : 오름차순 정렬  
    elif category=="수열":  
        _rank_user = db.query(User.username,User.school_number,User.sequence_score)
        _rank_user = _rank_user.order_by(User.sequence_score.desc()) # order_by : 정렬, desc : 내림차순 정렬, asc : 오름차순 정렬
    
    rank_user = _rank_user.filter(User.school_number==school_number)

    if rank_user.count()==0:
        return -1,rank_user
    else:
        rank_user=rank_user.first()
    
    if category=="지수":  
        rank = _rank_user.filter(User.exponential_score>rank_user.exponential_score).count()+1
    elif category=="로그":  
        rank = _rank_user.filter(User.log_score>rank_user.log_score).count()+1
    elif category=="수열":  
        rank = _rank_user.filter(User.sequence_score>rank_user.sequence_score).count()+1
        
    else:
        rank = -1
    
    return rank,rank_user  # (전체 건수, 페이징 적용된 질문 목록)    