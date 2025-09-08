from models import Detail,Record
from sqlalchemy.orm import Session

from domain.detail.detail_schema import DetailCreate


def detail_size(db: Session):
    record = db.query(Detail).count()
    return record

def findtrytime(text):

	#text=data_parsing['user_answers']
	text=text.replace(',,',',')
	text=text.split(',')

	trytime = -1
	if len(text)==0:
		if len(text)==0:
			trytime=5
		elif text=="ac":
			trytime=1
		else:
			trytime=5
	else:
		if text[-1]=='wa' or text[-1]=='w':
			trytime=5
		elif text[-1]=='ac' or text[-1]=='c':
			trytime=len(text)
		else:
			if text[-1]=='':
				trytime=5
			else:
				trytime=len(text)
    

	if trytime>4:
		trytime=5

	return trytime

def create_detail(db: Session, record : Record,
                  detail_create: DetailCreate):
    
    
    cnt = findtrytime(detail_create.user_answers)
	
    db_question = Detail(
                        category=detail_create.category,
                        problem = detail_create.problem,
                        problem_answer = detail_create.problem_answer,
                        user_answers = detail_create.user_answers,
                        record=record,
                        trytime = cnt,
                        )
    db.add(db_question)
    db.commit()
    
    return cnt
    
def get_detail_list(db: Session, record_id: int = 1): # skip : 데이터 시작 위치, limit : 데이터 건수
    _detail_list = db.query(Record).filter(Record.id == record_id).first()

    return _detail_list  # (전체 건수, 페이징 적용된 질문 목록)

def detail_trytime_update(db: Session):
    
    detail_list = db.query(Detail).all()
    for i in range(len(detail_list)):
        detail_list[i].trytime = findtrytime(detail_list[i].user_answers)
        
    db.commit()
