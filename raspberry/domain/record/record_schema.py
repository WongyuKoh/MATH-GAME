import datetime
from typing import Optional, Union

from pydantic import BaseModel,validator
from domain.detail.detail_schema import Detail


class Categorylist(BaseModel):
    classcategorylist : list = []

class Record(BaseModel):
    id : int = 0
    main_category : str = ""
    correct_pb_cnt : int = 0
    wrong_pb_cnt : int = 0
    score : int = 0
    user_name : str = ""
    create_date: datetime.datetime
    trytime : int = 0
    school_id : int = 0
    detail : list[Detail] = []
    
    
    class Config:
        from_attributes = True
        
class RecordCreate(BaseModel):
    main_category : str = ""
    correct_pb_cnt : int = 0
    wrong_pb_cnt : int = 0
    score : int = 0
    trytime : int = 0
    detail : list[Detail] = [Detail()]
    

    
class RecordList(BaseModel):
    record_list : list[Record] = []
    
    
class RecordCnt(BaseModel):
    record_cnt : int = 0
    
class RecordClassCnt(BaseModel):
    record_class : list = []
    
class nodetail_Record(BaseModel):
    id : int = 0
    main_category : str = ""
    correct_pb_cnt : int = 0
    wrong_pb_cnt : int = 0
    score : int = 0
    user_name : str = ""
    create_date: datetime.datetime
    trytime : int = 0
    school_id : int = 0
    
    
    class Config:
        from_attributes = True
    
