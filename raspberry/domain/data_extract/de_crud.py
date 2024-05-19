from models import Detail,Record,User
from sqlalchemy.orm import Session

from domain.detail.detail_schema import DetailCreate


def detail_db_list(db : Session):
    return db.query(Detail).all()


def user_db_list(db : Session):
    return db.query(User).all()


def record_db_list(db : Session):
    return db.query(Record).all()


def detail_db_list_cnt(offset : int,limit : int, db : Session):
    return db.query(Detail).offset(offset).limit(limit).all()