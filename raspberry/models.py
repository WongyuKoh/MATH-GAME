"""
    [그리움] [오후 12:35] 어떤 유형까지 풀었는지 확인할수 있어야 세특이나 평가에 반영할수 있을것같아
    [그리움] [오후 12:36] 아니면 몇문제정도 풀었는지??
    [그리움] [오후 12:36] 최종점수가 몇점인지
"""
    
"""
    sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) Cannot add a NOT NULL column with default value NULL
    [SQL: ALTER TABLE record ADD COLUMN score INTEGER NOT NULL]
    (Background on this error at: https://sqlalche.me/e/20/e3q8)

    에러가 나는 이유는 새로운 항목을 추가할때 nullable=False 라고 해두면 다른 위치의 값을 설정해야 됨
    안그러면 null 이 들어갈 수 없으므로 에러,
    또는 nullable=False 를 해도 됨

    """

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

    
class User(Base):
    __tablename__ = "user"

    
    school_number = Column(Integer, primary_key=True) # 학번 , 로그인 시 사용
    username = Column(String, nullable=False) # 실제 이름
    password = Column(String, nullable=False)
    
class Record(Base): # user 에 종속, record 복수
    __tablename__ = "record"

    id = Column(Integer, primary_key=True)
    score = Column(Integer,nullable=False, primary_key=False)
    correct_pb_cnt = Column(Integer, primary_key=False)
    wrong_pb_cnt = Column(Integer, primary_key=False)
    
    
    create_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("user.school_number"), nullable=True)
    user = relationship("User",backref="records")
    
    
    
class Detail(Base): # user 에 종속, record 복수
    __tablename__ = "detail"

    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False) # 문제 분류
    problem = Column(String, nullable=False) # 문제 
    problem_answer = Column(String, nullable=False) # 문제 답
    user_answers = Column(String, nullable=False) # 문제에 대한 유저의 답(응답,응답,... 형태의 문자열) 
    
    
    record_id = Column(Integer, ForeignKey("record.id"), nullable=True)
    record = relationship("Record",backref="detail")