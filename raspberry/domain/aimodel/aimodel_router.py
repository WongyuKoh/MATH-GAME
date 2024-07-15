from fastapi import APIRouter,HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status
from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt,JWTError
from argon2.exceptions import VerificationError

from database import get_db
from domain.user.user_crud import get_user_detail
from domain.aimodel import aimodel_schema
from domain.record import record_schema, record_crud
from domain.detail import detail_crud
from sklearn.linear_model import LinearRegression
import numpy as np
from models import Detail,Record,Problem,User


import json
import numpy as np

from domain.problem_parsing.exponents import problem_e_1
from domain.problem_parsing.exponents import problem_e_2
from domain.problem_parsing.exponents import problem_e_3


router = APIRouter(
    prefix="/api/aimodel",
)

def reverse_func(model,x): # x는 n번째 시도 때 시도/문제수 값
    return (x-model.intercept_)/(model.coef_) # 예측한 번째수

def FUNC(model,n,x): #  n : 실제 시도 횟수, x : 시도 때 시도/문제수 값
    print(max(0,(reverse_func(model,x)[0]-n)))
    return max(1,10-max(0,(reverse_func(model,x)[0]-n))/10)


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

def e1(x): # x : 표준 편차 값
    return min(max(0,60-(x/8.4)),60)

def e2(db,x): # x : 현재 점수 값
    _rank_list = db.query(User.username,User.school_number,User.exponential_score)
    # 랭킹 시스템을 바꿔야됨
    # 자신의 수업에서 제공된 문제에 대한 랭킹 판이 다로 존재해야됨
    # 점수를 정렬 할때 어떤 값이든 숫자의 차이로 랭킹을 찾을 수 있어야 됨
    # 점수를 나열하고 자기보다 큰 숫자 + 1 만큼을 성적으로 둬서 값을 출력하기
    _rank_list = _rank_list.order_by(User.exponential_score.desc()) # order_by : 정렬, desc : 내림차순 정렬, asc : 오름차순 정렬
        
    rank = 1
    
    return min(max(0,(-2/13)*rank + 40),40)


@router.get("/evaluate", response_model=aimodel_schema.StudentEvaluate)
def user_evaluate(_record_create: record_schema.RecordCreate,
                  db: Session = Depends(get_db), 
                  school_number : int = 0, school_id : int = 0,record_id : int = 0):
    
    
    # Linear Model
    
    last_details = get_user_detail(db,school_id=school_id,school_number=school_number)
    
    print(last_details)
    #_record_create
    records=[]
    for record in last_details:
        if (record['correct_pb_cnt']+record['wrong_pb_cnt'])==0:continue
        v = record['trytime']/(record['correct_pb_cnt']+record['wrong_pb_cnt'])
        if v<1:continue
        records.append(min(5,v))
        
    X=[i+1 for i in range(len(records))]
    
    
        
    model = LinearRegression()
    x=np.array(X)
    y=np.array(records)
    model.fit(X=x.reshape(-1, 1),y=y)

    #pred = model.predict(x.reshape(-1, 1))
        
    _record_create.detail
    
    if (_record_create.correct_pb_cnt+_record_create.wrong_pb_cnt)==0:
        # 수정하기
        return {"school_number":1}
    
    V = _record_create.trytime/(_record_create.correct_pb_cnt+_record_create.wrong_pb_cnt)
    
    rate = FUNC(model,len(X)+1,V)
    
    game_detail = detail_crud.get_detail_list(db=db,record_id=record_id)
    
    data_value = {}
    
    for one_detail in game_detail.detail:
        one_problem = db.query(Problem).filter(Problem.problem==one_detail.problem).first()
        
        cnt=findtrytime(one_detail.user_answer)
        
        # 조합을 지정해서 묶는게 좋을 듯
        # 문제 별 조합을 db 에 저장, 저장된걸 불러오는 형식
        # 인덱스 별로 해당되는거 묶음
        
        #one_detail.category
        bundles = json.loads(one_problem.bundles_idx_list)
        problem_list = json.loads(one_problem.problem_list)
        
        # 조합이 다른 것도 그냥 하나로 묶어서 하기
    
        for idx,bundle in enumerate(bundles):
            if bundle[0]<0:
                one_data=str([-bundle[0],problem_list[bundle[1]]])
            else:
                one_data=str([problem_list[bundle[0]],problem_list[bundle[1]]])
                
                
            if one_data in data_value:
                data_value[one_data][0]+=cnt * rate
                data_value[one_data][1]+=1
                
            else:
                data_value[one_data] = [cnt * rate, 1]
            
            
    result = []    
                
    for data in data_value:
        result.append(10*(data_value[data][0]/data_value[data][1]))
        
        
    STD = np.std(np.array(result))
    
    P = e1(STD) + e2(db,game_detail.score)
    
    student_level = 0
    if 80<=P:
        student_level = 1
    elif 65<=P<80:
        student_level = 2
    else:
        student_level = 3
        
    
    return {"score":P,"level":student_level}
    
    """
    
    
 {
  "id": 20,
  "main_category": "로그",
  "correct_pb_cnt": 38,
  "wrong_pb_cnt": 5,
  "score": 8,
  "user_name": "고원규",
  "create_date": "2024-03-15T05:29:00",
  "trytime": 13,
  "school_id": 1,
  "detail": [
    {
      "category": "로그 값 맞추기",
      "problem": "log_{4}{64} = ?",
      "problem_answer": "3",
      "user_answers": "3"
    },
    """
    
    """
    
    stack={}
for data in using_data:
  if str(data[1:]) in stack:
    stack[str(data[1:])][0]+=data[0]*12.5
    stack[str(data[1:])][1]+=1
  else:
    stack[str(data[1:])]=[data[0]*12.5,1]

print(stack)
x=[]
y=[]
r=[]
for data in stack:
  Data=json.loads(data)
  x.append(Data[0])
  y.append(Data[1])
  r.append(10*(stack[data][0]/stack[data][1]))
    """