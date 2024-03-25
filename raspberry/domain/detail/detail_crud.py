from models import Detail,Record
from sqlalchemy.orm import Session

from domain.detail.detail_schema import DetailCreate


def detail_size(db: Session):
    record = db.query(Detail).count()
    return record


def create_detail(db: Session, record : Record,
                  detail_create: DetailCreate):

    db_question = Detail(
                        category=detail_create.category,
                        problem = detail_create.problem,
                        problem_answer = detail_create.problem_answer,
                        user_answers = detail_create.user_answers,
                        record=record
                        )
    db.add(db_question)
    db.commit()
    
def get_detail_list(db: Session, record_id: int = 1): # skip : 데이터 시작 위치, limit : 데이터 건수
    _detail_list = db.query(Record).filter(Record.id == record_id).first()

    return _detail_list  # (전체 건수, 페이징 적용된 질문 목록)