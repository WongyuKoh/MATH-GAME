import datetime
from typing import Optional, Union

from pydantic import BaseModel,validator
#from models import Detail


class Detail(BaseModel):
    category : str = "" # 문제 분류
    problem : str = "" # 문제 
    problem_answer : str = "" # 문제 답
    user_answers : str = "" # 문제에 대한 유저의 답(응답,응답,... 형태의 문자열) 
    
    
    class Config:
        from_attributes = True
        
class DetailCreate(BaseModel):
    trytime : int = 0 # 시도 횟수
    category : str = "" # 문제 분류
    problem : str = "" # 문제 
    problem_answer : str = "" # 문제 답
    user_answers : str = "" # 문제에 대한 유저의 답(응답,응답,... 형태의 문자열) 
    
    
    
"""class RecordList(BaseModel):
    total: int = 0
    record_list : list[Record] = []"""
    