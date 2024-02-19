from database import SessionLocal
from models import User,Record
from datetime import datetime
db = SessionLocal()

"""
class Record(Base): # user 에 종속, record 복수
    __tablename__ = "record"

    id = Column(Integer, primary_key=True)
    correct_pb_cnt = Column(Integer, primary_key=False)
    wrong_pb_cnt = Column(Integer, primary_key=False)
    create_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("user.school_number"), nullable=True)
    user = relationship("User",backref="records")
    
    
    """

#q=User(school_number='20402',username='고원규',password='test')
"""db.add(q)
db.commit()
"""

print(db.query(User).count())