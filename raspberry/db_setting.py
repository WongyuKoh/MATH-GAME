

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
import requests
import random
import time
#http://127.0.0.1:8000/api/record/create/20402/
cnt=0
for i in range(1,10):
    for g in range(1,30):
        school_number="20"+str(i)
        if g<10:school_number+="0"
        school_number+=str(g)
        if(int(school_number)==20402):continue
        st=["수열","로그","지수"]
        upload = {
            "main_category": st[random.randint(0,2)],
            "correct_pb_cnt": 1231231,
            "wrong_pb_cnt": 234234234,
            "score": 1234432,
            "detail": [
                {
                "category": "ㅃ",
                "problem": "ㄹ",
                "problem_answer": "ㅇ",
                "user_answers": "ㄸ"
                } for _ in range(60)
            ]
        }
        print(upload)
        cnt+=1
        #http://127.0.0.1:8000/api/user/create
        requests.post("http://127.0.0.1:8000/api/record/create/"+str(school_number), json=upload)
        
        #requests.post("http://127.0.0.1:8000/api/record/create/"+str(school_number), json=upload)
print(cnt)   
#requests.post("http://127.0.0.1:8000/api/record/create/20402/", json=upload)
