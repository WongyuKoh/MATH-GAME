import datetime
from typing import Optional, Union

from pydantic import BaseModel,validator
from domain.detail.detail_schema import Detail


class Record(BaseModel):
    id : int = 0
    main_category : str = ""
    correct_pb_cnt : int = 0
    wrong_pb_cnt : int = 0
    score : int = 0
    user_name : str = ""
    create_date: datetime.datetime
    detail : list[Detail] = []
    
    
    class Config:
        from_attributes = True
        
class RecordCreate(BaseModel):
    main_category : str = ""
    correct_pb_cnt : int = 0
    wrong_pb_cnt : int = 0
    score : int = 0
    detail : list[Detail] = [Detail()]
    

    
class RecordList(BaseModel):
    record_list : list[Record] = []