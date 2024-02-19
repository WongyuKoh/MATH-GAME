import datetime
from typing import Optional, Union

from pydantic import BaseModel,validator
from domain.detail.detail_schema import Detail


class Record(BaseModel):
    id : int = 0
    correct_pb_cnt : int = 0
    wrong_pb_cnt : int = 0
    score : int = 0
    create_date: datetime.datetime
    detail : list[Detail] = []
    
    
    class Config:
        from_attributes = True
        
class RecordCreate(BaseModel):
    correct_pb_cnt : int = 0
    wrong_pb_cnt : int = 0
    score : int = 0
    create_date: datetime.datetime
    detail : list[Detail] = [Detail()]
    

    
"""class RecordList(BaseModel):
    total: int = 0
    record_list : list[Record] = []"""