from models import School
from sqlalchemy.orm import Session
import datetime
import asyncio

def create_school(db:Session,school_name : str,address : str):
    
    
    db_school = School(school_name=school_name,
                       address=address)
    
    db.add(db_school)
    db.commit()
    
    
def school_list(db:Session):
    
    schools=db.query(School).all()
    
    return schools


def school_search_list(db:Session,search_text:str):
    search = "%{}%".format(search_text)
    search_result = db.query(School).filter(School.school_name.like(search)).all()

    
    return search_result

def school_limited_search_list(db:Session,search_text:str,search_data_cnt : int, now_page : int):
    search = "%{}%".format(search_text)
    _search_result = db.query(School).filter(School.school_name.like(search))
    search_result_cnt = _search_result.count()
    search_result = _search_result.offset(search_data_cnt*(now_page-1)).limit(search_data_cnt).all()

    return search_result_cnt,search_result


#rank_list = _rank_list.offset(page_data_cnt*(now_page-1)).limit(page_data_cnt).all()